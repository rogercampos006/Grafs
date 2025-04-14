import networkx as nx
import random
from collections import Counter

G = nx.Graph()

def build_lastgraph():
    G = nx.Graph()
    with open('lastfm_asia_edges.csv', 'r') as f:
        next(f)
        for linia in f:
            node1, node2 = linia.strip().split(',')
            G.add_edge(node1, node2)
    return G

def simulate_coincidence(m,s):
    G = build_lastgraph()
    arestes = list(G.edges())
    for x, y in arestes:
        pes = random.gauss(m, s)
        pes = max(0, min(pes, 1))
        G [x] [y] ['pes'] = round(pes, 3)
    
    return G

def  how_many_cliques(n,m,s):
    G = simulate_coincidence(m, s)
    H = nx.Graph()
    for u, v in G.nodes():
        if G [u][v] ['pes'] > n:
            H.add_edge ([u], [v])
    cliques = list(nx.find_cliques(H))
    comptador = Counter(len(c) for c in cliques)
    return comptador
