from neo4j import GraphDatabase

def fetch_metrics():
    uri = "bolt://localhost:7687"
    auth = ("neo4j", "password")
    driver = GraphDatabase.driver(uri, auth=auth)
    
    query = """
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
    """
    
    with driver.session() as session:
        result = session.run(query)
        data = [row for row in result]
    
    driver.close()
    return data

def save_markdown(data):
    md_content = "| Component | Fan-in | Fan-out | Instability |\n|---|---|---|---|\n"
    for row in data:
        md_content += f"| {row['Component']} | {row['fanIn']} | {row['fanOut']} | {row['instability']:.2f} |\n"
    
    with open("stability_metrics.md", "w") as f:
        f.write(md_content)

data = fetch_metrics()
save_markdown(data)
