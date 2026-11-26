# Wine Wench · Alana Kaye

Open index.html to view the responsive site. The four website compositions in the supplied styleboard map to Home, Work, Person and Editorial. The tall first sheet is the brand board. Original artwork and reference compositions are in assets/. Text, navigation, cards and buttons are HTML. The desktop layout follows the mockup dimensions. Small screens reflow for reading and touch. All static assets and fonts are local. No installation or build is required.

## Finitor

Bind AMStarks/WineWench to the website-only project and import the full Git commit SHA. The Studio import reads deployer/site.json. The manifest defines Home, The person, The work and Editorial as separate pages. The native navigation follows the draft route. Work buttons link to the on-page contact section. The native layout retains the original photography and artwork. It uses Finitor’s navigation, fonts, buttons and responsive columns. The standalone HTML has the four precisely composed pages. Finitor does not execute those files during native import.

The native draft expects publicly readable HTTPS image URLs. Its default URLs point to this repository at the asset commit. If this repository is private, host the assets directory on your designated public media origin and run the following before importing the resulting commit. A private GitHub read token lets Finitor read the manifest, but a visitor’s browser still needs access to the images.

    python3 scripts/finitor.py https://your-media-host.example/wine-wench/assets

No final biography, contact destination or full articles were supplied. The mockup copy and article excerpts are retained. Contact and work controls open informational previews. Article controls open an excerpt. Replace these in the relevant HTML and native draft for launch.
