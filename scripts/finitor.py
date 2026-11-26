"""Generate the native Finitor draft with the supplied HTTPS asset directory."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("asset_base", help="HTTPS directory containing the files in assets/")
base = parser.parse_args().asset_base.rstrip("/")
parts = urlsplit(base)
if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or parts.query or parts.fragment:
    parser.error("provide an HTTPS asset directory")
red, pink, paper = "#AF0004", "#EE88AD", "#EAD3DC"

def image(key, filename, alt):
    return dict(id=key, type="image", url=f"{base}/{filename}", alt=alt)

def heading(key, text, level=2):
    return dict(id=key, type="heading", text=text, level=level)

def paragraph(key, text):
    return dict(id=key, type="text", text=text)

def button(key, text, target):
    return dict(id=key, type="button", text=text, url="#"+target)

def group(key, children, **style):
    return dict(id=key, type="container", children=children, style=style)

copy = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        "tempor incididunt ut labore et dolore magna aliqua.")
def page(slug, title, *nodes):
    return dict(id="wine-wench-"+slug, title=title, slug=slug, nodes=list(nodes))

home = page("home", "Home", image("hero-art", "home-body.webp",
    "Alana on the café terrace. For the LOVE of WINE. Wine Wench Approved."))
person = page("person", "The person", image("person-portrait", "person-body.webp",
    "Alana Kaye in turquoise, with the original pink artwork, introduction and Wine Wench seal."))
work = page("work", "The work", group("garden-scene", [
    button("partnerships", "Partnerships", "contact"), button("events", "Events", "contact")
], backgroundImage=base+"/garden-background.webp", minHeight=660, focalX=55, focalY=50,
   padding=72, gap=32, direction="column"),
    group("contact", [heading("contact-heading", "Contact Alana Kaye"),
        paragraph("contact-copy", "Contact details will appear here when supplied.")],
        padding=32, gap=12, background=red, color="#FFFFFF"))
articles = []
for key, title, category, excerpt, alt in [
    ("chardy", "Sip & Eat: Chardy & Fish Curry", "Wine & Food",
     'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."', "Food and wine on a table"),
    ("mudgee", "Weekender's Guide to Mudgee", "Travel & Adventures", copy, "An open country road")]:
    articles.append(group(key, [image(key+"-photo", key+".webp", alt),
                                paragraph(key+"-category", category), heading(key+"-title", title),
                                paragraph(key+"-credit", "By Alana Kaye\nJune 20, 2021"),
                                paragraph(key+"-excerpt", excerpt)], gap=12))
editorial = page("editorial", "Editorial", group("editorial-stories", articles,
               direction="row", background=paper, color=red, padding=48, gap=48))
# Omitting a custom header lets Finitor emit links relative to the actual
# draft or live route. Its custom header only accepts fixed URLs and anchors.
spec = dict(schemaVersion="1.0", name="Wine Wench · Alana Kaye",
            tokens=dict(primary=red, background=paper, text=red),
            presentation=dict(layout="full-width", bodyFont="humanist", headingFont="humanist", buttonRadius=12),
            pages=[home, person, work, editorial])
(Path(__file__).resolve().parents[1]/"deployer/site.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False)+"\n")
