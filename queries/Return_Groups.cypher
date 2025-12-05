//Return Groups
MATCH (f:FunctionDeclaration)
WHERE NOT f.name STARTS WITH 'std::'
RETURN f.group AS GroupID, collect(f.name) AS Functions
ORDER BY GroupID
