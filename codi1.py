import networkx as nx
import random
import time

def build_lastgraph():
    G = nx.Graph()  # Crear un graf no dirigit amb NetworkX
    with open('lastfm_asia_edges.csv', 'r') as f:  # Obrir el fitxer CSV amb les arestes
        next(f)  # Saltar la primera línia (capçalera)
        for linia in f:  # Iterar sobre cada línia del fitxer
            node1, node2 = linia.strip().split(',')  # Separar els dos nodes per la coma
            G.add_edge(node1, node2)  # Afegir una aresta entre node1 i node2
    return G  # Retornar el graf construït

def bfs(G):  
    v = next(iter(G.nodes()))  # Agafar un node qualsevol com a punt de partida
    Q = [v]  # Inicialitzar la cua amb el node inicial
    state = {node: 0 for node in G.nodes()}  # Crear diccionari: 0 = no visitat, 1 = visitat
    state[v] = 1  # Marcar el node inicial com a visitat
    
    llista_llistes = [[v]]  # Crear llista de llistes amb el node inicial com a primer nivell
    
    while Q:  # Mentre hi hagi nodes a la cua
        nivell = []  # Llista buida per emmagatzemar els nodes del següent nivell
        for _ in range(len(Q)):  # Iterar sobre tots els nodes actuals de la cua
            w = Q.pop(0)  # Treure el primer node de la cua (comportament FIFO per BFS)
            for u in G.neighbors(w):  # Explorar els veïns del node actual
                if state[u] == 0:  # Si el veí no ha estat visitat
                    Q.append(u)  # Afegir el veí a la cua
                    state[u] = 1  # Marcar-lo com a visitat
                    nivell.append(u)  # Afegir-lo al nivell actual
        if nivell:  # Si hi ha nodes al nivell, afegir-los a la llista de llistes
            llista_llistes.append(nivell)
    
    return llista_llistes  # Retornar els nodes organitzats per nivells

# Generem el graf 
G = build_lastgraph()  # Construir el graf a partir del fitxer CSV

# Executem BFS sobre el graf
desglossament_nivells = bfs(G)  # Executar BFS i obtenir els nivells
print(desglossament_nivells)  # Mostrar els nodes per nivells

def dfs(G):  
    v = next(iter(G.nodes()))  # Agafar un node qualsevol com a punt de partida
    Q = [v]  # Inicialitzar la pila amb el node inicial
    state = {node: 0 for node in G.nodes()}  # Crear diccionari: 0 = no visitat, 1 = visitat
    state[v] = 1  # Marcar el node inicial com a visitat
    
    llista_llistes = [[v]]  # Crear llista de llistes amb el node inicial com a primer nivell
    
    while Q:  # Mentre hi hagi nodes a la pila
        nivell = []  # Llista buida per emmagatzemar els nodes del següent nivell
        for _ in range(len(Q)):  # Iterar sobre tots els nodes actuals de la pila
            w = Q.pop()  # Treure l'últim node de la pila (comportament LIFO per DFS)
            for u in G.neighbors(w):  # Explorar els veïns del node actual
                if state[u] == 0:  # Si el veí no ha estat visitat
                    Q.append(u)  # Afegir el veí a la pila
                    state[u] = 1  # Marcar-lo com a visitat
                    nivell.append(u)  # Afegir-lo al nivell actual
        if nivell:  # Si hi ha nodes al nivell, afegir-los a la llista de llistes
            llista_llistes.append(nivell)
    
    return llista_llistes  # Retornar els nodes organitzats per "nivells" (segons DFS)

def experiment_resilient(G, num_intents=100):
    ll_nodes_eliminats = []  # Llista per guardar el nombre de nodes eliminats en cada prova
        
    for intent in range(num_intents):  # Repetir l'experiment 'num_intents' vegades
        G_copia = G.copy()  # Crear una còpia del graf per no modificar l'original
        nodes = list(G_copia.nodes())  # Llista de tots els nodes del graf
        nodes_eliminats = 0  # Comptador de nodes eliminats
            
        # Eliminar nodes mentre hi hagi nodes i només hi hagi 1 component connex
        while nodes and nx.number_connected_components(G_copia) == 1:
            node_eliminar = random.choice(nodes)  # Escollir un node aleatori per eliminar
            G_copia.remove_node(node_eliminar)  # Eliminar el node del graf
            nodes.remove(node_eliminar)  # Treure'l de la llista de nodes
            nodes_eliminats += 1  # Incrementar el comptador
            
        # Si el graf es divideix en més d'1 component, guardar el nombre de nodes eliminats
        if nx.number_connected_components(G_copia) > 1:
            ll_nodes_eliminats.append(nodes_eliminats)
        
    # Calcular la mitjana de nodes eliminats (si hi ha dades)
    avg_nodes_eliminats = sum(ll_nodes_eliminats) / len(ll_nodes_eliminats) if ll_nodes_eliminats else 0
            
    print(f"Nombre de proves: {num_intents}")  # Mostrar el nombre total de proves
    print(f"Mitjana de nodes eliminats: {avg_nodes_eliminats:.2f}")  # Mostrar la mitjana amb 2 decimals
     
experiment_resilient(G, 100)  # Executar l'experiment amb 100 intents

# Generem el graf 
G = build_lastgraph()  # Reconstruir el graf per a les proves de temps

temps_inici = time.time()  # Registrar el temps inicial
bfs(G)  # Executar BFS
temps_final = time.time()  # Registrar el temps final
print(f"Temps de funcio bfs: {temps_final - temps_inici} segons")  # Mostrar el temps d'execució

# Generem el graf 
G = build_lastgraph()  # Reconstruir el graf per a la prova de DFS

temps_inici = time.time()  # Registrar el temps inicial
dfs(G)  # Executar DFS
temps_final = time.time()  # Registrar el temps final
print(f"Temps de funcio dfs: {temps_final - temps_inici} segons")  # Mostrar el temps d'execució

# Experiment
def dividir_graf_eliminant_node(G):
    punts_articulacio = list(nx.articulation_points(G))  # Trobar tots els punts d'articulació del graf

    if punts_articulacio:  # Si hi ha algun punt d'articulació
        node_a_eliminar = punts_articulacio[0]  # Escollir el primer punt d'articulació trobat
        G.remove_node(node_a_eliminar)  # Eliminar aquest node del graf
        print(f"S'ha eliminat el node {node_a_eliminar} (punt d'articulació) per dividir el graf.")
    
    # Comprovar si el graf s'ha dividit en més d'una component connexa
    if nx.number_connected_components(G) > 1:
        print("El graf s'ha dividit en dues o més components connexes.")
    else:
        print("El graf encara té una sola component connexa.")

    return G  # Retornar el graf modificat

G = dividir_graf_eliminant_node(G)  # Executar la funció per dividir el graf
