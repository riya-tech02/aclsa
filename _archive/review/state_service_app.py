from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

graphs = {}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/state/initialize")
def initialize(user_id: str):
    graphs[user_id] = {"nodes": {}, "edges": []}
    return {"status": "success", "user_id": user_id}

@app.post("/state/node")
def add_node(data: dict):
    uid = data["user_id"]
    if uid not in graphs:
        graphs[uid] = {"nodes": {}, "edges": []}
    nid = f"{data['node_type']}_{len(graphs[uid]['nodes'])}"
    graphs[uid]["nodes"][nid] = {"node_id": nid, "node_type": data["node_type"], "attributes": data.get("attributes", {})}
    return {"node_id": nid}

@app.post("/state/query")
def query(data: dict):
    uid = data["user_id"]
    if uid not in graphs:
        return {"error": "Not found"}
    g = graphs[uid]
    nodes = list(g["nodes"].values())
    return {"user_id": uid, "nodes": nodes, "edges": [], "metadata": {"num_nodes": len(nodes), "num_edges": 0, "node_types": list(set(n["node_type"] for n in nodes)) if nodes else []}}
