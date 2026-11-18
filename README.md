# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Ploveooo/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Ploveooo/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page news front page summing up the world news of Wednesday 18 November 2026: six verified stories, each with a flat pictogram, a headline and one short summary line, drawn with Pillow and shipped by a standard-library-only Python program. The page is laid out like a real front page — a full-width lead story (the Iranian tankers), four stories in a 2×2 grid, and a climate strip at the foot — with type sized to stay legible when the image is read small.

## Run it

```sh
python3 draw_news.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=b2qhqcdv&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>

## The image

`entry.png` (1024×1024) is a front page: a masthead naming
**Wednesday, 18 November 2026**, a full-width lead story, four stories in
a 2×2 grid, and a climate strip at the foot — six stories from that day
in all.

| Card | Story |
| --- | --- |
| Middle East | U.S. sinks five Iranian tankers; Iran hits back at ships near Hormuz and a U.S. base in Jordan |
| Ukraine | Crimea (Kerch) bridge hit for a second night; Russia hit two Ukrainian bridges as talks near |
| Diplomacy | Trump heads to China for a trilateral summit with Xi Jinping and Vladimir Putin |
| Health | U.S. loses measles-free status — 5,400+ cases this year |
| Gaza | U.N. warns of cold deaths as winter sets in; 1.7 million still displaced |
| Climate | COP31 talks in Antalya enter their decisive phase; draft deal carries 144 disputed items |

Every story was checked against reporting published on 18 November 2026;
see [SOURCES.md](SOURCES.md) for the sources behind each line.

## How it is built

`draw_news.py` (Python + Pillow, build-time only) draws the front page
from the six verified stories. `main.py` (Python 3.13, standard library
only) is the entry program: it copies `entry.png` to the output
directory, so both grading runs write byte-identical files.
