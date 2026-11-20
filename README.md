[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/fauzinfau4/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/fauzinfau4/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — Friday 20 November 2026

A one-page newspaper front page for Friday 20 November 2026, drawn
entirely in code with Pillow shapes and text. No photos, no downloaded
assets, no network calls — every pixel comes from the scripts in this repo.

## What's on the page

- **Lead story — Cyclone Akvan comes ashore.** The severe cyclone is due
  to cross the Odisha–Andhra coast near Gopalpur around noon IST, with
  winds of 90–100 km/h gusting to 110; about 300,000 people have been
  moved to safety and 423 rescue teams deployed.
- **COP31 enters its last day in Antalya.** No final text yet; a slimmed
  draft cut from 144 paragraphs to 80 drops every mention of fossil fuels
  and the $120bn adaptation figure. The text is due by midnight.
- **Phillips' hundred lifts New Zealand.** Glenn Phillips made 118 and
  Henry Nicholls carried his century to 128 not out as New Zealand passed
  300 on day two of the first Test against India.
- **Plus:** Modi opens the SCO Civilisational Dialogue Forum in New Delhi,
  Florida's floods roll into Friday with the St. Johns River at a record
  18.3 ft, GTA VI user reviews open at noon Pacific, and the COP31 draft
  in numbers — with a timeline of the day, a numbered world map, nine more
  briefs, and a date check that names the big 19 November stories this
  page deliberately leaves out.

## Layout

A cream paper masthead with the date, a statistics strip, three hero cards
(Akvan, COP31, Wellington), four smaller cards, a "Friday by the hours"
timeline, a numbered world map beside the briefs, and a DATE CHECK box
listing the previous day's stories that are not today's news.

## Run it

Render the poster:

```bash
python3 draw.py
```

That writes `entry.png` (1024×1024). Then ship it the way the grader
does:

```bash
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` only copies `entry.png` byte-for-byte into the output
directory; it does no rendering and no network access. Running it twice
produces identical bytes.

## Files

- `draw.py` — draws the whole front page with Pillow primitives.
- `main.py` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`).
- `entry.png` — the rendered 1024×1024 front page.
- `LICENSE` — MIT.

---

Built with [make.fun](https://make.fun/?ref=7tgjyx9m)
