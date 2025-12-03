
import sys
print(sys.executable)

from neo4j import GraphDatabase
from itertools import combinations

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "00000000")

#Jaccard index measured by |A int. B| / |A union B|
def find_jaccard_similarity(set1, set2):
    set_intersection = set1.intersection(set2)
    set_union = set1.union(set2)
    if not set_union:
        return 0
    return len(set_intersection) / len(set_union)

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
        functions[record["method"]] = set(labels)
    print(functions.get("countA"))


    #look at every non-identical pair of functions and return those with Jaccard similiarty score greater than 0.5
    for f1, f2 in combinations(functions.keys(), 2):
            sim = find_jaccard_similarity(functions[f1], functions[f2])
            if sim > 0.5:  # threshold for "high similarity"
                print(f"{f1} ~ {f2}: {sim:.2f}")

    # Summary information
    """  print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after
    ))"""
