# Magic Machines — Invention Log

Working catalogue of the machines the mana-engineering system makes possible. Physics and numbers
live in [Power System](power-system.md); the runnable spell behind each is in `magics/`. Every entry
names the discipline it runs on, its spell file, and what it costs.

Three registers: what the **world already builds** (Kaiser meets it, then improves it), what he
**builds on the page**, and his **edge** — what he does first or better, up to the long game he tells
no one.

## Built in the story

**Robot / golem.** Animation ([§13](power-system.md#animation)), `robot.py` + `animasyon.py`. A worked
object that runs a written loop. Local masters trigger it with **exact key-words** — one spoken word,
one scribed action — mostly for attack and defense; matching a *loose* phrase to the nearest command is
information-processing no one here thinks of. **Kaiser can**, because he knows it as computation, and a
programmable golem is one of his quiet edges. Two bills: muscle (τ = load·arm, P = τω) and the
coordination "CPU" (DOF × loop-rate × sensing). A one-joint grinder runs for hours off a sliver; a
balancing biped costs ~1000× the CPU and staggers when its maker's attention breaks. No intelligence —
only what is scribed.

**Hand-lamp / flashlight.** Light projection ([§13](power-system.md#projection)), `isik.py`. A scribed
light-circuit, best on a matched perovskite substrate. At the circuit range (**30–80%**), 100 Wh gives
~250 lm for roughly **36–96 hours**; the old 6-hour figure belongs to a novice's 5% unstructured
hand-light, not a device. A city's set lamp can hold ~50 Wh and burn all night. Kaiser's first small
machine — light on demand, no flame.

**Piston / mana-engine.** Motive power ([§13](power-system.md#motive-power--the-mana-engine)),
`motor.py`. A force-circuit drives a piston, a spring or double-acting stroke returns it — a
solenoid-style reciprocator — and a crank and flywheel turn the stroke into shaft rotation. ~36 W of
shaft-work from a 100 W blue feed at ~36% end-to-end. That is an **assist**, not a cart engine: bulk
rotation still belongs to water, wind, animals, and muscle. Kilowatt purple can propel a cart or pump,
but its fuel price reserves that for war, rescue, mines, and nobles.

## In the world

**Storage crystal — single-use cell.** `kristal.py`, [§18](power-system.md#18-storage-crystals--the-mana-economy).
The world's fuel, not a battery: a fixed charge spent once, no recharge — and it **slowly leaks on the
shelf** by a grade measured in percent per month, so stock must keep moving (constant demand). Its weak
connected raw output is not the same as its much slower disconnected shelf leakage. **Blue** mineral (a ~5 cm³ cube ≈ 1 kWh, ≤100 W
worked, ~1 silver/kWh) runs daily devices; **purple** biological is denser and delivers kilowatts (a
blood-wolf stone ~30 kWh at 2 kW). Output rises with a stone's surface area, capacity with its volume —
big stone, big power — and **cutting** a stone raises its output at the cost of capacity. Wiring too many
blue in series/parallel beats out of phase and can explode.

**Mana cable.** Bornmülleriana resin, [§18](power-system.md#18-storage-crystals--the-mana-economy).
The one workable mana wire — mana conducts along it by contact, but the resin has **resistance**, so
efficiency **falls with distance** and the finest kozak tops out near **80%**. Runs a device from a
distance, or carries the feed while a circuit is scribed onto something out of reach. Not a store; a
conductor. (A unicorn's horn conducts near-perfectly, but it's a rare relic, not wire.)

**Ward-stone / shield.** Wards ([§13](power-system.md#wards)), `siper.py`. A scribed barrier that
absorbs or deflects — ~2,900 *plain* arrows off 100 Wh at 40%, or roughly **50–140** 1–3 kJ bullets if
it foolishly absorbs them head-on; deflection
stretches it far further. But fighters **enhance their weapons** ([Projection](power-system.md#projection),
`kuvvet.py`) — a boosted arrow carrying kilojoules collapses that count, so a ward is a **budget duel**,
not a fixed wall. A caravan mage turns plain arrows all day; one boulder, or one well-fed swing, empties
him. Gate-wards outlast their makers.

**Heater / kettle / forge.** Heat projection ([§13](power-system.md#projection)), `isi.py`. Q = mcΔT
plus the cost to *hold* a temperature. ~140 ml of water boils to steam off 100 Wh only at ideal 100%;
an 80% circuit manages ~110 ml. Wood and charcoal are far cheaper for bulk heat. Mana belongs to
smokeless noble rooms, field medicine, ignition, and a smith's small precision hot-spot — not replacing
the whole forge or kitchen fire.

**Ice-box (naive).** Alteration/cold ([§13](power-system.md#alteration)), `buz.py`. The ideal local way
dumps heat straight out — ~0.86 kg of ice off 100 Wh before circuit loss (~0.69 kg at 80%). Kaiser's
compressor triples the same-efficiency result (below). Crystal price keeps both in medicine, luxury,
and valuable cargo rather than mass food storage.

**Illusion projector / decoy.** Illusionism ([§13](power-system.md#illusionism)), `yanilsama.py`. Real
light and sound tuned to the eye — matching noon (~100,000 lux) is dear, night nearly free. Fools eyes
and ears, never touch; betrayed at noon by the missing shadow.

**Night-lens / heat-sight.** Sensing ([§13](power-system.md#sensing-instruments)), `mercek.py`. An
upconversion coating soaks infrared and re-emits it visible — a plain eye sees warmth in the dark. Two
IR photons make one visible; aperture sets sharpness (1.22 λ/D). A hunter picks a warm body out of cold
brush; a mana-density plate reads the dead patch around a Bornmülleriana grove.

**Horn / alarm / loudspeaker.** Sound projection ([§13](power-system.md#projection)), `ses.py`.
Acoustic power → SPL, falling ~6 dB per doubling of distance — ~140 dB at 10 m off a modest budget.
Sound is cheap and it is only noise: good for signaling and warning, never for work.

**Cutter / press / brake.** Alteration ([§13](power-system.md#alteration)), `alter.py`. Plastic work
(σ·ε·V) to bend, or fracture energy (γ·A) to cut — cheaper to cut than to crush. A lock-bolt chilled
brittle then cracked with a tap; ~7,200 cm³ of steel bent off 100 Wh at 10% strain.

**Healing device.** Medical ([§14](power-system.md#medical)), `sifa.py`. Feeds mana a body takes up —
the biological ideal is ~72 g of tissue per 100 Wh, but a best 80% scribed feed delivers at most
~**58 g** before biological rate and information limits. Painless self-cast; on another it burns, the flesh forced
to re-spin the flood. Field medics and their screaming patients.

## Kaiser's edge

**Compressor ice-box.** `buz.py`, COP 3. A refrigeration cycle instead of dumping heat — the ideal is
~2.6 kg of ice off 100 Wh, or ~2.1 kg at an 80% circuit, three times the same-efficiency local yield.
Same mana, better physics: the whole thesis in one machine, first valuable to healers, caravans carrying
rare goods, and nobles rather than every household.

**Better mana-engine.** `motor.py`. Crank throw, flywheel, valve timing, compounding, gearing — the
mechanism the locals never optimize. The same Wh yields far more shaft-work than their build. Paired
with a **flywheel or raised-weight store** ([§13](power-system.md#motive-power--the-mana-engine)), it
banks work without mana decay. A raised weight has negligible standing loss; a flywheel still loses to
bearing drag and air.

**Exoskeleton.** Animation + force Projection ([§13](power-system.md#animation)), `animasyon.py`. A worn
animated frame that carries what the skeleton can't bear — the answer when flesh caps out. Costly to
run (a golem's full muscle-and-CPU bill), but it doesn't break you. He builds one when he has no other
way.

**Electric devices — the long game.** `elektrik.py`, [§23](power-system.md#23-open-threads).
Electricity is unknown in this world; no one thought to shape mana into *current*. The shock (100 mA
kills, ~30 kV/cm arc) is the least of it — the prize is what current unlocks: electrolysis, the
telegraph, electrochemistry, real measurement. Kaiser's alone, unwritten until the story reaches it.
