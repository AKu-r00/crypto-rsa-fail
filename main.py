from mon_rsa import generer_cles, chiffrer, dechiffrer, inverse_modulaire
from attaque_petit_exposant import test_petit_exposant
from attaque_factorisation import test_factorisation
from broadcast_attack import test_broadcast_attack
from padding import test_padding
from analyse import test_analyse
from attaque_petit_exposant import attaque_racine_cubique
from attaque_factorisation import factorisation_naive
from broadcast_attack import crt
import math

print("="*60)
print("PROJET CRYPTOGRAPHIE RSA - ATTAQUES ET VULNERABILITES")
print("="*60)

M = int(input("Entrez un nombre a chiffrer : "))

print("\n" + "="*60)
print("[PARTIE 1] GENERATION DE CLES RSA (vulnerable)")
print("="*60)

p, q, e = 99023, 99053, 17
n = p * q
phi = (p - 1) * (q - 1)
d = inverse_modulaire(e, phi)

print("=== GENERATION DES CLES RSA ===")
print(f"Etape 1 : Choisir deux premiers  -> p={p}, q={q}")
print(f"Etape 2 : Calculer n             -> n = p x q = {n}")
print(f"Etape 3 : Calculer phi(n)        -> phi = (p-1)(q-1) = {phi}")
print(f"Etape 4 : Choisir e              -> e={e}, pgcd(e,phi)={math.gcd(e,phi)} OK")
print(f"Etape 5 : Calculer d             -> d = inverse(e, phi) = {d}")
print(f"Cle publique  -> (e={e},  n={n})")
print(f"Cle privee    -> (d={d}, n={n})")
print("================================")

pub, priv = (e, n), (d, n)

print("\n" + "="*60)
print("[PARTIE 2] CHIFFREMENT DU MESSAGE")
print("="*60)

C = pow(M, e, n)

print("=== CHIFFREMENT DU MESSAGE ===")
print(f"Etape 1 : Message saisi          -> M = {M}")
print(f"Etape 2 : Cle publique utilisee  -> e={e}, n={n}")
print(f"Etape 3 : Formule                -> C = M^e mod n")
print(f"Etape 4 : Calcul                 -> C = {M}^{e} mod {n}")
print(f"Etape 5 : Resultat               -> C = {C}")
print("==============================")

M_verify = pow(C, d, n)
print("\n=== VERIFICATION DECHIFFREMENT ===")
print(f"Etape 1 : Chiffre recu           -> C = {C}")
print(f"Etape 2 : Cle privee utilisee    -> d={d}, n={n}")
print(f"Etape 3 : Formule                -> M = C^d mod n")
print(f"Etape 4 : Calcul                 -> M = {C}^{d} mod {n}")
print(f"Etape 5 : Resultat               -> M = {M_verify} {'OK' if M_verify == M else 'FAILED'}")
print("==================================")

print("\n" + "="*60)
print("[PARTIE 3] ATTAQUE RACINE CUBIQUE (e petit)")
print("="*50)

M_cube = M ** 3
p1, q1 = 1500007, 1500019
n1 = p1 * q1

if M_cube >= n1:
    print(f"ATTENTION: M^3 = {M_cube} >= n = {n1}")
    print("Condition non remplie, attaque impossible pour ce M")
    print("Cette attaque fonctionne uniquement si M est petit")
    print(f"Exemple qui marche : M=7 -> 7^3=343 < n")
    M1 = None
else:
    e1 = 3
    C1 = pow(M, e1, n1)
    M1 = attaque_racine_cubique(C1, n1)
    print(f"n={n1}, C={C1}")
    print(f"Attaque 1 (petit exposant) -> M retrouve = {M1}")

print("\n" + "="*60)
print("[PARTIE 4] ATTAQUE PAR FACTORISATION")
print("="*50)

p2, q2, e2 = 99023, 99053, 17
n2 = p2 * q2
C2 = pow(M, e2, n2)
p_factor, q_factor = factorisation_naive(n2)
phi2 = (p_factor - 1) * (q_factor - 1)
d_recup = inverse_modulaire(e2, phi2)
M2 = pow(C2, d_recup, n2)
print(f"n={n2}, C={C2}")
print(f"Attaque 2 (factorisation)  -> M retrouve = {M2}")

print("\n" + "="*60)
print("[PARTIE 5] ATTAQUE BROADCAST (CRT)")
print("="*50)

p_bc1, q_bc1 = 1299709, 1299721
p_bc2, q_bc2 = 1299743, 1299763
p_bc3, q_bc3 = 1299791, 1299811

n_bc = [p_bc1*q_bc1, p_bc2*q_bc2, p_bc3*q_bc3]
C_vals = []
for n in n_bc:
    C_val = pow(M, 3, n)
    C_vals.append(C_val)
    print(f"n={n}, C={C_val}")

M3 = None
M_reconstruct = crt(C_vals, n_bc)
if M_reconstruct:
    M3 = round(M_reconstruct ** (1/3))
    print(f"M^3 reconstruct = {M_reconstruct}")
print(f"Attaque 3 (broadcast)      -> M retourne = {M3}")

print("\n" + "="*60)
print("[PARTIE 6] COMPARAISON PADDING")
print("="*50)
test_padding()

print("\n" + "="*60)
print("[PARTIE 7] ANALYSE GRAPHIQUE")
print("="*50)
test_analyse()

print("\n" + "="*60)
print("RESUME FINAL")
print("="*60)
print(f"Message original    : {M}")
print(f"Attaque 1 (petit exposant) : {'OK' if M1 == M else 'ECHEC'}")
print(f"Attaque 2 (factorisation)   : {'OK' if M2 == M else 'ECHEC'}")
print(f"Attaque 3 (broadcast)      : {'OK' if M3 == M else 'ECHEC'}")
print("\nProjet execute avec succes!")