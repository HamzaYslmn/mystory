"""isik.py — Isik buyusu (Projection). Isik akisi Phi_v = K * P_opt."""
from __init__ import Devre, IDEAL_LM_W

K_MAX = 683.0   # lm/W, 555 nm tepe isiksal etkinlik — kandelanin SI tanimi (tam ust sinir)

def optik_guc(lumen, K=IDEAL_LM_W):
    """Bir Phi_v lumeni surdurmek icin gereken optik guc: P = Phi_v / K [W]. (K <= K_MAX)"""
    return lumen / K

def isik(d, lumen=250):
    """Kac saat yanar: t = E_isik / P = (mana*eta) / (Phi_v/K) [Wh/W = saat]."""
    return d.is_wh() / optik_guc(lumen)

if __name__ == "__main__":
    assert optik_guc(683, K_MAX) == 1.0            # tanim: 683 lm @555nm = 1 W
    assert abs(isik(Devre(100, 0.05)) - 6) < 0.5   # ~6 saat @5% (doc §21)
    print(isik(Devre(100, 0.05)), "saat")
