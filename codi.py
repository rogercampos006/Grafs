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
