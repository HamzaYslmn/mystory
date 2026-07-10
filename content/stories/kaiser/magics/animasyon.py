"""animasyon.py — Animasyon fizik faturasi (§13). Iki fatura: KAS + CPU.
Komut katmani robot.py'de; burasi hareketin ne kadara mal oldugu.
Ders: basit tekrar bedava, dengede duran biped pahali — CPU faturasi hizli buyur.
"""
from __init__ import Devre

def tork(yuk_N, kol_m):
    """Eklem torku: tau = yuk * kol [N m] (tau = F r)."""
    return yuk_N * kol_m

def eklem_gucu(tau, omega):
    """Mekanik guc: P = tau * omega [W]."""
    return tau * omega

def kas_gucu(tau, omega, duty=1.0, verim=0.6):
    """Aktuator cekisi: P_kas = tau omega * duty / verim [W] (§13: * duty / verimlilik)."""
    return eklem_gucu(tau, omega) * duty / verim

def cpu_yuku(dof, dongu_hz, duyu):
    """Koordinasyon faturasi (goreli): DOF * dongu-hizi * algi. Basit tekrar ~1, biped devasa."""
    return dof * dongu_hz * duyu

def calisma_suresi(d, P_kas):
    """Kac saat calisir: t = E / P_kas [saat]. is_wh() = verimden sonra."""
    return d.is_wh() / P_kas

if __name__ == "__main__":
    assert tork(50, 0.3) == 15 and eklem_gucu(15, 2) == 30           # deger tanimlari
    ogutucu = cpu_yuku(1, 1, 1); biped = cpu_yuku(12, 100, 3)
    assert biped > ogutucu * 1000                                    # biped CPU faturasi devasa
    P = kas_gucu(tork(50, 0.3), 2, duty=0.8)                         # tas kol degirmen
    print(round(calisma_suresi(Devre(100, 0.5), P), 1), "saat ogutur; biped/ogutucu CPU:", biped)
