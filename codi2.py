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

#Tasca 2. La loto n<m

def obtenir_intents(n,m):
    combinacio_guanyadora = []
    while len(combinacio_guanyadora) < n:
        try:
            num = int(input(f"Introdueix el número {len(combinacio_guanyadora)+1}: "))
            if num < 1 or num > m:
                print(f"El número ha d'estar entre 1 i {m}.")
            elif num in combinacio_guanyadora:
                print("No pot haver-hi números duplicats.")
            else:
                combinacio_guanyadora.append(num)
        except ValueError:
            print("Introdueix un número vàlid.")
    combinacio = []
    intents = 0
    while (set(combinacio) != set(combinacio_guanyadora)):
        combinacio = []
        combinacio = random.sample(range(1, m+1), n)
        intents +=1
    return intents

def loto ():
    try:
        n = -1
        m = 3
        while (not 0<n<=m):
            n = int(input("Introdueix la quantitat de números a triar: "))
            m = int(input("Introdueix el rang màxim de números: "))
        intents = obtenir_intents (n, m)
        print("S'han necessitat", intents, "intents per guanyar la loteria")
    except ValueError:
        print("Error: Introdueix valors numèrics vàlids.")
    
loto ()

#Tasca 3. Experiment

import networkx as nx
import time

# Funció per construir el graf
def build_lastgraph():
    G = nx.Graph()
    try:
        with open('lastfm_asia_edges.csv', 'r') as f:
            next(f)  # Saltem la capçalera
            for linia in f:
                linia = linia.strip()
                if not linia:  # Ignorem línies buides
                    continue
                try:
                    node1, node2 = linia.split(',')
                    G.add_edge(node1, node2)
                except ValueError as e:
                    print(f"Error processant línia: {linia}. Error: {e}")
                    continue
        print(f"Graf construït: {G.number_of_nodes()} nodes, {G.number_of_edges()} arestes")
        return G
    except FileNotFoundError:
        print("Error: No s'ha trobat el fitxer 'lastfm_asia_edges.csv'")
        return nx.Graph()
    except Exception as e:
        print(f"Error inesperat en construir el graf: {e}")
        return nx.Graph()

# Construïm el graf
G = build_lastgraph()

# Comprovem si el graf té arestes
if G.number_of_edges() == 0:
    print("Error: El graf està buit. Comprova el fitxer 'lastfm_asia_edges.csv'.")
    exit()

# Configuració de l'experiment
strategies = ['largest_first', 'random_sequential', 'smallest_last', 
              'independent_set', 'connected_sequential_bfs', 
              'connected_sequential_dfs', 'saturation_largest_first']
sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
results = {}

# Executem l'experiment
for size in sizes:
    print(f"\nProcessant subgraf de mida: {size}")
    results[size] = {}
    try:
        subgraph = nx.Graph(list(G.edges())[:size])
        print(f"Subgraf creat: {subgraph.number_of_nodes()} nodes, {subgraph.number_of_edges()} arestes")
        for strategy in strategies:
            print(f"  Executant estratègia: {strategy}")
            times = []
            colors = []
            for i in range(5):
                start = time.time()
                coloring = nx.coloring.greedy_color(subgraph, strategy=strategy)
                times.append(time.time() - start)
                colors.append(max(coloring.values()) + 1)
            results[size][strategy] = {
                'avg_time': sum(times) / len(times),
                'avg_colors': sum(colors) / len(colors)
            }
            print(f"    Temps mitjà: {results[size][strategy]['avg_time']:.4f} segons, Colors mitjans: {results[size][strategy]['avg_colors']}")
    except Exception as e:
        print(f"Error processant mida {size}: {e}")
        continue

# Mostrem els resultats finals
print("\nResultats finals:")
for size in results:
    print(f"\nMida: {size}")
    for strategy in results[size]:
        print(f"  {strategy}: Temps mitjà = {results[size][strategy]['avg_time']:.4f} s, Colors mitjans = {results[size][strategy]['avg_colors']}")
print("\nFi de l'execució")
