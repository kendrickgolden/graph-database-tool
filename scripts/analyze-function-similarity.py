
import sys
print(sys.executable)

from neo4j import GraphDatabase
from itertools import combinations
from collections import Counter

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


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")

    #Finds all functions and returns name and node labels
    records, summary, keys = driver.execute_query("""
     MATCH (f:FunctionDeclaration)-[:AST*]->(n)
    RETURN f.name AS method, collect(labels(n)) AS astTypes
    """,
    database_="neo4j",
)


    #Go through all functions and store AST info in dictionary by metjhod name
    functions = {}
    
    for record in records:
        labels = []
        for sublist in record["astTypes"]:
            for label in sublist:
                labels.append(label)
        functions[record["method"]] = labels
    print(functions.get("countA"))


    #look at every non-identical pair of functions and return those with Jaccard similiarty score greater than 0.5
    for f1, f2 in combinations(functions.keys(), 2):
            sim = multiset_jaccard(functions[f1], functions[f2])
            if sim >= 0.0:  # threshold for "high similarity"
                print(f"{f1} ~ {f2}: {sim:.2f}")

    # Summary information
    """  print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after
    ))"""
