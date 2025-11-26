
import sys
print(sys.executable)

from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "00000000")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")

    records, summary, keys = driver.execute_query("""
     MATCH (f:FunctionDeclaration)-[:AST*]->(n)
    RETURN f.name AS method, collect(labels(n)) AS astTypes
    """,
    database_="neo4j",
)

    # Loop through results and do something with them
    for record in records:
        print(record.data())  # obtain record as dict

    print(type(record))
    # Summary information
    """  print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after
    ))"""
