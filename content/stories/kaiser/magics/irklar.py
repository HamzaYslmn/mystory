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
    "insan":    (10.0, 100.0, 1.0,  75, 2),   # denge: cikis ~= kapasite, her yerde, nadir dahi
    "beastman": ( 5.0,  15.0, 1.0,  55, 1),   # beden ustasi: az mana, sadece beden guclendirme
}

# Kapasite egitimle olcekler (#3): irksal TABAN (1x) -> egitimli 2-3x -> usta 5-10x -> nadir prodigy >10x.
# Taban her irkin dogustan zemini. Elf hepsi dogustan egitimli, o yuzden "yaygin"i (75) zaten egitimli
# tier; cuce/insan/beastman'de "yaygin" = egitimsiz taban. Rezervuar beastman'in yetenegi degil: ustasi yok.
BAZ_KAPASITE = {"elf": 30.0, "cuce": 10.0, "insan": 10.0, "beastman": 5.0}
EGITIM_CARP  = (2, 3)     # egitimli kapasite = taban * 2-3
USTA_CARP    = (5, 10)    # usta kapasite = taban * 5-10; bir iki kisi (prodigy) bunu da asar

# Affinite turleri: cekirdek merdivenin DISINDA (kapasite_sirasi assert'ine girmez). Tek alanda ~%100
# verim, gerisinde siradan; denge: dar alan + cografi kilit + kisa omur/az sayi.
# Synthora: KOLONI. Birey ~5 W (en zayif caster). Echo-kristali muzigiyle ayri castleri FAZA KILITLER:
# mana aktarimi YOK (§6 kapali beden); etkiler ust uste biner. §11 faz-cakismasini muzikle cozen tek halk.
SYNTHORA_BIREY_W = 5.0     # tek synthoranin dogustan debisi
SYNTHORA_BEDEN   = 12      # normal "beden" ~12 birey (ahtapot dokunacli)
SYNTHORA_KRAL    = 500     # kral = ~500 bireyin devasa fuzyonu, kimildamaz
SYNTHORA_ALAN    = "ses"   # ~%100 verim alani (muzik, ses taklidi, enstruman)

# buyu ogrenimi (#5): kim ogrenir. elf dogustan egitimli (hepsi), cuce yetenekli,
# beastman avlanirken ogrenir; insan ciftci -> ogretmen az, ~%20'si basit bir numara
# ogrenir (ates yakma, kisa sureli isik). "koyumuze bir gezgin buyucu ogretmisti".
CASTER_ORAN = {"elf": 1.00, "cuce": 0.90, "beastman": 0.70, "insan": 0.20}

# Demografi: (erginlik, ortalama kusak, erginlige_ulasan_cocuk).
# Omur tek basina nufus uretmez; docs/races.md "Demographic rules" ile ayni sabitler.
DEMOGRAFI = {
    "elf":      (50, 125, 2.1),
    "cuce":     (30,  65, 2.4),
    "insan":    (17,  27, 3.0),
    "beastman": (13,  20, 4.2),
}
ARCHMAGE_ORAN = 0.001       # elflerin yaklasik binde biri 300 Wh+
UZMANLIK_YUVASI = (2, 3)    # zihin girisimi: cogu kisi 2-3 disiplinde ustalik tutar

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
    # Kapasite sirasi yalniz bireysel depoyu anlatir; toplumsal guc nufus, oran ve verimi de ister.
    kapasite_sirasi = sorted(IRKLAR, key=lambda a: IRKLAR[a][1], reverse=True)
    assert kapasite_sirasi == ["elf", "cuce", "insan", "beastman"]
    assert [DEMOGRAFI[a][1] for a in kapasite_sirasi] == [125, 65, 27, 20]
    assert ARCHMAGE_ORAN == 1/1000 and UZMANLIK_YUVASI == (2, 3)
    # kapasite tier'leri (#3): elf hepsi egitimli -> "yaygin" = egitimli tier (2-3x taban)
    assert EGITIM_CARP[0] <= IRKLAR["elf"][0] / BAZ_KAPASITE["elf"] <= EGITIM_CARP[1]   # 75/30 = 2.5x
    for a in ("cuce", "insan", "beastman"):       # digerlerinde yaygin = egitimsiz taban (1x)
        assert IRKLAR[a][0] == BAZ_KAPASITE[a]
    for a in ("elf", "cuce", "insan"):            # rezervuar irklarinda zirve usta-ustu (>=5x taban)
        assert IRKLAR[a][1] / BAZ_KAPASITE[a] >= USTA_CARP[0]        # elf 10x, cuce 20x, insan 10x
    assert IRKLAR["beastman"][1] / BAZ_KAPASITE["beastman"] <= EGITIM_CARP[1]   # 15/5=3x: beastman ustasi yok
    # Synthora (affinite/koloni): eszamanli cikis = birey_sayisi * birey_W (mana havuzu DEGIL, faz-kilit)
    assert SYNTHORA_BEDEN * SYNTHORA_BIREY_W == 60            # 12'lik beden ~60 W
    assert SYNTHORA_KRAL * SYNTHORA_BIREY_W == 2500           # kral ~2.5 kW eszamanli ses
    assert SYNTHORA_BIREY_W <= MORTAL_CEIL_W                  # her birey tek basina tavanin cok altinda (yasal)
    assert SYNTHORA_KRAL * SYNTHORA_BIREY_W > MORTAL_CEIL_W   # koloni toplami tavani asar — sayiyla, tek bedenle degil
    # skilled-but-low-fuel: kanli kurdun 30 kWh kristali yaygin cucenin 10 Wh rezervini eritir
    assert 30_000 / 10 == 3000               # ~3000x yakit; kurt gucte ezer, cuce hunerde yener
    # buyu ogrenimi (#5): insan en dusuk (ciftci, ogretmen yok), elf hepsi
    assert CASTER_ORAN["insan"] == 0.20 and CASTER_ORAN["elf"] == 1.00
    assert min(CASTER_ORAN, key=CASTER_ORAN.get) == "insan"
    # nefes teknigi baz regeni ~2x'ler (10 Wh insan: 24 saat -> ~10 saat)
    assert 2 < NEFES_REGEN_ORAN / BAZ_REGEN_ORAN < 3
    print("irklar OK: elf 900W(kap300) cuce 1000W(kap200) insan 10W(kap10) beastman 15W(beden);",
          "tavan", int(MORTAL_CEIL_W), "W; archmage binde 1; uzmanlik 2-3;",
          "caster orani insan %20 - elf %100")
    print("kapasite tier: taban 1x -> egitim 2-3x -> usta 5-10x -> prodigy >10x;",
          "taban elf30/cuce10/insan10/beastman5 Wh")
    print("Synthora (affinite/koloni): birey", int(SYNTHORA_BIREY_W), "W; beden", SYNTHORA_BEDEN,
          "~60W; kral", SYNTHORA_KRAL, "~2.5kW ses (faz-kilit, mana havuzu degil); alan", SYNTHORA_ALAN)
