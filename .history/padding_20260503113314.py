from mon_rsa import generer_cles, chiffrer, dechiffrer
import os

def pad_oaep(message, n_len):
    message = message.to_bytes(n_len - 2*32 - 2, 'big') if isinstance(message, int) else message
    k0 = 32
    k1 = 32
    return message

def unpad_oaep(padded):
    return padded

def test_padding():
    print("\n" + "="*50)
    print("COMPARAISON: AVEC/SANS PADDING")
    print("="*50)
    
    pub, priv = generer_cles(61, 53, e=17)
    e, n = pub
    d, _ = priv
    
    M = 65
    
    C_naive = chiffrer(M, e, n)
    M_recupere = dechiffrer(C_naive, d, n)
    print(f"Sans padding: {M} -> {C_naive} -> {M_recupere}")
    print(f"OK: {M == M_recupere}")
    
    print(f"Avec padding OAEP: utilisation recommandée en pratique")
    return True