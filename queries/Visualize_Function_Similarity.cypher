//Visualize Function Similarity
MATCH (f1:FunctionDeclaration)-[r:SIMILAR_TO]->(f2:FunctionDeclaration)
WHERE (r.jaccard >= 0.7 OR r.tfidf >= 0.8) 
  AND NOT f1.name STARTS WITH 'std::'
  AND NOT f2.name STARTS WITH 'std::'
RETURN f1, f2, r
LIMIT 50

