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
    for x, y in G.edges():
        pes = random.gauss(m, s)
        pes = max(0, min(pes, 1))
        G [x][y]['pes'] = round(pes, 3)
    
    return G

def  how_many_cliques(n,m,s):
    G = simulate_coincidence(m, s)
    H = nx.Graph()
    for u, v, data in G.edges(data = True):
        if G [u][v] ['pes'] > n:
            H.add_edge (u, v)
    cliques = list(nx.find_cliques(H))
    comptador = Counter(len(c) for c in cliques)
    return comptador
