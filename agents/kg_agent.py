# agents/kg_agent.py
import networkx as nx
from rdflib import Graph

class KGAgent:
    def __init__(self, rdf_path):
        self.graph = Graph()
        self.graph.parse(rdf_path, format="ttl")
        self.nx_graph = self._to_networkx()

    def _to_networkx(self):
        G = nx.DiGraph()
        for s, p, o in self.graph:
            G.add_edge(str(s), str(o), predicate=str(p))
        return G

    def query_neighbors(self, entity, depth=1):
        """
        返回 entity 周围邻居节点，depth 控制跳数
        """
        if entity not in self.nx_graph:
            return []
        neighbors = nx.single_source_shortest_path_length(self.nx_graph, entity, cutoff=depth)
        return list(neighbors.keys())

if __name__ == "__main__":
    kg = KGAgent("kg_store/graph.ttl")
    print(kg.query_neighbors("http://example.org/entity/某实体"))
