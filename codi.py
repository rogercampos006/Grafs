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
        
    return avg_nodes_eliminats
      
print(experiment_resilient(G, 100))
