"""isi.py — Isi buyusu (Projection/Alteration). Kalorimetri: Q = m c dT (+ gizli isi)."""
from __init__ import Devre

C_SU = 4186.0      # J/(kg K), suyun ozgul isisi — kalori tanimi (1 cal ~ 4.186 J/g/K)
L_BUHAR = 2.257e6  # J/kg, suyun buharlasma gizli isisi @100C 1atm (olculmus)

def duyulur_isi(m, dT):
    """Faz degismeden isitma enerjisi: Q = m c dT [J]."""
    return m * C_SU * dT

def buhar_maliyeti(m, T0=20.0):
    """m kg suyu buhara cevirme: duyulur (100'e cikar) + gizli (buharlastir) [J]."""
    return m * C_SU * (100 - T0) + m * L_BUHAR

def isit(d, kg):
    """kutle_kg maddeyi kac derece isitir: dT = E / (m c)  (duyulur_isi'nin tersi)."""
    return d.is_j() / (kg * C_SU)

def kaynat(d, T0=20.0):
    """Kac ml buhar: m = E / (c(100-T0) + L_buhar)  (buhar_maliyeti'nin tersi), *1000 -> ml."""
    return d.is_j() / (C_SU * (100 - T0) + L_BUHAR) * 1000

if __name__ == "__main__":
    assert duyulur_isi(1, 1) == C_SU                                  # 1 kg'i 1 K = c
    m = kaynat(Devre(100, 1.0)) / 1000
    assert abs(buhar_maliyeti(m) - Devre(100, 1.0).is_j()) < 1        # forward o inverse = E
    assert abs(kaynat(Devre(100, 1.0)) - 140) < 10                    # ~140 ml @100% (doc §21)
    print(round(kaynat(Devre(100, 1.0))), "ml buhar")
