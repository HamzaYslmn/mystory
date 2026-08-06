# Proje notları

Bu dosya bu depoda gerçekten yakalanmış hataları tutar. Kural kitabı değil, sabıka kaydıdır.
Yeni bir hata türü yakalandığında buraya bir satır eklenir; genel kurallar `references/` altındaki
öteki iki dosyada ve `CLAUDE.md` içinde durur.

## Anlamı kayan kelimeler

Aşağıdakiler cümlede doğru duruyordu, ne var ki kelimenin gerçek anlamı başkaydı. Emin olmadığın
kelimeyi metne koymadan önce TDK'ye sor.

- **kiriş**, yayın ipidir. *Çile* iplik demetidir, yayda kullanılmaz.
- **ağız**, kılıcın kesen yüzüdür. *Namlu* ateşli silaha aittir.
- **kasaba, köy.** *Yerleşke* üniversite kampüsüdür, ortaçağ dünyasına oturmaz.
- **açıkta yakalanmak.** *Yolda kalmak* aracın bozulup kalmasıdır.
- **dar toprak yol.** *Patika* yaya yoludur, üstünde teker izi olmaz.
- **parmakların izi.** *Parmak izi* adli terimdir, yanık izini anlatırken çarpışır.
- **yıkarken.** *Yıkararken* diye bir çekim yoktur.

## Karakterin ağzına uymayan kelime

Kaiser teknolojik bir şehirden gelir, hafızası gitmiştir ama teknik bilgisi durur. Bu yüzden
*kandil, ocak* gibi sanayi öncesi örnekler değil, kendi dünyasının kelimeleri gelir aklına:
*pil, radyasyon*. Tersi de geçerlidir; bu dünyanın insanları onun kelimelerini kullanmaz.

## Düşen ekler ve yüklemsiz cümleler

- *Diz tutar* değil, **dizi tutar**. Sahnede sahibi olan her ad iyelik ekini taşır.
- İki nokta yüklemi düşürmez. **Sistemin belkemiğinde bir ölçek farkı.** diye cümle olmaz.

## Tik hâline gelen fiiller

*vardır / yoktur* yasağı kendi tikini doğurdu: bir bölümde on iki *durur*, dört bölümde yedi
*çıkaramaz* birikti. Bir yasağı uygularken yerine koyduğun fiili de say.

## Düzeltirken doğan yeni hatalar

Her düzeltme turundan sonra aynı cümleyi bir kez daha oku. Bu projede düzeltmenin kendisi şunları
üretti: *yol… yoldur* aynı cümlede, ikizlenmiş *yerde*, *bir karışlık bir parça*, bir kelime
değiştirilince kalan *sise benzer ince bir sis*.

## Arama deseni kurarken

`m\(ak\|ek\)tedir` yalnızca *maktedir* ile eşleşir, dokuz tane *maktadır* elini kolunu sallayarak
geçer. Türkçede ünlü uyumu deseni de değiştirdiğinden her iki ünlüyü de yaz:
`m[ae]kt[ae]d[ıi]r`. Aynı tuzak `-yor`, `-dık`, `-acak` aramalarında da vardır.

## Satır genişliğini ölçerken

`awk length` bayt sayar; Türkçe harfler UTF-8'de iki bayt tuttuğundan her satır uzun görünür ve
bütün dosya hatalı sanılır. Karakter saymak gerekir.
