//Return function similarity
MATCH (f1:FunctionDeclaration)-[r:SIMILAR_TO]->(f2:FunctionDeclaration)
RETURN f1.name AS Function1, f2.name AS Function2, r.jaccard AS Jaccard, r.tfidf as TFIDF
ORDER BY Jaccard DESC
