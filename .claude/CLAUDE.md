# Storytelling style

The story and the narrative are the whole point. Above all else, the writing must flow smoothly and
read easily — when any other rule here fights that goal, readability wins.

These rules govern all narrative prose in this project (the Kaiser story and any story content
here). They override any default instinct toward rich or literary prose.

- **Keep sections short.** No section in this file should grow past 300 lines; split or
  reorganize it before it reaches that limit.

- **Tell the story directly and straightforwardly.** Name things by their names — say "acid
  rain," not "gray, faintly sour rain." Never talk around something you could state plainly.
- **Readability first.** The goal is a story that pulls the reader along, fluid and easy to
  read. Choose flow over cleverness every time.
- **A plain, direct voice (the house style).** Short, clear sentences, mostly one idea each.
  Everyday words a tired reader understands on the first pass. State what happens, then stop, and
  let cause lead into consequence. A single blunt sentence on its own line can land a beat. Carry
  emotion and stakes through action and consequence, never through adjectives or an "epic" register.
  State even the strange and enormous matter-of-factly. The weight comes from what happens, not from
  ornate or literary language. (This supersedes the earlier "grave, legendary" voice wherever the
  docs still describe it; the rewritten **chapters 1 and 6** are the model to match.)
- **Through Kaiser's eyes.** We live the story from inside Kaiser's experience — immediate, in the
  moment, in what he senses and works out right now; keep the reader there by default. The narrator's
  wider, explaining voice (the grave chronicle register above) steps forward only for the sequences
  that *explain* something — the world, the metaphysics, how a thing works — and then recedes back
  into his point of view.
- **Show the vast by a glimpse, not a catalog.** Name ordinary things plainly (above) — but for
  the huge, the dreadful, or the wondrous, give one clear impression and stop. A thing half-seen,
  or a pointed silence, unsettles more than a full inventory. Don't pile on detail to prove scale;
  let the reader's mind finish it, and leave the deepest mystery unstated.
- **The refrain that turns.** A deliberate refrain is not lazy repetition. Plant a plain or telling
  line or image, and bring it back only when its return will mean *more* than the first time — at
  its strongest, something first read as ordinary pays off later as literal. If a repeat doesn't
  deepen, cut it.
- **Cut accidental repetition.** The refrain above is the *only* licensed repeat. Everything else —
  a word, an image, a sentence shape echoed within a few lines or across neighboring beats — is
  noise, and it dulls the prose. Hunt for it always, not only while writing: whenever you write,
  revise, edit, or even just read a passage, watch for the same word twice close together (three
  "cold"s, two "soul"s in a sentence), a doubled image (two things "thinning" a beat apart), or the
  same construction repeated — and when you spot it, fix it on the spot. Vary the word or, better,
  cut the weaker instance. When a phrase must recur, make sure it *earns* the recurrence as a
  refrain; if it doesn't, it's an accident — fix it.
- **Keep it simple.** Short, clear sentences. Minimal description — only what the scene needs.
  Avoid piled-up metaphors, stacked clauses, doubled adjectives, and ornate phrasing that slows
  the reader down.
- **Kısa ve öz — kill compressed and convoluted phrasing.** Two habits ruin Turkish clarity, and
  both must be hunted on every pass. (1) A squeezed noun-phrase no one would actually say — *on
  dakikalık işe muhtaç bir lamba* — opens into a plain relative clause: *on dakikada tamir
  edebileceği bir lamba*. (2) One idea over-explained across three or four sentences gets cut to the
  line that lands — *Porsiyonlar küçülür, buna karşılık da makinelerin boşaldığı söylentisi yayılır*
  — then stop; drop the "no one can prove it / whoever proves it loses their card" tail. Prefer
  simple, everyday words, and when unsure, cut.
- **Show character through action, not narrator praise.** Let the reader judge the character
  from what they do. The narrator never rates them ("gifted," "the one talent he has," etc.).
- **Consistency, within a chapter and across chapters.** Every beat must follow from what's
  already established. A character can't act on something they were never told or shown — if proud
  Izzet hides his debt, Kaiser can't walk in already knowing his time is up; he pieces it together
  in the moment. When you revise one chapter, re-check the others and the docs so nothing
  contradicts: names, timeline, who-knows-what, chapter numbers.
- **Revise by rebuilding, not by negating.** When a sentence needs work, rewrite it from scratch
  to say plainly what is there and what happens. Never patch it by tacking on what it isn't ("no
  box to drop off," "no pretense of a repair"). State the thing directly and let concrete action
  carry it.
- **When in doubt, cut.** A plain, concrete sentence beats a rich, ornate one.

The story wiki and working docs stay in English, but **write the chapters themselves directly in
Turkish.** Do not draft a chapter in English and translate it — English-first prose comes out stiff
and unidiomatic. Compose in Turkish from the start, with natural Turkish phrasing and idioms
  (*yerelleştir* — a Turkish reader should never feel a translation underneath). See
`content/stories/kaiser/docs/` for the story wiki (characters, magic system, arc map, narrative
  rules).

**Drafting mode — scene by scene is the default (*sahne sahne*).** Polishing a chapter to finished
literary prose costs too much time, so new chapters are drafted scene by scene in condensed running
prose. This is a *register*, not an outline:

- **Still real Turkish prose, still Turkish-first.** Full sentences, present tense (geniş zaman),
  third person, no em dash, plain everyday words. Every other rule in this file still applies.
- **Condensed, not thinned.** Clauses run together with commas where finished prose would break them
  into separate beats: *"Kaiser yağmurla uyanır, siste ne kadar kaldığını hatırlamaz, ısı ve acı bir
  anda üstüne biner."* Say more per sentence, then move on.
- **Never lose the fine detail.** The point is to skip the *craft* pass, not the *content*. Concrete
  specifics stay — the tool, the wound, the number, the exact object, the thing he notices. A vague
  summary is worse than no draft.
- **Drop only the artistry pass.** No hunting for rhythm, no single-sentence paragraphs used as
  beats, no engineered refrain placement. State what happens, clearly, and go on.
- **Number each scene** with a bare `1 - `, `2 - ` prefix. Do not title the scenes; the number alone
  is enough to keep the chapter skimmable and easy to expand later.
- Finished, polished prose is written only for a chapter the user explicitly asks to polish.
  **Chapters 1-4 are in the finished register; chapter 5 onward is scene-by-scene.**

**Writing in Turkish — craft notes.** The concrete conventions behind the *yerelleştir* rule above,
so the voice stays consistent across chapters:

- **VS Code-friendly line width.** In published `.mdx` chapter files, soft-wrap prose at roughly
  **92 characters per source line** so the text fits comfortably in the editor without horizontal
  scrolling. Preserve paragraph breaks, Markdown syntax, frontmatter, and the wording itself. This
  is source formatting only; do not insert extra blank lines or change the rendered prose. After
  writing or revising a chapter, check that no ordinary prose line exceeds 92 characters.
- **Short terminology notes.** When a chapter uses a technical, anatomical, historical, or
  world-specific term that a general reader may not know, mark only its first occurrence with a
  Unicode superscript number (`¹`, `²`, `³`). At the end of that chapter, add a separate Markdown
  block consisting of `---`, the heading `### Kısa Notlar`, and a numbered list of one-sentence
  definitions. Keep definitions short and concrete. Do not annotate ordinary vocabulary, repeat a
  note in the same chapter, invent unrevealed lore, or explain a mystery before the story earns it.
  Keep the note block and all its lines within the 92-character source limit.
- **Punctuation (noktalama) — no em dash in Turkish.** The em dash (`—`) is an English habit and
  reads foreign in Turkish prose; never use it in the chapters. Where an aside, appositive, or
  turn wants a break, use a comma, semicolon, colon, or parentheses, or just rebuild the sentence.
  (This rule is Turkish-only; the English docs and these notes may still use `—`.)
- **Tense (kip).** The grave chronicle runs in the present. Geniş zaman (aorist, *-ir*) is the spine
  — *durur, yürür, bilir, çıkarır*. Use şimdiki zaman (*-yor* / *-maktadır*) only for a genuinely
  in-the-moment action or state. Past tense (*-di* / *-mış*) is reserved for backstory told as
  backstory (how İzzet took Kaiser in, years earlier); keep the present-tense frame around it, and
  never flip a whole beat's tense while polishing.
- **Hunt translationese (*çeviri kokusu*).** The enemy is Turkish that reads like English
  underneath. Rebuild, in native word order, any: heavy nominal chain (*…olmasının sebebi …ayarlanmış
  olmasıdır* → a plain active sentence), an English "whether…or not" rendered as *…olup olmadığını*, a
  dangling demonstrative (*bu / şu / o*) with no clear referent, or a causative forced where a simple
  verb fits.
- **Use real idioms, where they land.** Reach for the genuine Turkish *deyim* when it fits the beat —
  *taş kesilmek, sırra kadem basmak, kılını kıpırdatmamak, tabana kuvvet, gözü dönmek, beş para
  etmemek, posası çıkmak* — but never shoehorn one; a plain sentence beats a forced idiom.
- **How we work a chapter.** Compose/rewrite Turkish-first, then pass it sentence by sentence for
  flow, idiom, and accidental repetition (the rules above). When several chapters need the same pass,
  one editor per chapter in parallel is fine — but re-read each result yourself against the
  glossary, tense, refrains, and cross-chapter consistency before trusting it.

## Story architecture

- **Information drives suspense.** Track what happened, what the viewpoint believes, what the reader
  can infer, and what an institution records. Wrong conclusions must be intelligent responses to
  limited evidence.
- **A scene has residue.** Give every substantial scene a present want, a working model, an active
  limit, a reversal, and a lasting result: cost, clue, debt, obligation, reputation, or false belief.
- **Prove competence before measuring danger.** Establish that an observer, worker, or opponent knows
  their field. Their precise failed assumption then reveals the scale of the anomaly.
- **Power is clearest through restraint.** Prefer preparation, verification, unguarded confidence, and
  the option not taken over loud declarations of strength. Early Kaiser has technical leverage, not
  physical invulnerability.
- **Worldbuilding enters through work.** Reveal systems through repair, food, wages, travel, ritual,
  law, checkpoints, injury, and failed tests. A quiet routine must build attachment, hierarchy, a
  future promise, or the next conflict.
- **Reputation becomes material.** When others mistake Kaiser's caution for foresight or his silence
  for authority, someone must commit status or resources to that belief. The misunderstanding then
  changes his options.
- **Braid three scales.** Move between domestic life, operational problems, and strategic ownership.
  After a large event, return to an ordinary need or object whose meaning has changed.
- **Recontextualize.** A later reveal should often change the meaning of an earlier gift, rescue,
  repair, or threat. Do not rely only on larger enemies and louder effects.
- **Keep side characters alive on the page.** Each recurring person needs a present want, private
  pressure, useful competence, boundary, mistaken belief, and a specific plan beyond the current
  scene. The future gives danger its price.
- **Violence follows decisions.** Establish objective, terrain, protected resource, false assumption,
  and retreat condition. During conflict, follow changing choices. Afterward, count wounds, energy,
  tools, witnesses, law, and belief.
- **Humor shares the same world as dread.** Build it from incompatible priorities, ceremonial scale
  interrupted by a practical need, or the gap between Kaiser's public image and private calculation.
  Never make injury slapstick or make locals stupid to flatter him.
