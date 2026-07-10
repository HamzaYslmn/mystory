"""mercek.py — Duyu araci (Sensing, §13). Buyu degil optik: kizilotesini gorunure ceviren mercek.
Mana yalniz yukseltir; menzili aciklik + SNR belirler. Aktif ~menzil^4, pasif ~menzil^2.
"""
import math
from __init__ import Devre

H = 6.626e-34   # J s, Planck sabiti
C = 3.0e8       # m/s, isik hizi
RAYLEIGH = 1.22 # ilk Airy sifiri / pi -> dairesel aciklik ayirma sabiti

def foton_enerjisi(lamda):
    """Foton enerjisi: E = h c / lamda [J]. Upconversion: iki IR foton -> bir gorunur."""
    return H * C / lamda

def ayirma_gucu(lamda, D):
    """Acisal ayirma (Rayleigh): theta = 1.22 lamda / D [rad]. Buyuk aciklik = keskin goruntu."""
    return RAYLEIGH * lamda / D

def alinan_sinyal(P0, r, aktif=False):
    """Alinan sinyal: pasif ~1/r^2 (kaynaktan), aktif ~1/r^4 (gidis-donus iki kez ters-kare)."""
    return P0 / r ** (4 if aktif else 2)

def snr(sinyal, gurultu):
    """Sinyal/gurultu; algilama icin > 1 gerek — bu, menzilin gercek tabani."""
    return sinyal / gurultu

if __name__ == "__main__":
    assert abs(foton_enerjisi(750e-9) - 2 * foton_enerjisi(1500e-9)) < 1e-30   # 2 IR = 1 gorunur
    assert ayirma_gucu(500e-9, 0.1) < ayirma_gucu(500e-9, 0.01)                # buyuk D keskin
    assert abs(alinan_sinyal(1, 10, True) - alinan_sinyal(1, 10) / 100) < 1e-12 # aktif r^2 kat duser
    print(round(ayirma_gucu(500e-9, 0.05) * 1e6, 1), "mrad ayirma; aktif/pasif menzil cezasi r^2")
