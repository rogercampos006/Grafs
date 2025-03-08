import networkx as nx
import random


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

def build_lastgraph():
    with open ('lastfm_asia_edges.csv', 'r') as f:
        for linia in f:
            G.add_node(linia[0], linia[1])
            G.add_edges([(linia[0], linia[1])])

#Graf generat per realitzar proves
def generar_graf():
    G = nx.Graph()
    center = 0  # Node central
    corona1 = list(range(1, 11))  # Primera corona
    corona2 = list(range(11, 30))  # Segona corona
    
    # Connectem el centre amb la primera corona
    for node in corona1:
        G.add_edge(center, node)
    
    # Connectem la primera corona amb la segona
    for i, node in enumerate(corona2):
        G.add_edge(corona1[i % len(corona1)], node)
    
    return G


import networkx as nx

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
G = generar_graf()

# Executem BFS sobre el graf
desglossament_nivells = bfs(G)
print(desglossament_nivells)

import networkx as nx

def component_DFS(G):
    # Triem un node qualsevol per començar l'exploració
    v_inicial = next(iter(G.nodes))

    # Inicialitzem la pila i el conjunt de nodes visitats
    P = [v_inicial]  # Pila (LIFO)
    visitats = set()  # Conjunt per evitar repetir nodes
    llista_llistes = []  # Llista de nodes de la component

    while P:
        llista = []
        w = P.pop()  # Extreu l'últim node (DFS)
        if w not in visitats:
            visitats.add(w)
            llista.append(w)  # Afegim el node al resultat
            
            # Afegim els veïns que encara no hem visitat
            for u in G.neighbors(w):
                if u not in visitats :
                    P.append(u)
                    if u not in llista_llistes:
                        llista.append(u)
            llista_llistes.append(llista)
    return llista_llistes  # Retorna els nodes de la mateixa component connex



llista = component_DFS(G)
print(llista)
