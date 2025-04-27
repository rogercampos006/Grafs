import networkx as nx
import random
from collections import Counter

G = nx.Graph()

def build_lastgraph():
    G = nx.Graph()
    # Obrim el fitxer d'arestes i llegim les dades
    with open('lastfm_asia_edges.csv', 'r') as f:
        next(f)  # Saltem la capçalera
        for linia in f:
            node1, node2 = linia.strip().split(',')
            G.add_edge(node1, node2)  # Afegim aresta al graf
    return G

def simulate_coincidence(m,s):
    G = build_lastgraph()
    # Assignem pesos aleatoris a les arestes
    for x, y in G.edges():
        pes = random.gauss(m, s)  # Generació de pes amb distribució normal
        pes = max(0, min(pes, 1))  # Trunquem valors entre 0 i 1
        G [x][y]['pes'] = round(pes, 3)  # Arrodonim a 3 decimals
    
    return G

def  how_many_cliques(n,m,s):
    G = simulate_coincidence(m, s)
    H = nx.Graph()
    # Creem subgraf amb arestes de pes superior a n
    for u, v, data in G.edges(data = True):
        if G [u][v] ['pes'] > n:
            H.add_edge (u, v)
    # Comptem mida de cliques trobades
    cliques = list(nx.find_cliques(H))
    comptador = Counter(len(c) for c in cliques)
    return comptador

# Tasca 2. Simulador de loteria
def obtenir_intents(n,m):
    combinacio_guanyadora = []
    # Demanem números a l'usuari amb validació
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
    
    # Simulem intents fins a encertar
    combinacio = []
    intents = 0
    while (set(combinacio) != set(combinacio_guanyadora)):
        combinacio = random.sample(range(1, m+1), n)  # Generació combinació aleatòria
        intents +=1
    return intents

def loto ():
    try:
        n = -1
        m = 3
        # Validació entrada d'usauri
        while (not 0<n<=m):
            n = int(input("Introdueix la quantitat de números a triar: "))
            m = int(input("Introdueix el rang màxim de números: "))
        intents = obtenir_intents (n, m)
        print("S'han necessitat", intents, "intents per guanyar la loteria")
    except ValueError:
        print("Error: Introdueix valors numèrics vàlids.")
    
loto ()

# Tasca 3. Experiment de coloració de grafs
import time

# Configuració de l'experiment
strategies = ['largest_first', 'random_sequential', 'smallest_last', 
              'independent_set', 'connected_sequential_bfs', 
              'connected_sequential_dfs', 'saturation_largest_first']
sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
results = {}

# Executem l'experiment per diferents mides
for size in sizes:
    print(f"\nProcessant subgraf de mida: {size}")
    results[size] = {}
    try:
        # Creem subgraf amb les primeres 'size' arestes
        subgraph = nx.Graph(list(G.edges())[:size])
        print(f"Subgraf creat: {subgraph.number_of_nodes()} nodes, {subgraph.number_of_edges()} arestes")
        
        # Proves amb diferents estratègies de coloració
        for strategy in strategies:
            print(f"  Executant estratègia: {strategy}")
            times = []
            colors = []
            # Fem 5 execucions per estratègia
            for i in range(5):
                start = time.time()
                coloring = nx.coloring.greedy_color(subgraph, strategy=strategy)
                times.append(time.time() - start)  # Mesurem temps execució
                colors.append(max(coloring.values()) + 1)  # Comptem colors utilitzats
            # Emmagatzemem resultats
            results[size][strategy] = {
                'avg_time': sum(times) / len(times),
                'avg_colors': sum(colors) / len(colors)
            }
            print(f"    Temps mitjà: {results[size][strategy]['avg_time']:.4f} segons, Colors mitjans: {results[size][strategy]['avg_colors']}")
    except Exception as e:
        print(f"Error processant mida {size}: {e}")
        continue

# Resultats finals de l'experiment
print("\nResultats finals:")
for size in results:
    print(f"\nMida: {size}")
    for strategy in results[size]:
        print(f"  {strategy}: Temps mitjà = {results[size][strategy]['avg_time']:.4f} s, Colors mitjans = {results[size][strategy]['avg_colors']}")
print("\nFi de l'execució")
