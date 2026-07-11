"""irklar.py — Peoples (Races). Balance canon for docs/races.md.
Three magic axes: capacity (Wh), throughput (x capacity -> W), aptitude.
Capacity is TRAINED up to a born ceiling (§2); numbers below are those ceilings.
Flesh caps the draw: no mortal channels much past ~1 kW (power-system §16).
Design law: stronger magic -> fewer, longer-lived, slower to replace.
A mortal is skilled-but-low-fuel; a crystal-beast is crude-but-high-fuel."""

MORTAL_CEIL_W = 1000.0   # body channel ceiling (§16); ~1 kW, the hardest burst a mortal throws

# ad: (kap_yaygin_wh, kap_zirve_wh, debi_max_x, omur_yil, nufus_sira)  kap = egitimli tavan
# nufus_sira 1 = en kalabalik
IRKLAR = {
    "elf":      (75.0, 300.0, 3.0, 500, 4),   # kapasite ustasi: tum elfler buyucu, zirve arsimaj
    "cuce":     (10.0, 200.0, 5.0, 250, 3),   # debi/burst ustasi: kucuk rezerv, sert cikis, aletler
    "insan":    (10.0, 100.0, 2.0,  75, 2),   # denge: cikis ~= kapasite, her yerde, nadir dahi
    "beastman": ( 5.0,  15.0, 1.0,  55, 1),   # beden ustasi: az mana, sadece beden guclendirme
}

# buyu ogrenimi (#5): kim ogrenir. elf dogustan egitimli (hepsi), cuce yetenekli,
# beastman avlanirken ogrenir; insan ciftci -> ogretmen az, ~%20'si basit bir numara
# ogrenir (ates yakma, kisa sureli isik). "koyumuze bir gezgin buyucu ogretmisti".
CASTER_ORAN = {"elf": 1.00, "cuce": 0.90, "beastman": 0.70, "insan": 0.20}

# regen (#1,#2): herkes kendi rezervini ~24 saatte doldurur (yemek/hava/uyku) = ~%4/saat.
# NEFES teknigi (egitimli): ~%10/saat -> baz regeni ~2x'ler, iyilesme suresi yariya
#   (rezerv dolumu + kendini-sifa ayni manaya bagli). Muharebe olceginde hala sifir.
# Hizli yol: iksirler + Ocak Kanli (ayakta Mist-kanali, §20).
BAZ_REGEN_ORAN   = 1/24    # dogal: tam rezerv 24 saatte (kapasitenin ~%4'u/saat)
NEFES_REGEN_ORAN = 0.10    # egitimli nefes: kapasitenin ~%10'u/saat

def cikis_w(kap_wh, debi_x):
    """Zirve surdurulebilir cikis = kapasite * debi carpani [W]."""
    return kap_wh * debi_x

if __name__ == "__main__":
    # imza ciktilari (races.md soz verdikleri)
    assert cikis_w(300, 3.0) == 900          # elf zirve ~900 W, tavana yakin
    assert cikis_w(200, 5.0) == 1000         # cuce usta = tavan, en sert burst
    assert cikis_w(10, 1.0) == 10            # yaygin insan ~10 W, cikis ~= kapasite
    # hicbir olumlu beden tavanini asamaz
    for ad, (kc, kz, dx, omur, nuf) in IRKLAR.items():
        assert cikis_w(kz, dx) <= MORTAL_CEIL_W + 1e-9, ad
    # denge defteri: guclu buyu -> az nufus (buyuk sira sayisi) VE uzun omur
    sira = sorted(IRKLAR, key=lambda a: IRKLAR[a][1], reverse=True)   # zirve kapasiteye gore
    assert sira == ["elf", "cuce", "insan", "beastman"]              # buyu gucu sirasi
    assert [IRKLAR[a][4] for a in sira] == [4, 3, 2, 1]              # nufus tam ters
    assert [IRKLAR[a][3] for a in sira] == [500, 250, 75, 55]       # omur de azalan
    # skilled-but-low-fuel: kanli kurdun 30 kWh kristali yaygin cucenin 10 Wh rezervini eritir
    assert 30_000 / 10 == 3000               # ~3000x yakit; kurt gucte ezer, cuce hunerde yener
    # buyu ogrenimi (#5): insan en dusuk (ciftci, ogretmen yok), elf hepsi
    assert CASTER_ORAN["insan"] == 0.20 and CASTER_ORAN["elf"] == 1.00
    assert min(CASTER_ORAN, key=CASTER_ORAN.get) == "insan"
    # nefes teknigi baz regeni ~2x'ler (10 Wh insan: 24 saat -> ~10 saat)
    assert 2 < NEFES_REGEN_ORAN / BAZ_REGEN_ORAN < 3
    print("irklar OK: elf 900W(kap300) cuce 1000W(kap200) insan 10W(kap10) beastman 15W(beden);",
          "tavan", int(MORTAL_CEIL_W), "W; guc sirasi elf>cuce>insan>beastman == nufus ters;",
          "caster orani insan %20 - elf %100")
