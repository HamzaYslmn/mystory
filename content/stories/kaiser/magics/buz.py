"""buz.py — Buz/dondurma (Alteration). Kaba dokum vs kompresor (Kaiser'in hilesi)."""
from __init__ import Devre

C_SU = 4180.0     # J/(kg K), su (bkz. isi.py)
L_ERIME = 3.34e5  # J/kg, suyun erime/donma gizli isisi @0C (olculmus)

def cikan_isi(m, dT=20.0):
    """Bir kutle suyu dondurmak icin cikarilacak isi: Q = m c dT + m L_erime [J]."""
    return m * C_SU * dT + m * L_ERIME

def carnot_cop(T_c=273.0, T_h=293.0):
    """Sogutma Carnot tavani: COP_max = T_c/(T_h-T_c). 273/293 K -> 13.6 (ideal)."""
    return T_c / (T_h - T_c)

def buz(d, cop=1.0, dT=20.0):
    """Kac kg dondurur: m = E * cop / cikan_isi(1). cop=1 kaba dokum, cop~3 kompresor (< Carnot)."""
    return d.is_j() * cop / cikan_isi(1, dT)

if __name__ == "__main__":
    assert abs(carnot_cop() - 13.65) < 0.1 and carnot_cop() > 3   # gercek cop=3 << ideal tavan
    assert abs(buz(Devre(100, 1.0), 1) - 0.69) < 0.05           # %80 cizili kaba
    assert abs(buz(Devre(100, 1.0), 3) - 2.07) < 0.1            # %80 cizili kompresor
    print(round(buz(Devre(100, 1.0), 1), 2), "/", round(buz(Devre(100, 1.0), 3), 2),
          "kg cihaz (%80); ideal 0.86 / 2.59 kg")
