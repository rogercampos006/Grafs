import networkx as nx
import random

G = nx.Graph()

def build_lastgraph():
    G = nx.Graph()
    with open('lastfm_asia_edges.csv', 'r') as f:
        next(f)
        for linia in f:
            node1, node2 = linia.strip().split(',')
            G.add_edge(node1, node2)
    return G

def bfs(G):  
    v = next(iter(G.nodes()))  # Agafem un node qualsevol per començar
    Q = [v]  # Cua per gestionar els nodes pendents
    state = {node: 0 for node in G.nodes()}  # 0 = no visitat, 1 = visitat
    state[v] = 1  # Marquem el primer node com a visitat
    
    llista_llistes = [[v]]  # Primera capa amb el node inicial
    
    while Q:  
        nivell = []  # Llista per al següent nivell
        for _ in range(len(Q)):  # Iterem sobre tots els elements actuals de la cua
            w = Q.pop(0)  # Traiem el primer de la cua
            for u in G.neighbors(w):  # Per cada veí del node actual
                if state[u] == 0:  # Si encara no l'hem visitat
                    Q.append(u)  # Afegim el veí a la cua
                    state[u] = 1  # El marquem com a visitat
                    nivell.append(u)  # L'afegim a la llista del nivell actual
        if nivell:  # Només afegim nivells no buits
            llista_llistes.append(nivell)
    
    return llista_llistes


# Generem el graf 
G = build_lastgraph()

# Executem BFS sobre el graf
desglossament_nivells = bfs(G)
print(desglossament_nivells)


def dfs(G):  
    v = next(iter(G.nodes()))  # Agafem un node qualsevol per començar
    Q = [v]  # Cua per gestionar els nodes pendents
    state = {node: 0 for node in G.nodes()}  # 0 = no visitat, 1 = visitat
    state[v] = 1  # Marquem el primer node com a visitat
    
    llista_llistes = [[v]]  # Primera capa amb el node inicial
    
    while Q:  
        nivell = []  # Llista per al següent nivell
        for _ in range(len(Q)):  # Iterem sobre tots els elements actuals de la cua
            w = Q.pop()  # Traiem el primer de la cua
            for u in G.neighbors(w):  # Per cada veí del node actual
                if state[u] == 0:  # Si encara no l'hem visitat
                    Q.append(u)  # Afegim el veí a la cua
                    state[u] = 1  # El marquem com a visitat
                    nivell.append(u)  # L'afegim a la llista del nivell actual
        if nivell:  # Només afegim nivells no buits
            llista_llistes.append(nivell)
    
    return llista_llistes


def experiment_resilient(G, num_intents=100):
    ll_nodes_eliminats = []  # Llista per emmagatzemar el nombre de nodes eliminats per prova
        
    for intent in range(num_intents):
        G_copia = G.copy()
        nodes = list(G_copia.nodes())
        nodes_eliminats = 0
            
            # Eliminar nodes mentre hi hagi nodes i només 1 component
        while nodes and nx.number_connected_components(G_copia) == 1:
                node_eliminar = random.choice(nodes)
                G_copia.remove_node(node_eliminar)  # Eliminar node, no aresta
                nodes.remove(node_eliminar)  # Actualitzar la llista de nodes
                nodes_eliminats += 1
            
            # Si hem aconseguit 2 components, guardem el nombre de nodes eliminats
        if nx.number_connected_components(G_copia) > 1:
                ll_nodes_eliminats.append(nodes_eliminats)
        
    # Calcular la mitjana
    avg_nodes_eliminats = sum(ll_nodes_eliminats) / len(ll_nodes_eliminats) if ll_nodes_eliminats else 0
            
    print(f"Nombre de proves: {num_intents}")
    print(f"Mitjana de nodes eliminats: {avg_nodes_eliminats:.2f}")
     
print(experiment_resilient(G, 100))

"""

G = nx.Graph()
G2 = nx.DiGraph()


def create_graph_1():
    G.add_node(1,2,3,4,5)
    G.add_nodes_from([(1,{'nom': 'charles'})], [(2,{'nom': 'jake'})], (3,{'nom': 'amy'}), (4,{'nom': 'raymond'}), (5,{'nom': 'gina'}))
    G.add_edges_from([(1, 2), (1, 5), (5,3), (3,2), (2,4)])

def create_graph_2():
    G2.add_node()
    G2.add_node(1,2,3, 5, 6, 10, 20)
    G2.add_nodes_from([(1,{'aparell':'servidor'})], [(2, {'aparell':'ordinador'})], [(3, {'aparell':'memòria'})], [(5, {'aparell':'altaveus'})], [(6, {'aparell':'altaveus'})], [(10, {'aparell':'mòbil'})], [(20, {'aparell':'impressora'})])

"""
G = nx.Graph()

import time

# Generem el graf 
G = build_lastgraph()

temps_inici = time.time()
bfs(G)
temps_final = time.time()
print(f"Temps de funcio bfs: {temps_final - temps_inici} segons")
# Generem el graf 
G = build_lastgraph()

temps_inici = time.time()
dfs(G)
temps_final = time.time()
print(f"Temps de funcio dfs: {temps_final - temps_inici} segons")

#Experiment



def dividir_graf_eliminant_node(G):
    
    punts_articulacio = list(nx.articulation_points(G))# Trobar tots els punts d'articulació del graf

    if punts_articulacio:
        node_a_eliminar = punts_articulacio[0]# Si hi ha punts d'articulació, eliminar el primer trobat

        G.remove_node(node_a_eliminar)
        print(f"S'ha eliminat el node {node_a_eliminar} (punt d'articulació) per dividir el graf.")
    # Comprovar si el graf ara té dues components
    if nx.number_connected_components(G)>1:
        print("El graf s'ha dividit en dues o més components connexes.")
    else:
        print("El graf encara té una sola component connexa.")

    return G

G = dividir_graf_eliminant_node(G)
