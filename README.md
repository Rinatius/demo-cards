# News Cards

A static site that turns news research into short, sourced cards.

- `index.html` renders a topic's cards (`?topic=<id>`, defaults to the first topic).
- `cards/topics.json` lists the topics.
- `cards/<topic>/cards.json` holds the cards; `cards.md` is the same set for reading.

Card fields: `id`, `category`, `headline` (under 70 chars), `body` (1 to 3 sentences), `source` (`name`, `url`), `date`, `confidence` (`confirmed` or `reported`; reported cards show a *Reported* tag).

Preview locally with `python3 -m http.server` and open http://localhost:8000. It also works as-is on GitHub Pages.
