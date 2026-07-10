"""ses.py — Ses (Projection, §17). Akustik guc -> SPL(dB), kureyle ters-kare.
Ders: enerji olarak ses UCUZ; bir ciglik neredeyse bedava, ama sadece gurultu — is yapmaz.
"""
import math
from __init__ import Devre

I0 = 1e-12   # W/m^2, isitme esigi referans siddeti (SI; 0 dB burada tanimli)

def yayilma_yogunlugu(P, r):
    """Kureye yayilan siddet: I = P / (4 pi r^2) [W/m^2]. (Kabuk alani 4 pi r^2.)"""
    return P / (4 * math.pi * r ** 2)

def spl_db(I, I0=I0):
    """Ses basinc seviyesi: SPL = 10 log10(I / I0) [dB]. Mesafe 2x -> -6.02 dB."""
    return 10 * math.log10(I / I0)

def ses(d, r_m=10.0, sure_s=1.0):
    """r'de kac dB: P = E/t, sonra yayilma + dB. is_j() = verimden sonraki akustik enerji."""
    P = d.is_j() / sure_s
    return spl_db(yayilma_yogunlugu(P, r_m))

if __name__ == "__main__":
    assert abs(spl_db(I0)) < 1e-9                                      # referansta 0 dB
    P = 100.0                                                          # ters-kare: 2x mesafe = -6 dB
    assert abs(spl_db(yayilma_yogunlugu(P, 2)) - spl_db(yayilma_yogunlugu(P, 1)) + 6.02) < 0.02
    print(round(ses(Devre(100, 0.5))), "dB @10 m")
