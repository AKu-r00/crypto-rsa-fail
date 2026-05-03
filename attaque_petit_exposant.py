from mon_rsa import chiffrer, generer_cles

def attaque_racine_cubique(C, n):
    C = int(C)
    n = int(n)
    cube = round(C ** (1/3))
    for m in range(max(0, cube-10), cube+10):
        if pow(m, 3, n) == C:
            return m
    return None

def test_petit_exposant():
    print("\n" + "="*50)
    print("ATTAQUE 1: RACINE CUBIQUE (e=3)")
    print("="*50)
    
    p, q = 53, 59
    pub, priv = generer_cles(p, q, e=3)
    e, n = pub
    d, _ = priv
    
    M = 10
    C = chiffrer(M, e, n)
    print(f"Message chiffre: {C}")
    
    M_recupere = attaque_racine_cubique(C, n)
    if M_recupere == M:
        print(f"ATTAQUE REUSSIE! Message retrouve: {M_recupere}")
        return True
    else:
        print(f"ATTAQUE ECHOUEE")
        return False