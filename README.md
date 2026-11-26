# Wine Wench · Alana Kaye

A responsive static website and a native Finitor SiteSpec. Open the root with a static web server, for example `python3 -m http.server 8000`. The standalone version uses the supplied styleboard’s monogram, original photography, seal, palette and embedded letterforms.

## Content and browsing

Home, The person, The work, Editorial and Contact lead to the November 2026 inventory of the source site. The 26 editorial entries include local cover images, dates, introductory copy, category filtering and individual reading pages. The reader loads the original article on demand with a separate direct link. The Wix origin serves full articles, enquiries, newsletter subscriptions and booking availability. Keep that origin online while using those integrations. The standalone site includes directory-index aliases for the previous page and category paths. The Thirsty Hungry video uses the original media service.

## Editing

Edit `content/site.json` for services, contact and biography, and `content/journal.json` for stories. Run `python3 scripts/build.py` to generate the static pages. Images live under `assets/`. The Finitor generator takes a publicly readable, immutable HTTPS assets directory, including its journal/ subdirectory:

    python3 scripts/finitor.py https://raw.githubusercontent.com/AMStarks/WineWench/ASSET_COMMIT/assets

Bind AMStarks/WineWench in the target site's connections, then import the full GitHub commit SHA. Finitor imports deployer/site.json and uses native navigation, cards, category anchors, video and outbound links. CSS, JavaScript search and embedded Wix readers belong to the standalone build. Finitor links to full articles directly. Review the draft in Studio before publishing.
