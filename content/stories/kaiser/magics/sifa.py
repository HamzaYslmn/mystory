"""sifa.py — Sifa (Medical). Enerji basina doku onarimi.
Enerji tek basina yetmez (#14): yeni doku KUTLE ister, mana kutle yapamaz (E=mc^2),
o yuzden beden KENDI biyokutlesinden (yag, su, besin) harcar. Ac bedeni iyilestirmek
cok yavas; fazla iyilestirme hastayi eritir. Asagidaki sadece enerji butcesi."""
from __init__ import Devre

E_DOKU = 5000.0   # J/g, doku onarim maliyeti — STIPULATED (yanma ~17-20 kJ/g, yeniden-kullanimla kesri)

def sifa(d):
    """gram = E / e_doku. Ekler (§6); kendine agrisiz, yabanci beden akan manayi zorla re-spin eder -> yanar."""
    return d.is_j() / E_DOKU

if __name__ == "__main__":
    # 72 g fiziksel %100 ideali; cizili cihaz recine tavani %80 -> ~58 g
    assert abs(sifa(Devre(100, 1.0)) - 57.6) < 2
    print(round(sifa(Devre(100, 1.0))), "g cihaz (%80); 72 g ideal")
