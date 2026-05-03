import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mon_rsa import generer_cles

def factorisation_naive(n):
    debut = time.time()
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            temps = time.time() - debut
            return p, n // p, temps
    return None, None, time.time() - debut

def test_analyse():
    print("\n" + "="*50)
    print("ANALYSE: TEMPS DE FACTORISATION")
    print("="*50)
    
    donnees = []
    for p, q in [(61, 53), (101, 107), (151, 157), (191, 193)]:
        pub, _ = generer_cles(p, q, 17)
        _, n = pub
        pfactor, qfactor, temps = factorisation_naive(n)
        print(f"n={n}, temps={temps:.4f}s")
        donnees.append((n, temps))
    
    ns, ts = zip(*donnees)
    plt.figure(figsize=(10, 6))
    plt.plot(ns, ts, 'bo-')
    plt.xlabel('n')
    plt.ylabel('Temps (s)')
    plt.title('Temps de factorisation naive en fonction de n')
    plt.grid(True)
    plt.savefig('analyse.png')
    print("Graphique sauvegarde dans analyse.png")
    return True