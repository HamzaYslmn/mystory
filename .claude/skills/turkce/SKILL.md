---
name: turkce
description: Türkçe metin yazarken, düzeltirken veya gözden geçirirken imla, noktalama, anlatım bozukluğu ve ev üslubu denetimi yapar; şüpheli kelimeleri TDK Sözlük API'siyle doğrular. Bu depoda üretilen HER Türkçe metinde çalıştır - bölüm yazmak, sahne düzeltmek, paragraf yeniden kurmak, doküman çevirmek, hatta uzun sohbet yanıtı yazmak dâhil. Tetikleyiciler - 'imla kontrolü', 'yazım kontrolü', 'anlatım bozukluğu', 'Türkçe düzelt', 'metni düzelt', 'redaksiyon', 'gözden geçir', 'bu cümle doğru mu', 'TDK'de var mı', 'doğru yazımı ne', 'şu deyim doğru mu', ayrıca 'bölüm yaz', 'sahneyi düzelt', 'kısalt', 'birleştir', 'akıcı yap' gibi Türkçe metin üreten her istek. Kullanıcı 'imla' demese bile Türkçe cümle yazılıyorsa tetikle.
---

# Türkçe denetimi

Üç katman var, sırayla uygulanır. Alt katman üsttekini geçersiz kılmaz.

## Ne okunur

**Her seferinde iki dosya:** `references/ozet.md` ile `references/proje-notlari.md`. İkisi kısadır
ve kararların yüzde doksanını bitirir. Dışarıya bakmaya gerek yoktur.

Yetmediğinde ilgili derin dosyayı aç:

| Şüphe | Dosya |
|---|---|
| Bir yazım ya da noktalama maddesinin tam metni | `references/imla-kurallari.md` (29 bölüm) |
| Öge, vurgu, fiilimsi, bağlaç, tamlama ayrıntısı | `references/cumle-yapisi.md` |
| Anlatım bozukluğunun türü ve örnekleri | `references/anlatim-bozukluklari.md` |
| Bu kitabın sesi | `.claude/CLAUDE.md` (oturumda zaten yüklü) |

TDK'ye yalnızca **tek bir kelimenin varlığından ya da bir deyimin gerçek biçiminden** şüphelenince
sor; kural aramak için sorma:

- Doğru yazım `https://sozluk.gov.tr/yazim?ara=KELIME`
- Anlam ve köken `https://sozluk.gov.tr/gts?ara=KELIME`
- Deyimin gerçek biçimi `https://sozluk.gov.tr/atasozu?ara=KELIME`

## Nasıl çalışır

1. **Metni al.** Yeni yazdıysan kendi çıktın, düzeltiyorsan dosyanın ilgili kısmı.
2. **`ozet.md` ile `proje-notlari.md` dosyalarını oku.**
3. **Özetin on beş maddesini** baştan sona geçir; sonuncusu ev kurallarının denetim listesidir.
4. **Cümle cümle oku.** Her cümle için: yüklemi var mı, ögeleri tam mı, iyelik ekleri yerinde mi,
   bir Türk yazarın kitabında bu cümle böyle mi durur.
5. **Düzelt.** Dosya üstünde çalışıyorsan doğrudan Edit ile uygula, ayrı rapor çıkarma. Yalnızca
   kullanıcı rapor isterse yanlış/doğru listesi ver.
6. **Yeni bir hata türü yakaladıysan** `references/proje-notlari.md` dosyasına bir satır ekle.

Uzun bir metni tek başına denetlemek zorsa `general-purpose` bir subagent'a aynı listeyi ver ve
bulguları karşılaştır. Kullanıcı istemedikçe subagent açma.

## Bu kitaba özel, hiçbir kaynakta yazmayan kurallar

`CLAUDE.md` bunları taşır, burada yalnızca denetim listesi olarak duruyorlar:

- `-maktadır / -mektedir` yasak. Resmî rapor kipi.
- Bölüm başına en fazla bir baharat bağlaç: *ne var ki, oysa, üstelik, dolayısıyla*. Düz bağ *ama*.
- İyelik eki düşmez. *Diz tutar* değil, *dizi tutar*.
- *vardır / yoktur* yerine gerçek fiil. *Yerde iki ok vardır* → *Yerde iki ok durur*.
- Türkçe metinde em dash (—) kullanılmaz. İngilizce dokümanlar serbest.
- Diyalog çift tırnakla, konuşma çizgisiyle değil.
- Özdeyiş yok. Dengeli, alıntılanabilir, genel doğru bildiren cümle kurma.
- Olanı yaz, olmayanı değil. *Başka ses yoktur* → *Duyduğu her ses bu ikisinden birine çıkar*.
- Kişileştirme ve uydurma benzetme yok. *Acı bacağını kilitler* gibi cümleleri düz kur.
- Bölüm dosyalarında satırlar ~92 karakterde sarılır.

## Sık düşülen tuzaklar

Aşağıdakiler bu projede gerçekten yapılmış hatalar. Ayrıntısı `references/proje-notlari.md`
dosyasında.

- Anlamı kaymış kelime seçmek: *yerleşke* kampüstür, *namlu* ateşli silahtadır, *yolda kalmak*
  aracın bozulmasıdır, yayın ipi *çile* değil *kiriş*tir.
- İngilizceden çevrilmiş bağlaç ve ritim: *tam olarak*, *işte bu*, kısa cümleleri arka arkaya
  dizip vurgu arama.
- Yüklemsiz başlık cümlesi kurmak; iki nokta bunu mazur göstermez.
- Aynı fiili birkaç satırda tekrarlamak. *durur*, *çıkaramaz*, *yoktur* çabuk tik hâline gelir.
