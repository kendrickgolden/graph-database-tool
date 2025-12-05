
#import sys
#print(sys.executable)

from neo4j import GraphDatabase
from itertools import combinations
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "00000000")

#Jaccard index measured by |A int. B| / |A union B|
'''def find_jaccard_similarity(set1, set2):
    set_intersection = set1.intersection(set2)
    set_union = set1.union(set2)
    if not set_union:
        return 0
    return len(set_intersection) / len(set_union)'''

#Jaccard index, while also accounting for duplicate AST node types
def multiset_jaccard(list1, list2):
    counter1 = Counter(list1)
    counter2 = Counter(list2)

    #calculcate the number of times a label occurs in both methods, and return sum over all labels
    intersection_count = sum(min(counter1[k], counter2[k]) for k in counter1.keys() | counter2.keys())
    #calculcate the number of times a label occurs in at least one method, and return sum over all labels
    union_count = sum(max(counter1[k], counter2[k]) for k in counter1.keys() | counter2.keys())
    
    if union_count == 0:
        return 0
    return intersection_count / union_count

#Turn functions into tokens for TF-IDF processing by looking for variables/keywords, then numbers, then operators
def tokenize_code(code: str) -> str:
    tokens = re.findall(
        r"[A-Za-z_]\w+|"       
        r"\d+|"                 
        r"==|!=|<=|>=|&&|\|\||" 
        r"[{}();.,+\-*/%=<>]",  
        code
    )
    return " ".join(tokens)

#Use TF-IDF to compare vectorized tokens
def compute_function_similarity(function_dict):
    tokenized = {name: tokenize_code(code)
                 for name, code in function_dict.items()}

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(tokenized.values())

    similarity_matrix = cosine_similarity(tfidf)

    names = list(function_dict.keys())
    return names, similarity_matrix

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")

    #Finds all functions and returns name and node labels
    records, summary, keys = driver.execute_query("""
    MATCH (f:FunctionDeclaration)-[:AST*]->(n)
    WHERE NOT f.name STARTS WITH 'std::'                                            
    RETURN f.name AS method, f.code AS code, collect(labels(n)) AS astTypes
    """,
    database_="neo4j",
    )


    
    functions = {}
    call_graph = {}
    function_code_dict = {}  

    #Go through all functions and store AST info in dictionary by metjhod name
    for record in records:
        labels = []
        method_name = record["method"]
        code_text = record.get("code")
        if code_text:
            function_code_dict[method_name] = code_text

        for sublist in record["astTypes"]:
            for label in sublist:
                labels.append(label)
        functions[record["method"]] = labels

    names, tfidf_matrix = compute_function_similarity(function_code_dict)

    assigned = set()
    adjacency = defaultdict(set) 
    similarities = {}

    for i, f1 in enumerate(names):
        for j, f2 in enumerate(names):
            if i >= j:
                continue
            jaccard_score = multiset_jaccard(functions[f1], functions[f2])
            tfidf_score = tfidf_matrix[i, j] if tfidf_matrix is not None else 0

            similarities[(f1, f2)] = (jaccard_score, tfidf_score)
    adjacency = defaultdict(set)

    #group together functions with high degree of similarity
    for (f1, f2), (jaccard_score, tfidf_score) in similarities.items():
        if jaccard_score >= 0.5 and tfidf_score >= 0.5: #values can be adjusted as needed
            adjacency[f1].add(f2)
            adjacency[f2].add(f1)
    visited = set()
    groups = {}
    group_id = 0
    def dfs(node, group_id):
        visited.add(node)
        groups[node] = group_id
        for neighbor in adjacency[node]:
            if neighbor not in visited:
                dfs(neighbor, group_id)

    #if function has no group, return it under group: -1
    for func in names:
        if func not in visited:
            if adjacency[func]: 
                dfs(func, group_id)
                group_id += 1
            else:  
                groups[func] = -1
                visited.add(func)


    with driver.session() as session:
        # Write group IDs
        for func, gid in groups.items():
            session.run(
                """
                MATCH (f:FunctionDeclaration {name: $name})
                SET f.group = $gid
                """,
                name=func,
                gid=gid
            )
        # Write similarity edges
        for (f1, f2), (jaccard_score, tfidf_score) in similarities.items():
            if f2 in adjacency[f1]:
                session.run(
                    """
                    MATCH (a:FunctionDeclaration {name: $f1}),
                        (b:FunctionDeclaration {name: $f2})
                    MERGE (a)-[r:SIMILAR_TO]->(b)
                    SET r.jaccard = $j, r.tfidf = $t
                    """,
                    f1=f1,
                    f2=f2,
                    j=jaccard_score,
                    t=tfidf_score
                )
                       

    # Summary information
    """  print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after
    ))"""
