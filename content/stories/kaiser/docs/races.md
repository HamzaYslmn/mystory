# Peoples

The sentient races, and how mana divides them. [Power System](power-system.md) sets the mechanics;
this page sets who has what. One rule sits under the whole balance: **no people is strong at
everything, and the stronger a people's magic, the fewer it is and the slower it breeds.** Power is
paid for in numbers.

Three axes decide a mortal's magic ([§5](power-system.md#5-what-separates-casters)): **capacity** (how
much mana the body holds, in Wh), **throughput** (how fast it pours out — a multiple of capacity, in
W), and **aptitude** (what the spark can be turned to). Efficiency — how well the mana converts — is
trained on top. And flesh caps the tap: **no mortal channels much past ~1 kW**
([§16](power-system.md#16-the-casters-limits)). The peoples just reach that ceiling by different roads,
or never reach it.

Capacity itself is **trained up to a born ceiling** ([§2](power-system.md#2-the-reservoir)): drilling
grows your reserve toward a racial-and-talent limit, then stops. An ordinary human tops out near ~10 Wh
however hard he works; an elf's ceiling sits far higher. So the numbers below are **trained ceilings** —
what a people reaches at its best, not what an idler carries.

The great equalizer stands behind all of them: a person's whole reserve is tiny — **~10 Wh for most,
~300 Wh for the rarest elf** — beside a single-use crystal measured in **kilowatt-hours**
([§18](power-system.md#18-storage-crystals--the-mana-economy)). A mortal is *skilled but low-fuel*; a
crystal-beast is *crude but high-fuel*. A dwarf out-finesses a blood-wolf, and the wolf still
out-powers him thousands of times over on its purple stone. This is why magic is a craft, not a
war-winner, and why beasts and crystals decide battles that mortals cannot.

Fields below: **What · Homeland · Lifespan · Numbers · Mana · Signature · The trade** (the ceiling and
the floor that keep the people balanced).

## Elves — the deep reservoir

- What: ancient, few, long-lived; every elf a born caster
- Homeland: the West
- Lifespan: ~500 years
- Numbers: the smallest of the peoples — and 500-year lives mean few births, so a death replaces slowly
- Mana: **all** elves cast — mana-drill begins in childhood, so the gift is never wasted. Nine in ten hold **50–100 Wh** — a small town's worth of casting in one
  body. The other **one in ten** hold **300 Wh and up**: the archmages, with the finest efficiency in
  the world. Throughput is unhurried (~1× common, up to ~3× trained) — an elite elf pours ~**900 W**
  near the mortal ceiling for ~20 minutes, or ~**300 W for about an hour**, before the 300 Wh reserve is
  dry and a day's rest must refill it
- Signature: sustained, refined battle-magic and enchantment — the best patterns and circuits made, and
  held the longest
- The trade: supreme at magic, and almost no one to wield it. Isolationist, thin on the ground, slow to
  recover a single loss. A handful of archmages, never an army

## Dwarves — the burst and the forge

- What: stout, long-lived master-smiths; small reserves, ferocious output
- Homeland: the North
- Lifespan: ~250 years
- Numbers: few, but more than the elves
- Mana: dwarves take to the craft easily, so most learn it. A common dwarf holds only **~10 Wh** — but throws it fast. Their gift is **throughput**: the
  strongest master reaches **200 Wh at 5× — a full ~1 kW**, the hardest burst any mortal makes. They do
  not sustain; they **spike**
- Signature: **body-enhancement and impact weapons** ([Projection](power-system.md#projection)). A
  scribed hammer or axe buffers a charge between swings and dumps it on contact — a master lands
  **1–2 kJ a blow**, enough to split a shield. Their **ground-set impact shield** doesn't absorb a blow
  (absorbing is dear, [§13](power-system.md#negation)) — it **turns the strike's vector down into the
  earth**, so the ground takes the reaction and only a fraction reaches the dwarf. And no one builds
  crystal **devices** better: the dwarves arm the world
- The trade: kings of burst and craft, capped at a candle's worth of stored mana. No dwarf sustains
  magic — drain the reserve and the hammer is just iron

## Humans — the balanced many

- What: short-lived, adaptable, everywhere; masters of nothing, adequate at all
- Homeland: all of it — humans are the connective tissue between the others
- Lifespan: ~70–80 years
- Numbers: vast, and they breed fast — a war's losses are a generation, not a century
- Mana: humans are farmers with no one to teach them, so magic mostly goes unlearned — only about
  **one in five** ever picks it up, usually a trick or two off a **wandering mage** passing through:
  starting a fire, a few heartbeats of light. Those who do carry **~10 Wh** and output about as much
  (~1×, ~10 W). Real casters are the trained few; a rare notable reaches ~100 Wh. And once in a great
  while a human is a **universal engineer**, the equal of any dwarf master at the workbench — never more
  than a handful alive
- Signature: **arrow-acceleration and body-enhancement** in war; **engineering** in craft. No single
  peak, every field entered
- The trade: outdone in magic by elves, at the forge by dwarves, in the body by beastmen — and
  everywhere, numerous, adaptable, quick to recover. Ubiquity is the human weapon. (Kaiser lands here:
  the rare engineer, in a body with a hidden [Mist bond](power-system.md#20-ocak-kanlı))

## Beastmen — the strong hand

- What: cat- and dog-kin — human-shaped, with ears, tails, and beast-quick bodies
- Homeland: the East, deep in the wild; they live with the land, not over it
- Lifespan: ~50–60 years
- Numbers: the most numerous of all the peoples
- Mana: **low, and body-enhancement only.** A beastman carries little mana — enough to **boost his own
  body** (a harder hit, a faster dash). They **learn it young, at the hunt**, passed down as a hunter's
  skill rather than scribed from a book. Layered on a frame already stronger and faster than a man's, it
  makes a fearsome close fighter. But that is the whole of their magic: they don't scribe circuits or
  build devices
- Signature: **enhanced body** — natural strength and speed, pushed further by self-enhancement learned
  in the chase. What another race must build entirely out of mana, a beastman mostly already has and
  only tops up
- The trade: the strongest bodies and the largest numbers — and it stops at the body. Not that they
  *can't* learn a craft, but split into small warring villages with no teachers and no unity, they never
  do; they **buy** dwarf-made blades and tools rather than forge magic of their own. Strength that never
  gathers into power



## Ocak Kanlı — the bloodline across peoples

Not a people but a **rare bloodline** that can surface in any of them
([§20](power-system.md#20-ocak-kanlı)): a direct channel to the Mist, born once in a great while, marked
by an outsized regeneration anywhere. **Kaiser is secretly one** — he doesn't know it, and the reveal is
far off.

## To design

Add peoples as scenes demand, each with the same fields; pin any new mana numbers in `magics/irklar.py`.
