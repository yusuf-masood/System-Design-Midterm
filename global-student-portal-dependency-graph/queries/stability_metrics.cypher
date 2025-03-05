MATCH (c:Component)
OPTIONAL MATCH (c)<-[:DEPENDS_ON]-(incoming)
WITH c, count(incoming) AS fanIn
OPTIONAL MATCH (c)-[:DEPENDS_ON]->(outgoing)
WITH c, fanIn, count(outgoing) AS fanOut
WITH c, fanIn, fanOut, 
     CASE WHEN (fanIn + fanOut) = 0 THEN 0 
          ELSE toFloat(fanOut) / (fanIn + fanOut) END AS instability
RETURN c.name AS Component, fanIn, fanOut, instability
ORDER BY instability DESC;
