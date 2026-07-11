# robot.py — Robot/golem buyusu (Animation koordinasyonu, doc §13).
# DUNYA: yerli ustalar KESIN tetik-sozcuk kullanir (bir kelime -> bir eylem),
#   cogu saldiri/savunma icin; bulanik eslesme kavramini bilmezler.
# KAISER (#9): kodlama bildigi icin soyleneni EN YAKIN komuta esler (bulanik) -
#   bu bir hesaplamadir ve dunyada bir ilktir. Asagisi onun surumu.
# ponytail: difflib bulanik eslesme yeter; gercek dil anlama gerekirse
#   onune bir LLM cagrisi konur, model egitilmez.
import difflib

# tetik -> eylemler. Eylem simdilik yazdirilan ad; robota baglarken fonksiyon koy.
KOMUTLAR = {
    "ilerle":   ["ileri"],
    "geri":     ["geri"],
    "sola don": ["sola don"],
    "saga don": ["saga don"],
    "dur":      ["dur"],
    "ates et":  ["silahi atesle"],
    "kaz":      ["kurek al", "kaz"],
    "topla":    ["nesneyi al"],
    "birak":    ["nesneyi birak"],
    "temizle":  ["otlari temizle"],
}

def komut_bul(soz, esik=0.6):
    """En benzeyen tetigin eylemleri; hicbiri esigi gecmezse None."""
    soz = soz.lower()
    tetik = max(KOMUTLAR, key=lambda t: difflib.SequenceMatcher(None, t, soz).ratio())
    skor = difflib.SequenceMatcher(None, tetik, soz).ratio()
    return KOMUTLAR[tetik] if skor >= esik else None

def calistir(soz):
    for eylem in komut_bul(soz) or []:
        eylem() if callable(eylem) else print(f">> {eylem}")

if __name__ == "__main__":
    assert komut_bul("ates et") == ["silahi atesle"]
    assert komut_bul("biraz ilerle") == ["ileri"]
    assert komut_bul("sola don") == ["sola don"]
    assert komut_bul("guzel bir gun") is None
    print("robot kontrolleri gecti")
