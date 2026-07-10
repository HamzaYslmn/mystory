"""kuvvet.py — Kuvvet/mermi (Projection). Is-enerji + momentum korunumu."""
import math
from __init__ import Devre

def ke(m, v):
    """Kinetik enerji: E = 1/2 m v^2 [J]. (1/2 tam; W = int F dx = int m v dv.)"""
    return 0.5 * m * v ** 2

def hiz(E, m):
    """ke'nin tersi: v = sqrt(2 E / m) [m/s]."""
    return math.sqrt(2 * E / m)

def momentum(m, v):
    """Geri tepme: p = m v [kg m/s] (Newton III; buyuye -p biner)."""
    return m * v

def kuvvet(d, kg):
    """(hiz, geri tepme). Temas (§6): bu bir mermi, hedefe konan mana degil."""
    v = hiz(d.is_j(), kg)
    return v, momentum(kg, v)

def guclendir(taban_j, d):
    """Silah guclendirme (§13): mana KE'si taban vurusa eklenir. Vurus_j = taban + is_j();
    geri tepme momentum() ile yaya/kola biner. Sade ok ~49 J, guclendirilmis kJ'lere cikar."""
    return taban_j + d.is_j()

if __name__ == "__main__":
    assert hiz(ke(2, 3), 2) == 3                        # forward o inverse: E(v=3) -> v=3
    assert abs(Devre(100, 0.2).is_j() - 72000) < 100    # 72 kJ @20% (doc §21)
    assert guclendir(49, Devre(100, 0.2)) == 49 + 72000 # sade ok + eklenen KE
    print(round(kuvvet(Devre(100, 0.2), 0.2)[0]), "m/s;", round(guclendir(49, Devre(100, 0.02))), "J guclu ok")
