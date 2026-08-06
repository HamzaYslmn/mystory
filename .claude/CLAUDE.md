# Kaiser — writing rules

**The story is the point. When a rule below fights readability, readability wins.**

Chapters are written in Turkish from the start, never drafted in English and translated. Chapter
files live in `content/stories/kaiser/chapters/`; the story wiki in
`content/stories/kaiser/docs/` stays in English.

Each rule lives in exactly one section:

| Section | Covers |
|---|---|
| Register | which chapters are finished, how new ones are drafted |
| Voice | how a sentence sounds; tense and repetition |
| Turkish, not translated Turkish | judgement calls that separate native prose from translation |
| Yazım denetimi | checkable orthography and punctuation |
| Story architecture | plot, consistency, what the arc may not do |
| Chapter files | source formatting, Kısa Notlar, cover art |
| Fixed motifs | canon that never changes |

## Register

| Chapters | Register | Model to match |
|---|---|---|
| 1-2 | **Finished prose.** Full scenes, dialogue, paragraph breaks, no scene numbers. | Ch1 |
| 3 onward | **Scene-by-scene draft.** Condensed running prose, numbered `1 - `, `2 - `. | Ch4 |

Draft mode is real Turkish prose, not an outline: full sentences, present tense, third person,
plain words, clauses running together with commas where finished prose would separate them.
**Condensed, not thinned** — every concrete specific stays: the tool, the wound, the number, the
object he notices. What you skip is the craft pass, so no hunting for rhythm and no engineered
refrains. Chapters 3-5 are drafts awaiting polish; do not treat their compression as the house
standard. Polish a chapter to finished prose only when asked for that chapter.

## Voice

- **Plain and direct.** Short sentences, mostly one idea each. Everyday words a tired reader gets
  on the first pass. State what happens, then stop; let cause lead into consequence.
- **No epic register.** Carry emotion through action and consequence, never through adjectives.
  State even the strange and enormous matter-of-factly. Weight comes from what happens.
- **A single blunt sentence on its own line** can land a beat. Use it sparingly or it stops working.
- **Specificity is not ornament.** Keep the tool, the wound, the number, the exact object, the
  reasoning step. Cut adjectives, metaphors and mood-painting. "Minimal description" means no
  decoration, not no detail.
- **Show the vast by a glimpse.** One clear impression, then stop. Never catalogue to prove scale.
  This applies to spectacle, not to work: technical sequences earn their length.
- **Never praise the character.** No "gifted", no "master". The reader judges from what he does.
- **Point of view.** Stay inside Kaiser's experience: what he senses and works out right now. The
  narrator's wider, explaining voice steps forward only for the world or its metaphysics (as in
  Ch3), then recedes.
- **Tense.** Geniş zaman is the spine (*durur, bakar, ölçer*). Use *-yor* only for a genuinely
  in-the-moment action. Past tense (*-di* / *-mış*) is for backstory told as backstory; keep the
  present-tense frame around it and never flip a whole beat while polishing.
- **Repetition.** Cut accidental repetition ruthlessly on every pass, including when you are only
  reading: the same word twice within a few lines, a doubled image, a repeated sentence shape.
  A refrain returns only when it means more than the first time; at its best something first read
  as ordinary later pays off as literal. If a repeat doesn't deepen, it's an accident.

## Turkish, not translated Turkish

**Scope: every Turkish sentence, not only chapters.** Chat replies, reports and design summaries
are held to the same standard. Compose the sentence in Turkish first; never build an English
skeleton and fill it with Turkish words.

- **The book test.** Ask of every sentence: would this appear in a book originally written in
  Turkish? If not, rebuild it in native word order.
- **Every sentence needs a verb.** No headless fragments: *Sistemin belkemiğinde bir ölçek farkı.*
  → *Sistemin altında bir ölçek farkı yatar.* A colon does not license dropping the predicate, and
  a bolded lead-in is still a sentence.
- **No English rhythm.** Do not chain short punchy sentences for effect, do not open with *Ve* /
  *Ama* as a beat, and cut translated connectives (*tam olarak*, *işte bu*, *şurada başlar*).
  Turkish binds clauses instead: *çünkü, ne var ki, oysa, dolayısıyla, üstelik, ancak*.
- **No calqued idiom.** An English figure has no Turkish stock behind it: *birkaç kalp atımı* is
  not Turkish. Write *birkaç saniye*, or rebuild the sentence.
- **Two killers.** (1) **Personification** — *ateşin ne istediğini bilir*, *acı bacağını kilitler*,
  *yorgunluk üzerine kapanır*. (2) **Invented metaphor** Turkish has no stock for — *kapıları
  sökülmüş bir bina gibidir*. Say the thing plainly instead.
- **Say it once, short.** Never stretch one idea across two clauses.
- **Kısa ve öz.** Open squeezed noun-phrases nobody would say (*on dakikalık işe muhtaç bir lamba*
  → *on dakikada tamir edebileceği bir lamba*). Cut an idea explained across four sentences down to
  the line that lands, then stop.
- **Hunt translationese.** Rebuild heavy nominal chains (*…olmasının sebebi …olmasıdır*), English
  "whether or not" as *…olup olmadığını*, demonstratives (*bu / şu / o*) with no clear referent,
  and causatives forced where a simple verb fits.
- **Real idioms where they land** — *taş kesilmek, sırra kadem basmak, tabana kuvvet, beş para
  etmemek*. Never shoehorn one; a plain sentence beats a forced idiom.
- **No aphorisms.** Never write a neat, balanced, quotable line stating a general truth (*Yazılım
  yanılabilir. Zincir yanılmaz.*). It reads as the author speaking through the character and
  restates what the scene already showed. Never use the device that sets one up either, such as
  the character writing a phrase on paper. State the reasoning plainly about *this* machine and
  *this* moment.
- **Write the event, not its absence.** A sentence must carry what happens, what a thing is, what
  he sees. *Eşikten hemen dışarı atlamaz* → *Eşiğe kadar sürünüp orada bekler*. *Başka ses yoktur*
  → *Duyduğu her ses bu ikisinden birine çıkar*. *Karar veremez* → *Üçü de bu izle uyuşur*. Keep
  a negation only where the missing thing is itself the fact he acts on.
- **Revise by rebuilding.** Rewrite a weak sentence from scratch to say plainly what happens. Never
  patch it by adding what it isn't ("no box to drop off", "no pretense of a repair").
- **When in doubt, cut.**

## Yazım denetimi

The rules above are judgement calls. Orthography is not: **run the `turkce` skill on every Turkish
text before handing it over** (`.claude/skills/turkce/SKILL.md`). It carries the rules offline, so
do not write them from memory and do not copy them into this file.

| Read for | Where |
|---|---|
| **Her denetimde okunan özet** — 15 madde, kararların çoğunu bitirir | `skills/turkce/references/ozet.md` |
| İmla, noktalama, ekler, uyum, sayılar, kısaltmalar (29 bölüm) | `skills/turkce/references/imla-kurallari.md` |
| Ögeler, öge sırası, vurgu, fiilimsi, bağlaç, tamlama, çeviri kokusu | `skills/turkce/references/cumle-yapisi.md` |
| Öge eksikliği, çatı ve uyum hataları, gereksiz sözcük, deyim yanlışları | `skills/turkce/references/anlatim-bozukluklari.md` |
| Bu projede daha önce yapılmış hatalar | `skills/turkce/references/proje-notlari.md` |
| Tek bir kelimenin doğru yazımı, anlamı, kökeni; bir deyimin gerçek biçimi | [TDK Sözlük](https://sozluk.gov.tr) |
| Satır genişliği, *-maktadır*, em dash, bağlaç sayımı, yakın tekrar | the skill's denetim listesi |

The skill covers correctness. These six are house register, so no source will warn you:

- **No *-maktadır* / *-mektedir*.** Official-report kip. Write *yatar, dökülür, gider*.
- **One plain connective.** Ch3 binds nine clauses with *ama* and nothing fancier. *Ne var ki,
  oysa, üstelik, dolayısıyla* are seasoning: at most one per chapter, never two contrasts in one
  sentence.
- **Never drop the iyelik eki.** *Diz tutar* → *dizi tutar*. Anything with an owner in the scene
  carries its possessive.
- **A real verb beats *vardır* / *yoktur*.** *Yerde iki ok vardır* → *Yerde iki ok durur*.
- **No em dash (—) in Turkish prose.** Comma, semicolon, colon, parentheses, or rebuild the
  sentence. English docs may still use them.
- **Dialogue takes double quotes** (`"..."`), the convention Ch1 set. TDK also allows the konuşma
  çizgisi at line start; the book does not use it.

## Story architecture

- **Consistency is non-negotiable.** A character cannot act on something they were never told or
  shown. When you revise one chapter, re-check the others and the docs: names, timeline,
  who-knows-what, chapter numbers.
- **Information drives suspense.** Track what happened, what Kaiser believes, what the reader can
  infer, and what an institution records. Wrong conclusions must be intelligent responses to
  limited evidence.
- **Every substantial scene leaves residue:** a cost, clue, debt, obligation, reputation or false
  belief that outlasts it.
- **Prove competence before measuring danger.** Establish that someone knows their field; their
  precise failed assumption then reveals the scale of the problem.
- **Power through restraint.** Prefer preparation, verification and the option not taken over
  declarations of strength. Kaiser has technical leverage, not invulnerability.
- **Worldbuilding enters through work** — repair, food, wages, travel, law, checkpoints, injury,
  failed tests. A quiet routine must build attachment, hierarchy or the next conflict.
- **Recontextualize.** A later reveal should change the meaning of an earlier repair, gift or
  threat. Do not rely on louder enemies.
- **Violence follows decisions.** Establish objective, terrain, false assumption and retreat
  condition. Afterward count wounds, tools, witnesses, law and belief.
- **Humor and dread share a world.** Build it from incompatible priorities or the gap between
  Kaiser's public image and his private calculation. Never make injury slapstick or locals stupid
  to flatter him.
- **The old world gets one chapter.** Ch1 carries the city, the proof of competence and Kaiser's
  death. Do not add a second Anakara chapter; the reader does not need the cyberpunk world in
  depth and it delays the isekai.

## Chapter files

- **Wrap chapter source lines at ~92 characters.** Source formatting only; do not change wording,
  paragraph breaks or frontmatter.
- **Kısa Notlar.** Mark the first occurrence of a technical, anatomical or world-specific term with
  a superscript (`¹`, `²`, `³`). At the chapter end add `---`, `### Kısa Notlar`, and a numbered
  list of one-sentence definitions. Never annotate ordinary vocabulary, repeat a note, or explain
  a mystery the story hasn't earned.
- **Covers** live in `content/stories/kaiser/assets/chapter-N.png`, referenced from frontmatter as
  `/assets/chapter-N.png`. Generate them with `.claude/skills/agy/SKILL.md`.
- **No characters on a cover, ever.** No people, no figures, no faces, not even distant or
  silhouetted. Kaiser is never drawn. Places, weather, wreckage, objects and machines only.
- **One subject per cover**, and it must be something the chapter actually contains. A cover that
  invents a detail (magic lightning on a cart wheel) contradicts the prose.
- **House look:** muted desaturated palette, cinematic painterly illustration, dramatic natural
  light, square 1:1. The covers must read as one set. No text and no readable signage in the
  image; Anakara is not an English-speaking city.

## Fixed motifs

- Kaiser's signature gesture is **two fingers to the forehead** before he solves something. The
  gesture survives his death and memory loss; its origin does not.
- **Arc 1 runs on worth, not on a bond.** There is no mentor and no loved one in the old world. Do
  not add an old-world attachment.
