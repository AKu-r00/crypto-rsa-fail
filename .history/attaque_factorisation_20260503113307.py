from mon_rsa import generer_cles, chiffrer

def factorisation_naive(n):
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            return p, n // p
    return None, None

def attaque_factorisation(pub):
    e, n = pub
    p, q = factorisation_naive(n)
    if p is None:
        return None
    phi = (p - 1) * (q - 1)
    from mon_rsa import inverse_modulaire
    d = inverse_modulaire(e, phi)
    return d

def test_factorisation():
    print("\n" + "="*50)
    print("ATTAQUE 2: FACTORISATION NAIVE")
    print("="*50)
    
    p, q = 61, 53
    pub, priv = generer_cles(p, q, e=17)
    e, n = pub
    
    M = 65
    C = chiffrer(M, e, n)
    print(f"Message chiffre: {C}")
    
    d = attaque_factorisation(pub)
    if d:
        from mon_rsa import dechiffrer
        M_recupere = dechiffrer(C, d, n)
        if M_recupere == M:
            print(f"ATTAQUE REUSSIE! Cle privee trouvee: d={d}")
            return True
    print(f"ATTAQUE ECHOUEE")
    return False