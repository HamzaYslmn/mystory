"""elektrik.py — Elektrik (Projection, §17). P = V*I; olduren akim; hava arki.
Ders: sok enerjisi ucuz; asil fatura yuksek gerilim / arki atlatmaktir, joule degil.
NOT: bu dunyada elektrik KESFEDILMEMIS; her sey dogrudan buyuyle yapilir. Kaiser'in gizli kozu (§23).
"""
from __init__ import Devre

KALP_ESIK_A  = 0.1     # A, kalpten ~100 mA fibrilasyon/olum (~10-100 mA araligi)
HAVA_DELINME = 3e6     # V/m, havanin dielektrik delinmesi (~3 MV/m)

def guc(V, I):
    """Elektrik gucu: P = V I [W]."""
    return V * I

def ark_gerilimi(bosluk_m, E=HAVA_DELINME):
    """Boslugu atlatmak icin gerilim: V = E * d [V]. 1 cm hava -> ~30 kV."""
    return E * bosluk_m

def oldurucu(I):
    """Akim kalp esigini geciyor mu (>= ~100 mA)."""
    return I >= KALP_ESIK_A

def elektrik(d, V=1000.0, I=KALP_ESIK_A):
    """(V,I) yuku kac saniye surer: t = E / (V I). is_j() = verimden sonraki enerji."""
    return d.is_j() / guc(V, I)

if __name__ == "__main__":
    assert ark_gerilimi(0.01) == 30000 and oldurucu(0.1) and not oldurucu(0.005)
    assert abs(elektrik(Devre(100, 0.5)) * guc(1000, 0.1) - Devre(100, 0.5).is_j()) < 1  # t*P = E
    print(round(elektrik(Devre(100, 0.5))), "s olduren sok; ark 1cm:", round(ark_gerilimi(0.01)), "V")
