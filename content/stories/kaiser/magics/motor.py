"""motor.py — It-cek motoru (Motive power, §13). Mana -> donme. TORK adim adim, fonksiyonlarla.

Turetme (her adim asagida bir fonksiyon; ozdeslikler __main__'de sayisal dogrulanir):
  tork tanimi -> krank-biyel anlik tork -> strok isi (integral) -> ortalama tork -> guc.
"""
import math
from __init__ import Devre  # debi tabanli; enerji butcesi icin de import

def tork_anlik(F, r, theta):
    """tau = r x F  ->  F r sin(theta) [N m]. Dik kol = r sin(theta) (paralelkenar alani)."""
    return F * r * math.sin(theta)

def is_strok(F, r):
    """Bir strok isi: W = int_0^pi tau dtheta = 2 F r = F s (s=2r) [J]. (Biyel terimi nete katkisiz.)"""
    return 2 * F * r

def tork_ort(W_cevrim):
    """Ortalama tork (devirde 1 guc stroku): tau_ort = W / (2 pi) [N m]."""
    return W_cevrim / (2 * math.pi)

def omega(rpm):
    """Aci hizi: omega = 2 pi N / 60 [rad/s]."""
    return 2 * math.pi * rpm / 60

def saft_gucu(P_mana_W, eta=0.6, eta_m=0.6):
    """P_saft = P_mana * eta * eta_m [W]. eta_m = krank/volan/zamanlama (Kaiser'in kenari)."""
    return P_mana_W * eta * eta_m

if __name__ == "__main__":
    F, r = 100.0, 0.1
    assert tork_anlik(F, r, math.pi / 2) == F * r                       # 1) tepe tork = F r
    n = 10000                                                          # 2) integral = strok isi
    integral = sum(tork_anlik(F, r, math.pi * i / n) for i in range(n)) * (math.pi / n)
    assert abs(integral - is_strok(F, r)) < 1e-3
    W = is_strok(F, r)                                                 # 3) P = tau_ort * omega
    assert abs(tork_ort(W) * omega(600) - W * 600 / 60) < 1e-9
    assert saft_gucu(100) < 75                   # mavi 100 W: yarim insan gucunden az, cart assist
    assert 500 < saft_gucu(2000) < 1000         # kurt moru 2 kW: at sinifi, ama cok pahali
    print(round(saft_gucu(100), 1), "W mavi-assist;", round(saft_gucu(2000)), "W mor;",
          round(tork_ort(is_strok(1000, 0.1)), 2), "N m")
