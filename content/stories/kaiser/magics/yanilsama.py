"""yanilsama.py — Illusionism. Ortam parlakligini (lux) eslestirme."""
from __init__ import Devre, IDEAL_LM_W

def eslesme_gucu(lux, alan_m2, K=IDEAL_LM_W):
    """Ortami taklit icin gereken isik gucu: P = (lux/K)*alan [W]. ((lm/m^2)/(lm/W)*m^2 = W.)"""
    return lux / K * alan_m2

def yanilsama(d, lux=100000.0, alan_m2=1.0):
    """Kac saat tutar: t = E_isik / P. Ogle pahali, gece bedava; dokunusu/golgeyi tutamaz."""
    return d.is_wh() / eslesme_gucu(lux, alan_m2)

if __name__ == "__main__":
    assert yanilsama(Devre(100, 0.5), 100) > yanilsama(Devre(100, 0.5), 100000) * 100
    print(round(yanilsama(Devre(100, 0.5), 100)), "saat (gece)")
