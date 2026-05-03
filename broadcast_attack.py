from mon_rsa import generer_cles, chiffrer
import math

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def fuse_crt(x1, m1, x2, m2):
    g = math.gcd(m1, m2)
    if (x2 - x1) % g != 0:
        return None, 0
    lcm = m1 // g * m2
    p, q = m1 // g, m2 // g
    inv = modinv(p, q)
    if inv is None:
        return None, 0
    x = (x1 + m1 * (x2 - x1) // g * inv) % lcm
    return x, lcm

def crt(remainders, moduli):
    x, m = remainders[0], moduli[0]
    for i in range(1, len(remainders)):
        x, m = fuse_crt(x, m, remainders[i], moduli[i])
        if x is None:
            return None
    return x

def test_broadcast_attack():
    print("\n" + "="*50)
    print("ATTAQUE 3: BROADCAST (CRT)")
    print("="*50)
    
    M = 10
    
    pairs = [
        generer_cles(53, 59, 3),
        generer_cles(53, 71, 3),
        generer_cles(59, 71, 3),
    ]
    
    n_vals = []
    C_vals = []
    for pub, _ in pairs:
        e, n = pub
        n_vals.append(n)
        C = chiffrer(M, e, n)
        C_vals.append(C)
        print(f"n={n}, C={C}")
    
    M_reconstruct = crt(C_vals, n_vals)
    if M_reconstruct is None:
        print(f"ATTAQUE ECHOUEE")
        return False
    
    M_cube = round(M_reconstruct ** (1/3))
    
    if M_cube ** 3 == M_reconstruct:
        print(f"ATTAQUE REUSSIE! Message retrouve: {M_cube}")
        return True
    print(f"ATTAQUE ECHOUEE")
    return False