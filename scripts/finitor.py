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
    return dict(id=key, type="button", text=text, url=target)

def group(key, children, **style):
    return dict(id=key, type="container", children=children, style=style)

root = Path(__file__).resolve().parents[1]
site = json.loads((root/"content/site.json").read_text())
posts = json.loads((root/"content/journal.json").read_text())
live = site["live"]
mail = "mailto:"+site["email"]
def page(slug, title, *nodes):
    return dict(id="wine-wench-"+slug, title=title, slug=slug, nodes=list(nodes))

def feature(post):
    key = post["slug"]
    return group(key, [
        image(key+"-photo", "journal/"+key+".webp", post["title"]),
        paragraph(key+"-category"," · ".join(post["categories"])),
        heading(key+"-title",post["title"]), paragraph(key+"-credit","Alana Kaye · "+post["date"]),
        paragraph(key+"-intro",post["summary"]), button(key+"-read","Read full story",post["url"])
    ],gap=12,padding=20,background=paper,color=red)

def rows(items):
    return [group("stories-"+str(i),[feature(p) for p in items[i:i+2]],
                  direction="row",padding=32,gap=36,background=paper) for i in range(0,len(items),2)]

signup = button("newsletter","Join the Wine Wench Wine Up",live+"/#comp-jt4912ss")
home = page("home","Home", image("hero-art","journal/home-hero.webp","Alana Kaye on a café terrace. For the LOVE of WINE."),
            group("intro",[paragraph("home-copy","Australian wines, the people behind the bottle, and something delicious to eat alongside."),heading("latest","Latest from Alana")],padding=32),
            *rows(posts[:4]),signup)
person = page("person","The person",image("portrait","journal/person-hero.webp","Alana Kaye in turquoise with the Wine Wench seal."),
              group("biography",[heading("person-title","Meet Alana",1)]+[paragraph("bio-"+str(i),p) for i,p in enumerate(site["bio"])],gap=16,padding=40),
              group("thirsty-hungry",[heading("series-title","Thirsty Hungry"),paragraph("series-intro",site["series"]),
                    dict(id="series-video",type="video",url=site["video"],text="Thirsty Hungry",alt="Alana’s food and wine pairing series"),
                    button("series-link","Visit the series",live+"/copy-of-about")],gap=16,padding=40))
work = page("work","The work",
    group("garden-scene",[button("work-services","Partnerships","#partnerships"),button("work-events","Events","#events")],
          backgroundImage=base+"/garden-background.webp",minHeight=660,padding=72,gap=32),
    group("partnerships",[heading("services-title","Partnerships & collaborations",1)]+[
      group("service-"+str(i),[heading("service-name-"+str(i),name),paragraph("service-desc-"+str(i),desc)],gap=8)
      for i,(name,desc) in enumerate(site["services"])]+[button("rates","Request a rates card",mail)],padding=40,gap=24),
    group("packages",[heading("packages-title","Social media packages")]+[
      group("package-"+str(i),[heading("package-name-"+str(i),name+" · $"+str(price)+" / month"),
         paragraph("includes-"+str(i),f"{ig} Instagram posts, {fb} Facebook posts and {stories} stories weekly."+
          (f" Monthly reels included: {reels}." if reels else ""))],gap=8)
      for i,(name,price,ig,fb,stories,reels) in enumerate(site["packages"])]+[paragraph("setup",site["setup"])],padding=40,gap=24),
    group("events",[heading("events-title","Events & at-home tastings"),paragraph("tastings",site["tastings"]),
        button("enquiry","Tasting enquiry",live+"/at-home-tastings#comp-l0ejj03y"),heading("bookings-title","Tours & bookings"),
        paragraph("availability","The published calendar currently lists no services. Enquire about future dates."),
        button("bookings","Check the booking calendar",live+"/book-online"),button("tours","Visit the tours page",live+"/tours")],padding=40,gap=16))
editorial = page("editorial","Editorial",group("archive-title",[heading("journal-title","Editorial",1),
   button("contents-link","Browse by category","#categories")],padding=32,gap=12),*rows(posts))
categories=sorted({c for p in posts for c in p["categories"]})
editorial["nodes"].append(group("categories",[heading("category-index","Browse by category")]+[
    group("category-"+str(i),[heading("label-"+str(i),name)]+[button("pick-"+str(i)+"-"+str(j),p["title"],"#"+p["slug"])
    for j,p in enumerate(posts) if name in p["categories"]],gap=8) for i,name in enumerate(categories)],gap=24,padding=40))
contact = page("contact","Contact",group("contact-info",[heading("contact-title","Contact Alana",1),
    paragraph("contact-intro","For collaborations, interviews, tastings or a question about a bottle, get in touch with Alana."),
    button("email",site["email"],mail),button("form","Open the contact form",live+"/contact#comp-l0ekx094"),
    button("instagram","Instagram",site["instagram"]),button("facebook","Facebook",site["facebook"]),signup],padding=48,gap=20))
spec=dict(schemaVersion="1.0",name="Wine Wench · Alana Kaye",
          tokens=dict(primary=red,background=paper,text=red),
          presentation=dict(layout="full-width",bodyFont="humanist",headingFont="humanist",buttonRadius=12),
          footer=dict(text="Alana Kaye · The Wine Wench", links=[dict(text=t,url=u) for t,u in [
            ("Instagram",site["instagram"]),("Facebook",site["facebook"]),("Newsletter",live+"/#comp-jt4912ss"),("Email Alana",mail)]]),
          pages=[home,person,work,editorial,contact])
(root/"deployer/site.json").write_text(json.dumps(spec,indent=2,ensure_ascii=False)+"\n")
