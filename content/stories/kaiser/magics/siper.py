"""siper.py — Ward (savusturma). Tehdit enerjileri 1/2 m v^2'den turetilir."""
from __init__ import Devre

def ke(m, v):  return 0.5 * m * v ** 2   # 1/2 m v^2 [J]

OK     = ke(0.020, 70)    # ~49 J    (20 g ok, 70 m/s)
KURSUN = ke(0.008, 350)   # ~490 J   (9mm)
TUFEK  = ke(0.004, 940)   # ~1767 J  (tufek); agir kalibre ~3 kJ

def guclendirilmis(taban_j, mana_wh, verim=0.2):
    """Guclendirilmis tehdit: taban + eklenen KE (saldirgan da mana harcar, §13).
    Tehdit sabit degil -> ward bir BUTCE dellosu: E_ward, saldiriya dokulen manayla yarisir."""
    return taban_j + mana_wh * 3600 * verim

def siper(d, tehdit_j=OK):
    """Kac vurus savusturur: n = E / E_tehdit. tehdit_j sade ya da guclendirilmis olabilir."""
    return d.is_j() / tehdit_j

if __name__ == "__main__":
    assert abs(OK - 49) < 1 and abs(KURSUN - 490) < 5   # balistikten
    assert siper(Devre(100, 0.4)) > 1000
    guc = guclendirilmis(OK, 1)                          # +1 Wh KE @20% -> ~769 J
    assert siper(Devre(100, 0.4), guc) < siper(Devre(100, 0.4)) / 10   # guclendirme sayiyi cokertir
    print(round(siper(Devre(100, 0.4))), "sade ok /", round(siper(Devre(100, 0.4), guc)), "guclu ok")
