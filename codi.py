import networkx as nx

"""

G = nx.Graph() G2 = nx.DiGraph()

def create_graph_1(): G.add_node(1,2,3,4,5) G.add_nodes_from([(1,{'nom': 'charles'})], [(2,{'nom': 'jake'})], (3,{'nom': 'amy'}), (4,{'nom': 'raymond'}), (5,{'nom': 'gina'})) G.add_edges_from([(1, 2), (1, 5), (5,3), (3,2), (2,4)])

def create_graph_2(): G2.add_node() G2.add_node(1,2,3, 5, 6, 10, 20) G2.add_nodes_from([(1,{'aparell':'servidor'})], [(2, {'aparell':'ordinador'})], [(3, {'aparell':'memòria'})], [(5, {'aparell':'altaveus'})], [(6, {'aparell':'altaveus'})], [(10, {'aparell':'mòbil'})], [(20, {'aparell':'impressora'})])

""" G = nx.Graph()

def build_lastgraph(): with open ('lastfm_asia_edges.csv', 'r') as f: for linia in f: G.add_node(linia[0], linia[1]) G.add_edges([(linia[0], linia[1])])

def bfs(G):
v = next(iter(G.nodes())) # Agafem un node qualsevol per començar Q = [v] # Cua per gestionar els nodes pendents R = [v] # Llista de nodes visitats
