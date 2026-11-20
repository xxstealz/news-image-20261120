[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/xxstealz/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/xxstealz/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# news-image-20261120 — "The Daily Globe"

Sums up the world's news of **Friday 20 November 2026** in one image:
`entry.png` (1024×1024 PNG), drawn from scratch with code
(`draw_entry.py`, Python + PIL, no network, no external assets).

Six stories, verified 20 Nov 2026 from Reuters, CNN, ANI/PTI, IMD and
Sensor Tower estimates:

1. **Trump: no rush on Iran** — decision on Iran pushed to 2027
2. **Missiles rain on Kyiv** — mass missile attack overnight
3. **Dow sinks 1,101** — Wall Street's worst day in months; Anthropic's
   record $81.3bn IPO debuts (+17%)
4. **GTA VI: $2.36 billion** — first-day sales estimate, 24.6m copies
5. **Cyclone Akvan nears India** — ~300,000 evacuated in Odisha
6. **Tanker burns near Hormuz** — mine strike; Houthi claims on Saudi targets

Footer: Voyager 1 reaches one light-day; South Korea's exports top
$1 trillion; Genoa airport halts flights after drone sightings.

`main.ts` (Node 22, stdlib only) copies `entry.png` to
`/output/entry.png` — deterministic, two runs byte-identical.
