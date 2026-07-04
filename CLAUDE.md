# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Not: Bu depo iki farklı iş türü barındırır — **içerik yazımı** (Türkçe MDX hikâye
bölümleri) ve **frontend geliştirme** (React/Vite okuyucu). Hangi tarafta
çalışıldığına göre bakılacak yer değişir.

## Komutlar

Tüm frontend komutları `frontend/` içinden, **pnpm** ile çalışır:

```bash
cd frontend
pnpm install
pnpm dev        # Vite dev sunucusu (dev-only MDX editörü burada aktif)
pnpm build      # tsc -b && vite build  → dist/ (sitemap.xml + robots.txt üretir)
pnpm lint       # eslint .
pnpm preview    # üretim build'ini yerelde servis et
```

- **Tek bir dosyayı derleyip LLM bağlamına verme:** `python compile_mdx.py kisho`
  — bir kitabın tüm `.mdx` bölümlerini tek `story_output.txt` içinde birleştirir
  (isteğe bağlı bölüm aralığı sorar, örn. `3-16`). Test koşucusu değildir; bu
  depoda otomatik test yoktur.

## Deploy (kritik)

GitHub Pages'e deploy `.github/workflows/static.yml` ile yapılır ve **yalnızca
`main`'e push edilen commit mesajı "release" kelimesini içeriyorsa** (veya Actions
sekmesinden manuel `workflow_dispatch` ile) tetiklenir. "release" içermeyen
commit'ler siteyi güncellemez. Bu bilinçli bir kapıdır — her commit'e "release"
eklenmez.

## Mimari

### İçerik katmanı — tamamen konvansiyona dayalı, sıfır config

`content/stories/<kitap>/` altındaki her klasör bir "kitap"tır; klasör adı
`bookSlug` olur ve UI'da başlığa çevrilir (`the-wizard-of-oz` → "The Wizard Of
Oz"). Bölümler `<kitap>/chapters/*.mdx` içindedir. Dosya adı `pageSlug` olur;
`chapter10.mdx` gibi sayısal adlar doğal (numeric) sıralamayla TOC ve sayfalamayı
belirler. `docs/`, `library/`, `assets/` klasörleri her yerde atlanır.

MDX yazım kuralları, frontmatter alanları ve klasör düzeni **`AGENTS.md`** içinde
tanımlıdır — içerik dosyalarına dokunmadan önce oku.

Non-obvious noktalar:
- **Tarih frontmatter'da tutulmaz.** "Son düzenlenme" tarihi dosyanın filesystem
  mtime'ından `plugins/mdx-mtime.ts` sanal modülü ile türetilir. Elle tarih girme.
- **Frontmatter `gray-matter` ile değil**, `src/utils/markdown.ts` içindeki hafif
  regex ile parse edilir. Bu yüzden frontmatter'da inline virgül / kaçışsız
  string / karmaşık YAML kullanma — parser basit tutulmuştur.
- İçerik `frontend/` kökünün dışında olduğu için `vite.config.ts` içinde
  `server.fs.allow: ['..']` gerekir; dosyalar `import.meta.glob` ile yüklenir.

### Frontend — React 19 + Vite 8 + Tailwind 4, GitHub Pages SPA

`base: '/mystory/'`, router `basename="/mystory/"`. İki rota: kütüphane (`/`) ve
okuyucu (`/reader/:bookSlug/:pageSlug`). Bilinmeyen yol kütüphaneye düşer (404.html
SPA yönlendirmesi için var).

- **`src/utils/markdown.ts`** içeriğin tek giriş kapısıdır: glob'lardan kitap
  indeksini bir kez kurar (`_indexCache`), lazy raw loader'lar tutar, frontmatter
  parse eder, asset URL'lerini çözer. Kitap/bölüm okumak isteyen her şey buradan
  geçer.
- **`src/pages/useReader.ts`** okuyucunun tüm durumunu kapsar: sayfa çözümleme,
  ilerleme kaydı (`store/progress.ts`, localStorage), prev/next navigasyonu. UI
  sonraki/önceki linkleri elle almaz — slug indeksinden hesaplanır.
- **Zustand store'ları** (`src/store/`): `progress` (okuma yeri), `settings`
  (tema/font), `editing` (dev editör durumu).
- **Kod bölme:** rotalar `lazy()` ile yüklenir; `OptimizedImage` `<picture>` ile
  avif/webp/png sunar.

### Özel Vite eklentileri (`frontend/plugins/`) — asıl "sihir" burada

- **`mdx-mtime.ts`**: `content/stories/**/*.mdx` tarar, `virtual:mdx-mtime` sanal
  modülü olarak `{ "bookSlug/pageSlug": "YYYY-MM-DD" }` haritası verir. `.mdx`
  değişiminde HMR ile yeniden tarar.
- **`mdx-editor.ts`** (`apply: 'serve'` — sadece dev): `POST /__save-mdx` uç
  noktası ham MDX'i diske geri yazar; yoksa `chapters/` altına yeni dosya
  oluşturur ve glob tüketen modülleri invalidate ederek yeni bölümü sunucuyu
  yeniden başlatmadan görünür kılar. Üretim build'inde etkisizdir. Path traversal
  koruması ve slug regex doğrulaması içerir.
- **`sitemap.ts`** (`apply: 'build'`): `dist/sitemap.xml` ve `dist/robots.txt`
  üretir (her kitap + her bölüm, mtime'lı). `public/robots.txt`'i override eder.
- **`cover-optimize.ts`** (`apply: 'build'`, `closeBundle`): `dist/assets`
  içindeki PNG/JPG'leri `sharp` ile yeniden sıkıştırır ve `.webp`/`.avif`
  kardeşleri üretir.

## Kisho içeriği — kanon dokümanları

`content/stories/kisho/` içinde çalışırken önce `docs/rules.md` okunur (AGENTS.md
madde 0 bunu zorunlu kılar). Üç doküman katı şekilde ayrıdır, kategoriler
karıştırılmaz:

- **`docs/foundations.md`** — dünya kuralları, kristal-mana kanonu, sosyal yapı.
- **`docs/rules.md`** — anlatı disiplini, spoiler sınırı, üslup/kelime tutarlılığı,
  düzenleme iş akışı.
- **`docs/story_memory.md`** — hikâyede geçen kişi/hayvan/bitki/yer/kavram ve
  sabit terminoloji sözlüğü.

Yeni bilgi eklerken kategorileri karıştırmadan **eşleşen dosyayı** güncelle. Hikâye
Türkçe ve seinen tonundadır; metin çeviri kokusu taşımamalı, Kisho'nun o anki bilgi
seviyesinin ötesine spoiler vermemelidir (ayrıntılar `rules.md`).
