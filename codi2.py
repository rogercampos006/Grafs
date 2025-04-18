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
