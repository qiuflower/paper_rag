# utils/kg_builder.py
from rdflib import Graph, Namespace, URIRef, Literal, RDF
import re
from core.config import KG_FILE

class KnowledgeGraph:
    def __init__(self):
        self.graph = Graph()
        self.ns = Namespace("http://example.org/")

    def add_relation(self, subject, relation, obj):
        s = URIRef(self.ns[subject.replace(" ", "_")])
        p = URIRef(self.ns[relation.replace(" ", "_")])
        o = URIRef(self.ns[obj.replace(" ", "_")])
        self.graph.add((s, p, o))

    def extract_triples(self, text):
        # 简化：通过正则找 "[实体] 是 [实体]" 的结构
        triples = re.findall(r"(\w+)\s+是\s+(\w+)", text)
        for s, o in triples:
            self.add_relation(s, "is", o)

    def save(self):
        self.graph.serialize(KG_FILE, format="turtle")
