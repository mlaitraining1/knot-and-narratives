import jinja2, os

SITE_URL = "https://knotandnarratives.com"  # placeholder — update to your real Vercel domain

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("/home/claude/build/templates"),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

PAGES = [
    dict(template="home.html", out="index.html", page_id="home", path="/", hero_page=True,
         title="The Knot & Narratives | Wedding Photography & Choreography, Bengaluru",
         meta_description="Wedding photography and wedding choreography studio based in Bengaluru, shooting destination weddings across India and abroad. One team, one story."),

    dict(template="portfolio.html", out="portfolio.html", page_id="portfolio", path="/portfolio.html", hero_page=True,
         title="Portfolio | The Knot & Narratives Wedding Photography",
         meta_description="Browse wedding, pre-wedding, choreography and destination wedding photography from The Knot & Narratives studio."),

    dict(template="stories.html", out="stories.html", page_id="stories", path="/stories.html", hero_page=True,
         title="Stories | The Knot & Narratives",
         meta_description="Real wedding stories, choreography briefs and behind-the-scenes notes from recent weddings shot and choreographed by The Knot & Narratives."),

    dict(template="story-single.html", out="story-single.html", page_id="stories", path="/story-single.html", hero_page=True,
         title="Ritika & Devansh — A Bengaluru Wedding Story | The Knot & Narratives",
         meta_description="How a sangeet number the bride swore she'd never agree to became the most-requested photographs from her three-day Bengaluru wedding."),

    dict(template="about.html", out="about.html", page_id="about", path="/about.html", hero_page=True,
         title="About | The Knot & Narratives",
         meta_description="Meet the studio behind The Knot & Narratives — a wedding photography and choreography team founded by Kabir Anand in Bengaluru."),

    dict(template="services.html", out="services.html", page_id="services", path="/services.html", hero_page=True,
         title="Services | Wedding Photography, Choreography & Films",
         meta_description="Wedding photography, wedding choreography, cinematic films, destination weddings and albums — explore every service offered by The Knot & Narratives."),

    dict(template="pricing.html", out="pricing.html", page_id="pricing", path="/pricing.html", hero_page=True,
         title="Pricing & Packages | The Knot & Narratives",
         meta_description="Wedding photography and choreography packages starting at ₹1,25,000, with custom quotes for multi-day and destination weddings."),

    dict(template="contact.html", out="contact.html", page_id="contact", path="/contact.html", hero_page=True,
         title="Contact | The Knot & Narratives",
         meta_description="Check availability for your wedding date. Based in Bengaluru, shooting weddings across India and abroad."),

    dict(template="gallery.html", out="gallery.html", page_id="gallery", path="/gallery.html", hero_page=True,
         title="Client Gallery | The Knot & Narratives",
         meta_description="Private client gallery portal for couples photographed by The Knot & Narratives."),
]

OUT_DIR = "/home/claude/site"

for page in PAGES:
    tpl = env.get_template(page["template"])
    html = tpl.render(site_url=SITE_URL, **page)
    with open(os.path.join(OUT_DIR, page["out"]), "w") as f:
        f.write(html)
    print("built", page["out"])

print("done")
