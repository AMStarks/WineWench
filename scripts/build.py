"""Build the standalone website from the same editorial records as the Finitor draft."""
import json
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote
ROOT = Path(__file__).resolve().parents[1]
S = json.loads((ROOT/'content/site.json').read_text())
POSTS = json.loads((ROOT/'content/journal.json').read_text())
LIVE = S['live']
LABELS = [('person.html','the person'),('work.html','the work'),('editorial.html','editorial'),('contact.html','contact')]
def h(value): return escape(str(value), quote=True)
def link(url, label, cls=''): return f'<a class="{cls}" href="{h(url)}">{h(label)}</a>'
def pill(url, label): return link(url, label, 'action')
def paragraph(text): return f'<p>{h(text)}</p>'
def title(text): return f'<h2>{h(text)}</h2>'
def art(name, alt, cls=''): return f'<img class="{cls}" src="assets/{name}" alt="{h(alt)}">'
def pack(row):
    name,price,ig,fb,stories,reels=row
    return (f'{ig} Instagram posts, {fb} Facebook posts and {stories} stories each week.'
            + (f' Includes {reels} '+('reel' if reels == 1 else 'reels')+' per month.' if reels else ''))
def stamp(p):
    d=date.fromisoformat(p['date'])
    return f'{d.day} {d:%B %Y}'
def page(file, name, body, cls='', prefix=''):
    nav=''.join(f'<a href="{prefix}{url}"'+(' aria-current="page"' if url==file else '')+f'>{txt}</a>' for url,txt in LABELS)
    footer=f'''<footer class="base"><div><h2>The Wine Wench Wine Up</h2><p>Get Alana’s wine news by email.</p>{pill(LIVE+'/#comp-jt4912ss','Join the mailing list')}</div><div>{link(prefix+'contact.html','Contact Alana')}{link('mailto:'+S['email'],S['email'])}{link(S['instagram'],'Instagram')}{link(S['facebook'],'Facebook')}</div></footer>'''
    markup=f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{h(name)} · The Wine Wench</title><link rel="icon" href="{prefix}assets/monogram.svg"><link rel="stylesheet" href="{prefix}site.css"><script src="{prefix}site.js" defer></script></head>
<body class="scene {cls}"><a class="skip" href="#main">Skip to content</a><header class="masthead"><a class="brand" href="{prefix}index.html" aria-label="Alana Kaye home"><img src="{prefix}assets/monogram.svg" alt="AK"></a><nav aria-label="Main navigation">{nav}</nav></header><main id="main">{body}</main>{footer}</body></html>'''
    f=ROOT/file;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(markup+'\n')
def stage(kind, lead):
    pics={'home':('terrace','Alana on a café terrace'),'person':('portrait','Alana wearing sunglasses'),'work':('garden','Alana in a flower garden')}
    img,alt=pics[kind]
    tag={'home':'For the LOVE of WINE','person':'Meet Alana','work':'The work'}[kind]
    overlay=(f'<h1 class="sr">{tag}</h1><div class="work-options">{link("#partnerships","Partnerships")}{link("#events","Events")}</div>' if kind=='work' else f'<div class="intro"><h1>{tag}</h1>{paragraph(lead)}</div>')
    return f'<div class="stage">{art(img+".webp",alt,"photo")}<div class="pattern"></div><div class="panel"></div>{art("approval.svg","Wine Wench Approved","seal")}{overlay}</div>'
def card(p):
    url='post/'+p['slug']+'/index.html'
    return f'''<article class="card" data-categories="{h('|'.join(p['categories']))}"><a href="{url}" tabindex="-1" aria-hidden="true"><img loading="lazy" src="assets/journal/{p['slug']}.webp" alt=""></a><p class="kicker">{h(' · '.join(p['categories']))}</p><h2>{link(url,p['title'])}</h2><p class="credit">Alana Kaye · <time datetime="{p['date']}">{stamp(p)}</time></p>{paragraph(p['summary'])}{pill(url,'Read story')}</article>'''
def block(content,id=''):
    return f'<section class="spread"'+(f' id="{id}"' if id else '')+f'><div>{content}</div></section>'
def grid(posts): return '<div class="journal-grid">'+''.join(card(p) for p in posts)+'</div>'
page('index.html','Home',stage('home','Australian wines, the people behind the bottle, and something delicious to eat alongside.')+
     block(title('Latest from Alana')+grid(POSTS[:4])+pill('editorial.html','Explore all stories')),'home')
series=title('Thirsty Hungry')+paragraph(S['series'])+f'<video controls playsinline preload="none" aria-label="Thirsty Hungry food and wine video" src="{S["video"]}"></video>'+pill(LIVE+'/copy-of-about','Visit the series')
page('person.html','The person',stage('person','Wine writer, storyteller and Southern Highlands local. Pull up a chair.')+block(title('Alana Kaye')+''.join(map(paragraph,S['bio']))+pill('editorial.html','Read Alana’s stories'))+block(series,'thirsty-hungry'),'person')
services=''.join('<article>'+title(n)+paragraph(t)+'</article>' for n,t in S['services'])
packages=''.join(f'<article><h3>{h(p[0])}</h3><strong>${p[1]} / month</strong>{paragraph(pack(p))}</article>' for p in S['packages'])
page('work.html','Partnerships, collaborations & events',stage('work','')+block(title('Partnerships & collaborations')+'<div class="offers">'+services+'</div>'+pill('mailto:'+S['email'],'Request a rates card'),'partnerships')+block(title('Social media packages')+'<div class="offers">'+packages+'</div>'+paragraph(S['setup'])+pill('contact.html','Discuss a package'),'packages')+block(title('Events & at-home tastings')+paragraph(S['tastings'])+pill(LIVE+'/at-home-tastings#comp-l0ejj03y','Tasting enquiry')+title('Tours & bookings')+paragraph('The booking calendar currently lists no services. Check with Alana about future dates.')+pill(LIVE+'/book-online','Check the booking calendar')+link(LIVE+'/tours','Visit the tours page','text-link'),'events'),'work')
contact=title('Get in touch')+paragraph('For collaborations, interviews, tastings or a question about a bottle, get in touch with Alana.')+pill(LIVE+'/contact#comp-l0ekx094','Open the contact form')+link('mailto:'+S['email'],S['email'],'text-link')+title('Follow Alana')+pill(S['instagram'],'Instagram')+pill(S['facebook'],'Facebook')
page('contact.html','Contact','<div class="paper inner"><h1>Contact Alana</h1>'+contact+'</div>','sub')
categories=sorted(set(x for p in POSTS for x in p['categories']))
filters='<form class="filters" role="search"><label>Find a story<input type="search" name="q" placeholder="Wine, place or winemaker"></label><label>Category<select name="category"><option value="">All stories</option>'+''.join(f'<option>{h(c)}</option>' for c in categories)+'</select></label><button type="reset">Clear</button></form><p class="count" role="status"></p>'
page('editorial.html','Editorial','<div class="paper inner"><h1>Editorial</h1>'+filters+grid(POSTS)+'</div>','sub')
for p in POSTS:
    article=f'''<article class="paper inner reader"><a class="back" href="../../editorial.html">All stories</a><p class="kicker">{h(' · '.join(p['categories']))}</p><h1>{h(p['title'])}</h1><p class="credit">Alana Kaye · {stamp(p)}</p><img class="cover" src="../../assets/journal/{p['slug']}.webp" alt=""><p class="lede">{h(p['summary'])}</p>
    <div class="original"><h2>Read the full story</h2>{link(p['url'],'Open the original article','text-link')}
    <iframe loading="lazy" title="{h(p['title'])} — original article" src="{h(p['url'])}#content-wrapper" referrerpolicy="strict-origin-when-cross-origin"></iframe></div></article>'''
    page('post/'+p['slug']+'/index.html',p['title'],article,'sub','../../')

# Keep bookmarks to the existing website working on static directory-index hosts.
aliases = {'about':'person.html', 'blog':'editorial.html', 'contact':'contact.html',
           'partnerships-and-collaborations':'work.html#partnerships', 'social-media-packages':'work.html#packages',
           'at-home-tastings':'work.html#events', 'book-online':'work.html#events', 'tours':'work.html#events',
           'copy-of-about':'person.html#thirsty-hungry', 'profile/larnza/profile':'person.html',
           'post/the-rosé-revolution':'post/the-rose-revolution/index.html'}
for key, label in [('tips-tricks','Tips & tricks'),('news-trends','News & trends'),('recpies','Recipes'),
                   ('articles','Articles'),('interviews','Interviews'),('reviews','Reviews'),
                   ('nsw','NSW'),('sa','SA'),('qld','QLD'),('vic','VIC'),('wa','WA')]:
    aliases['blog/categories/'+key]='editorial.html?category='+quote(label)
for alias, target in aliases.items():
    f=ROOT/alias/'index.html';f.parent.mkdir(parents=True,exist_ok=True)
    href=h('../'*(1+alias.count('/'))+target)
    f.write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={href}"><title>The Wine Wench</title><a href="{href}">Continue to The Wine Wench</a></html>\n')
