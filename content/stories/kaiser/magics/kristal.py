"""kristal.py — Mana tasi (Storage crystal, §18). TEK KULLANIMLIK; sarj YOK.
Curume var: raftaki tas bile YAVAS SIZAR (#11, surekli talep) -> RAF_SIZINTI_AYLIK.
Iki tur: MAVI maden (~1 kWh/5 cm3 KUP, dusuk cikis) ve MOR biyolojik (yogun, yuksek cikis, canlidan).
CIKIS yuzey alaniyla, KAPASITE hacimle orantili -> buyuk tas: buyuk akim + buyuk kapasite.
KESMEK cikisi artirir ama kapasiteyi dusurur (#13, yeni yuzey + islerken sarj kacar) -> kes_cikis_kapasite.
Recine iletkenin DIRENCI var: verim mesafeyle duser, en iyi kozak ~%80 (#6) -> recine_verim.
Bedensel guclendirme %1 verimle calisir (§14) -> feats pahalidir, kristali eritir.
Cok fazlasini seri/paralel baglamak frekansi bozar (§11) -> patlar.
"""
import math

WH_PER_CM3        = 200.0   # mavi maden yogunlugu: 1 kWh / 5 cm3
K_CIKIS_MAVI      = 7.08    # W / cm2 yuzey (5 cm3 tas -> 100 W'tan turetildi)
HAM_W             = 5.0     # BAGLI ham tasin zayif kullanilabilir cikisi; raf sizintisi degildir
RAF_SIZINTI_AYLIK = 0.05    # BAGLANTISIZ iyi tas ayda ~%5 sizar; kalite/hasar bunu degistirir
KESIM_CARPAN      = 2.0     # #13: tasi kes -> cikis 2x ama kapasite ~yariya (5W->10W ornegi)
RECINE_VERIM_MAX  = 0.80    # #6: en iyi kozak %80; direnc yuzunden mesafeyle duser
RECINE_YARI_M     = 20.0    # verimin RECINE_VERIM_MAX/2'ye dustugu kablo boyu [m]
GUVENLI_DIZI      = 4       # bu kadar tas guvenle baglanir; fazlasi faz cakisir -> patlar
GUCLENDIRME_VERIM = 0.01    # bedensel guclendirme verimi (§14): akla bagli — brute icgudu ~%1
ZEKI_VERIM        = 0.50    # zeki canli (ejderha) bedenini sekillendirir: ~%50
SIGMA             = 5.67e-8 # Stefan-Boltzmann [W/m2 K4] — eritme aurasinin radyan kaybi

# para: 100 tunc = 1 gumus, 10 gumus = 1 altin, 100 altin = 1 platin (tunc cinsinden)
GUMUS  = 100
ALTIN  = 10 * GUMUS
PLATIN = 100 * ALTIN
EKMEK_TUNC   = 2       # bir ekmek ~2 tunc (yarim ekmek = en kucuk sikke); ekonomi capasi
ASGARI_TUNC  = 10      # taban nakit gunlugu; yillik hizmette yemek/yatak/ayni odeme ayrica
SEHIR_ISCI_TUNC = 15   # ayni destegi olmayan serbest kent gundeligi
NAKIT_CALISMA_GUNU = 250
KIRA_AY_TUNC       = 100   # aile kulubesi aylik kira (2 asgari, 4 kisilik hane: ucu ucuna)
YAKIT_AY_TUNC      = 80    # aylik yakit + isik
OGUN_YETISKIN_TUNC = 2     # yetiskin ogunu (gunde 2 ogun: kahvalti + aksam)
OGUN_COCUK_TUNC    = 1     # cocuk ogunu (gunde 3 ogun)

def kure_cikis_kapasite(r_cm, k_cikis=K_CIKIS_MAVI, wh_cm3=WH_PER_CM3):
    """Kure tas: cikis = k_cikis * yuzey(4 pi r^2) [W]; kapasite = wh_cm3 * hacim(4/3 pi r^3) [Wh].
    r 2x -> cikis 4x (r^2), kapasite 8x (r^3): buyuk tas hem buyuk akim hem buyuk kapasite."""
    return k_cikis * 4 * math.pi * r_cm**2, wh_cm3 * (4/3) * math.pi * r_cm**3

def maden_enerji_wh(hacim_cm3):
    """Mavi kristal enerjisi (tek kullanimlik): hacim * 200 Wh."""
    return hacim_cm3 * WH_PER_CM3

def maden_fiyat_tunc(hacim_cm3):
    """Mavi fiyat: 5 cm3 = 1 kWh = 1 gumus -> cm3 basi 20 tunc (1 gumus/kWh)."""
    return hacim_cm3 * (GUMUS // 5)

def biyo_fiyat_tunc(kapasite_kwh):
    """Mor enerji TABAN fiyati: 5 gumus/kalan-kWh. kW cikis primi ve assay ayrica eklenir."""
    return kapasite_kwh * 5 * GUMUS

def kristal_sertifika(kalan_kwh, cikis_kw, sizinti_aylik, kalite):
    """Pazar tasini tek sayiya ezmez: E(kWh), P(kW), aylik sizinti ve iscilik notu birlikte yazilir."""
    assert kalan_kwh >= 0 and cikis_kw >= 0 and 0 <= sizinti_aylik < 1
    return {"kalan_kwh": kalan_kwh, "cikis_kw": cikis_kw,
            "sizinti_aylik": sizinti_aylik, "kalite": kalite}

def biyo_sure_saat(kapasite_kwh, cikis_kw):
    """Mor tas tam cikista kac saat surer: kapasite / cikis [saat]. Kurt: 30/2 = 15 saat."""
    return kapasite_kwh / cikis_kw

def feat_maliyeti_j(mekanik_j, verim=GUCLENDIRME_VERIM):
    """Bedensel feat'in mana maliyeti: mekanik_j / %1. Kurt (100 kg) 5 m sicrama 4900 J -> 490 kJ."""
    return mekanik_j / verim

def radyan_w_m2(T_c):
    """Sicak yuzeyin radyan kaybi (Stefan-Boltzmann): P = sigma * T^4 [W/m2], T Kelvin.
    Eritme aurasi: bunu tutmak icin mana = P / verim. T^4 yuzunden bin dereceler cok pahali."""
    return SIGMA * (T_c + 273.15) ** 4

def dizi_guc_w(n, tekil_w=100.0):
    """n mavi tasi bagla: guvenliyse n*tekil_w [W], degilse None (faz cakisir, patlar)."""
    return n * tekil_w if n <= GUVENLI_DIZI else None

def raf_kalan_oran(ay):
    """#11: raftaki tasta 'ay' ay sonunda kalan sarj orani = (1-sizinti)^ay."""
    return (1 - RAF_SIZINTI_AYLIK) ** ay

def recine_verim(uzunluk_m):
    """#6: recine kablonun verimi — tavan %80, direnc yuzunden mesafeyle duser."""
    return RECINE_VERIM_MAX / (1 + uzunluk_m / RECINE_YARI_M)

def kes_cikis_kapasite(cikis_w, kapasite_wh, carpan=KESIM_CARPAN):
    """#13: tasi kes/isle -> cikis 'carpan' kati, kapasite ayni oranda duser.
    Ornek: 5 W tas kesilince 10 W verir ama kapasitesi yarilanir."""
    return cikis_w * carpan, kapasite_wh / carpan

if __name__ == "__main__":
    assert maden_enerji_wh(5) == 1000                          # 5 cm3 = 1 kWh
    assert maden_fiyat_tunc(5) == GUMUS                        # 5 cm3 = 1 kWh = 1 gumus
    assert maden_fiyat_tunc(5) // EKMEK_TUNC == 50             # 1 kWh = 1 gumus = 50 ekmek
    assert maden_fiyat_tunc(5) // ASGARI_TUNC == 10           # 1 kWh = 10 gunluk asgari ucret
    # hane (2 yetiskin 2 cocuk): 250 nakit gun + bahce/yakit/cocuk/ayni odeme, ucu ucuna
    yemek_ay = (2 * 2 * OGUN_YETISKIN_TUNC + 2 * 3 * OGUN_COCUK_TUNC) * 30   # 14/gun -> 420/ay
    gider_yil = (yemek_ay + YAKIT_AY_TUNC + KIRA_AY_TUNC) * 12
    nakit_yil = 2 * ASGARI_TUNC * NAKIT_CALISMA_GUNU
    ayni_ve_hane_uretimi = gider_yil - nakit_yil
    assert gider_yil == 7200 and nakit_yil == 5000 and ayni_ve_hane_uretimi == 2200
    assert biyo_fiyat_tunc(30) == 15 * ALTIN                  # 30 kWh = 150 gumus = 15 altin
    assert kristal_sertifika(30, 2, 0.05, "lonca")["cikis_kw"] == 2
    assert biyo_sure_saat(30, 2) == 15                         # 2 kW cikis -> 15 saat
    c1, k1 = kure_cikis_kapasite(1); c2, k2 = kure_cikis_kapasite(2)
    assert abs(c2/c1 - 4) < 1e-9 and abs(k2/k1 - 8) < 1e-9     # r 2x -> cikis 4x, kapasite 8x
    assert round(feat_maliyeti_j(4900) / 1000) == 490          # 100 kg, 5 m sicrama %1 -> 490 kJ
    assert dizi_guc_w(4) == 400 and dizi_guc_w(5) is None
    assert kes_cikis_kapasite(5, 1000) == (10, 500)           # #13: 5W->10W, kapasite yari
    assert round(recine_verim(0), 2) == 0.80                  # #6: en iyi kozak %80
    assert 0 < recine_verim(20) < 0.80                        # mesafeyle duser (20 m'de yariya)
    assert 0.50 < raf_kalan_oran(12) < 0.60                   # #11: 1 yil rafta ~%54 kalir
    atlayis = 30 * 3600 * 1000 / feat_maliyeti_j(4900)         # 30 kWh / 490 kJ
    cooldown_s = feat_maliyeti_j(4900) / 2000                  # 2 kW cikista dolum
    # --- dragon (20 t, ZEKI %50) — gercek fizik ---
    DRAGON_W = 100e3                                            # kristal cikisi 100 kW
    assert round(DRAGON_W * 1200 / 3.6e6) == 33                 # suzulerek 20 dk ucus = 33 kWh
    assert round(4e6 * 3 / DRAGON_W / 60) == 2                  # kalkis: 12 MJ burst / 100 kW = ~2 dk sarj
    ates_mj = 0.5 * 44                                          # 0.5 kg yakit x 44 MJ/kg (havadaki O2 ile)
    ates_mana_kj = 0.5 * (0.5 * 14.7) * 60**2 / 1000 / ZEKI_VERIM  # sadece hava koruk KE / %50
    assert round(ates_mj) == 22 and round(ates_mana_kj) == 26  # 22 MJ alev, 26 kJ mana (bedava)
    assert round(radyan_w_m2(2500) / 1e6, 1) == 3.4            # eritme: 2500 C -> 3.4 MW/m2 radyasyon
    eritme_mana = radyan_w_m2(2500) / ZEKI_VERIM               # tutmak icin ~6.7 MW/m2 mana
    print("kurt(100kg) 5m sicrama", round(feat_maliyeti_j(4900) / 1000), "kJ ->",
          round(atlayis), "atlayis;", round(cooldown_s / 60, 1), "dk cooldown")
    print("dragon(20t,zeki): ucus 20dk 33 kWh, kalkis ~2 dk sarj; ates", round(ates_mj),
          "MJ kimyasal (mana", round(ates_mana_kj), "kJ); eritme 2500C", round(eritme_mana / 1e6, 1), "MW/m2 mana")
    print("kristal: 5cm3 kup=1kWh; kes 5W->10W(-kapasite); recine %80 tavan, 20m'de yariya;",
          "raf 1 yil ~%", round(raf_kalan_oran(12) * 100), "kalir")
