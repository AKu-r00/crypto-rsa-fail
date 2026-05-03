import math

def est_premier(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def inverse_modulaire(e, phi):
    # Algorithme d'Euclide étendu
    def euclide_etendu(a, b):
        if b == 0:
            return a, 1, 0
        g, x, y = euclide_etendu(b, a % b)
        return g, y, x - (a // b) * y

    g, x, _ = euclide_etendu(e, phi)
    if g != 1:
        raise ValueError("Inverse n'existe pas")
    return x % phi

def generer_cles(p, q, e):
    # Vérifications
    assert est_premier(p), "p n'est pas premier"
    assert est_premier(q), "q n'est pas premier"
    assert p != q, "p et q doivent être différents"

    n = p * q
    phi = (p - 1) * (q - 1)

    assert 1 < e < phi, "e invalide"
    assert math.gcd(e, phi) == 1, "e doit être premier avec phi(n)"

    d = inverse_modulaire(e, phi)

    print(f"n = {n}")
    print(f"phi(n) = {phi}")
    print(f"Clé publique  : (e={e}, n={n})")
    print(f"Clé privée    : (d={d}, n={n})")

    return (e, n), (d, n)

def chiffrer(M, e, n):
    assert M < n, "Message trop grand pour n"
    C = pow(M, e, n)
    print(f"Chiffrement : {M}^{e} mod {n} = {C}")
    return C

def dechiffrer(C, d, n):
    M = pow(C, d, n)
    print(f"Déchiffrement : {C}^{d} mod {n} = {M}")
    return M

# ── TEST ──
if __name__ == "__main__":
    pub, priv = generer_cles(p=61, q=53, e=17)
    e, n = pub
    d, _ = priv

    M = 65
    C = chiffrer(M, e, n)
    M2 = dechiffrer(C, d, n)

    print(f"\nMessage original    : {M}")
    print(f"Message déchiffré   : {M2}")
    print(f"Test OK             : {M == M2}")