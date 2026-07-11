"""magics/__init__.py — buyu kurali: bir buyu = nesneye cizilen mana devresi.
Kanit, adli sabitler + adim fonksiyonlari olarak; yasa her fonksiyonun docstring'inde.
Atik = (1-verim) payi -> HAM MANA olarak dagilir (isi degil; doc §1).
"""
J_PER_WH = 3600.0    # 1 Wh = 1 W * 3600 s (birim tanimi, tam)
IDEAL_LM_W = 300.0   # beyaz isik isiksal etkinligi [lm/W]; turetme: isik.py
DEVRE_VERIM_TAVAN = 0.80  # Bornmulleriana recine direnci: hicbir cizili devre %80'i asmaz

class Devre:
    """Cizili mana devresi. Etki enerjisi E = mana_Wh * J_PER_WH * verim [J]."""
    def __init__(self, mana_wh, kalite=0.6, uzunluk=1.0, altlik=1.0):
        self.mana_wh, self.kalite, self.uzunluk, self.altlik = float(mana_wh), kalite, uzunluk, altlik

    def _direnc(self):
        """Seri 'kablo direnci': uzun iz mana kaybeder. 1/(1+0.15(L-1)); 0.15 tuning, kanon degil."""
        return 1.0 / (1 + 0.15 * (self.uzunluk - 1))

    def verim(self):
        """eta = min(%80, kalite * altlik * direnc). Altlik kaybi azaltir; enerji eklemez (§9)."""
        return min(DEVRE_VERIM_TAVAN, self.kalite * self.altlik * self._direnc())

    def is_j(self):   return self.mana_wh * J_PER_WH * self.verim()   # etki enerjisi [J]
    def is_wh(self):  return self.mana_wh * self.verim()              # [Wh]

if __name__ == "__main__":
    assert J_PER_WH == 3600                                   # 1 Wh = 3600 J
    assert Devre(100, 1.0, altlik=2.0).verim() == DEVRE_VERIM_TAVAN  # recine tavani asilmaz
    assert abs(Devre(100, 0.2).is_j() - 72000) < 100          # %20 -> 72 kJ
    print("kurallar ok")
