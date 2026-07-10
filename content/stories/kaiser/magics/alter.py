"""alter.py — Alterasyon kes/deforme (§13). Cansiz maddeyi buk/kes/kir.
Erime/faz isi.py & buz.py'de; buradaki yeni fizik: plastik is ve kirilma yuzey enerjisi.
Ders: kucuk yuk tasiyan noktada calis — hacim bedeli acimasiz.
"""
from __init__ import Devre

CELIK_AKMA = 250e6   # Pa (=J/m^3), yumusak celik akma gerilmesi
GAMMA_CAM  = 10.0    # J/m^2, cam kirilma enerjisi (yeni yuzey basina)

def deformasyon_isi(akma_pa, hacim_m3, gerinim=1.0):
    """Plastik is: W = sigma * gerinim * V [J]. gerinim=1 ust sinir (tam akma)."""
    return akma_pa * gerinim * hacim_m3

def kirilma_isi(gamma, alan_m2):
    """Kirma maliyeti: W = gamma * yeni-yuzey-alani [J]. Ince kesik ucuz; ez pahali."""
    return gamma * alan_m2

def deforme_hacim(d, akma_pa=CELIK_AKMA, gerinim=0.1):
    """Butcenin buktugu hacim: V = E / (sigma * gerinim) [m^3]. is_j() = verimden sonra."""
    return d.is_j() / (akma_pa * gerinim)

if __name__ == "__main__":
    assert deformasyon_isi(250e6, 1e-3, 1.0) == 250000           # 1 L celigi tam ak: 250 kJ
    V = deforme_hacim(Devre(100, 0.5))                           # ters: V*sigma*gerinim = E
    assert abs(V * CELIK_AKMA * 0.1 - Devre(100, 0.5).is_j()) < 1
    assert kirilma_isi(GAMMA_CAM, 1e-4) < deformasyon_isi(CELIK_AKMA, 1e-4, 0.1)  # kesmek < ezmek
    print(round(deforme_hacim(Devre(100, 0.5)) * 1e6), "cm^3 celik buker (%10 gerinim)")
