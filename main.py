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

p, q, e = 61, 53, 17
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

pub1, priv1 = generer_cles(99023, 99053, 3)
e1, n1 = pub1
C1 = chiffrer(M, e1, n1)
M1 = attaque_racine_cubique(C1, n1)
print(f"n={n1}, C={C1}")
print(f"Attaque 1 (petit exposant) -> M retrouve = {M1}")

print("\n" + "="*60)
print("[PARTIE 4] ATTAQUE PAR FACTORISATION")
print("="*50)

pub2, priv2 = generer_cles(61, 53, 17)
e2, n2 = pub2
C2 = chiffrer(M, e2, n2)
p, q = factorisation_naive(n2)
phi = (p-1)*(q-1)
d_recup = inverse_modulaire(e2, phi)
M2 = dechiffrer(C2, d_recup, n2)
print(f"n={n2}, C={C2}")
print(f"Attaque 2 (factorisation)  -> M retrouve = {M2}")

print("\n" + "="*60)
print("[PARTIE 5] ATTAQUE BROADCAST (CRT)")
print("="*50)

pairs = [
    generer_cles(99017, 99023, 3),
    generer_cles(99017, 99053, 3),
    generer_cles(99023, 99053, 3),
]
n_vals = []
C_vals = []
for pub, _ in pairs:
    e, n = pub
    n_vals.append(n)
    C_val = pow(M, 3, n)
    C_vals.append(C_val)
    print(f"n={n}, C={C_val}")

M3 = None
M_reconstruct = crt(C_vals, n_vals)
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