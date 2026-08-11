#!/usr/bin/env python3
"""Static site generator for Alex Chen's engineering portfolio.
Run: python3 build.py   -> writes *.html into the site root.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------
# NAV / SITE CONSTANTS
# ------------------------------------------------------------------
NAV = [
    ("index.html", "Home"),
    ("moonshine.html", "Moonshine"),
    ("vesper.html", "Vesper"),
    ("testing.html", "Testing"),
    ("riptide.html", "Riptide"),
    ("lander-jr.html", "Lander Jr"),
    ("boeing.html", "Boeing"),
    ("robot.html", "Robot"),
    ("research.html", "Research"),
    ("misc.html", "Misc"),
]

EMAIL = "alexanderchenla@gmail.com"
PHONE = "+1 (562) 474-3788"
SITE_TITLE = "Alexander Chen — Mechanical Engineering Portfolio"

# ------------------------------------------------------------------
# ICONS (inline SVG, line style, used for pages without photography)
# ------------------------------------------------------------------
ICONS = {
"factory": '''<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 56V28l14 9V28l14 9V20l14 9v27H6Z"/><path d="M48 56V38h10v18"/><circle cx="53" cy="30" r="2.4" fill="currentColor" stroke="none"/><path d="M6 56h52"/></svg>''',
"robot": '''<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="16" y="10" width="32" height="24" rx="4"/><circle cx="25" cy="21" r="2.6" fill="currentColor" stroke="none"/><circle cx="39" cy="21" r="2.6" fill="currentColor" stroke="none"/><path d="M32 4v6M12 34v10h40V34M18 44v14M46 44v14M24 58h4M36 58h4"/><path d="M6 20l10 4M58 20l-10 4"/></svg>''',
"molecule": '''<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="18" r="6"/><circle cx="46" cy="14" r="5"/><circle cx="48" cy="42" r="6.5"/><circle cx="16" cy="46" r="4.5"/><path d="M23 21l19-5M22 22l21 17M20 24l-2 18M44 18l3 20"/></svg>''',
"plane": '''<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 34 58 12 36 58l-6-18-18-6Z"/><path d="M30 40 58 12"/></svg>''',
"rocket": '''<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M32 6c8 6 12 16 12 28 0 4-1 9-3 13h-18c-2-4-3-9-3-13 0-12 4-22 12-28Z"/><path d="M26 40l-8 4v10l8-6M38 40l8 4v10l-8-6"/><circle cx="32" cy="24" r="4"/><path d="M27 47c-1 5-1 9 5 11 6-2 6-6 5-11"/></svg>''',
}

# ------------------------------------------------------------------
# SHARED TEMPLATE PIECES
# ------------------------------------------------------------------

def head(title, desc, current):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,{ICONS['rocket'].replace('currentColor','%2355CFFF').replace('#','%23')}">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body>
'''

def nav(current):
    items = ""
    for href, label in NAV:
        cls = "current" if href == current else ""
        items += f'<li><a class="{cls}" href="{href}">{label}</a></li>\n'
    return f'''<nav class="site-nav">
  <div class="wrap">
    <a class="brand" href="index.html">
      <span class="name">ALEXANDER CHEN</span>
      <span class="role">Mechanical Engineering · UCSD</span>
    </a>
    <ul class="nav-links">
      {items}
    </ul>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</nav>
'''

def footer():
    return f'''<footer>
  <div class="wrap footer-row">
    <span class="fmono">&copy; <span id="y"></span> Alexander Chen — built with hairline rules and hand-poured static fires.</span>
    <div class="foot-links">
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="tel:{PHONE.replace(' ','').replace('(','').replace(')','')}">{PHONE}</a>
    </div>
  </div>
</footer>
<div class="lightbox" id="lightbox">
  <button class="lightbox-close" aria-label="Close">
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
  </button>
  <img src="" alt="">
  <div class="lightbox-cap"></div>
</div>
<script>document.getElementById('y').textContent = new Date().getFullYear();</script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''

def placards(items):
    """items: list of (value, label) tuples"""
    out = '<div class="placards reveal">\n'
    for val, lbl in items:
        out += f'  <div class="placard"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>\n'
    out += '</div>\n'
    return out

def bullets(items):
    out = '<ul class="bullets">\n'
    for it in items:
        out += f'  <li>{it}</li>\n'
    out += '</ul>\n'
    return out

def gallery(items):
    """items: list of (imgpath, caption)"""
    out = '<div class="gallery reveal">\n'
    for img, cap in items:
        out += f'''  <figure>
    <img src="{img}" alt="{cap}" loading="lazy">
    <figcaption>{cap}</figcaption>
  </figure>
'''
    out += '</div>\n'
    return out

def sidebar(role, tools, team, related):
    """related: list of (href, label)"""
    rel_html = "".join(f'<a class="related-link" href="{h}">{l} &rarr;</a>' for h, l in related)
    return f'''<aside class="sidebar reveal">
  <h4>Project Info</h4>
  <dl>
    <dt>Role</dt><dd>{role}</dd>
    <dt>Tools</dt><dd>{tools}</dd>
    <dt>Team</dt><dd>{team}</dd>
  </dl>
  {rel_html}
</aside>
'''

def pager(prev, nxt):
    ph, pl = prev
    nh, nl = nxt
    return f'''<div class="proj-pager">
  <a class="prev" href="{ph}">
    <span class="pager-lbl">&larr; Previous</span>
    <span class="pager-title">{pl}</span>
  </a>
  <a class="next" href="{nh}">
    <span class="pager-lbl">Next &rarr;</span>
    <span class="pager-title">{nl}</span>
  </a>
</div>
'''

def write(fname, html):
    with open(os.path.join(ROOT, fname), "w") as f:
        f.write(html)
    print("wrote", fname)

PAGE_TITLES = dict((h, l) for h, l in NAV)

def pagerow(current):
    """auto prev/next based on NAV order"""
    hrefs = [h for h, _ in NAV]
    i = hrefs.index(current)
    prev_h = hrefs[i-1] if i > 0 else hrefs[-1]
    next_h = hrefs[(i+1) % len(hrefs)]
    return pager((prev_h, PAGE_TITLES[prev_h]), (next_h, PAGE_TITLES[next_h]))


# ==================================================================
# HOME PAGE
# ==================================================================

def project_card(href, tag, title, desc, chips, img=None, icon=None):
    if img:
        media = f'''<div class="pcard-media">
      <img src="{img}" alt="{title}" loading="lazy">
      <span class="pcard-tag">{tag}</span>
    </div>'''
    else:
        media = f'''<div class="pcard-media noimg">
      {ICONS.get(icon,'')}
      <span class="pcard-tag">{tag}</span>
    </div>'''
    chip_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    return f'''<a class="pcard reveal" href="{href}">
    {media}
    <div class="pcard-body">
      <h3>{title}</h3>
      <p>{desc}</p>
      <div class="pcard-specs">{chip_html}</div>
      <span class="pcard-link">View project <span class="btn-arrow">&rarr;</span></span>
    </div>
  </a>
'''

def build_index():
    html = head(SITE_TITLE, "Mechanical engineering portfolio of Alexander Chen — liquid rocket propulsion, structures, and materials science at UC San Diego.", "index.html")
    html += nav("index.html")

    html += f'''<header class="hero">
  <div class="hero-media">
    <img src="assets/img/testing-static-fire-wide.jpg" alt="Full-vehicle static fire of the Moonshine engine on Vesper, desert test stand">
  </div>
  <div class="hero-content wrap">
    <span class="eyebrow">Mechanical Engineering · UC San Diego</span>
    <h1>Alexander Chen</h1>
    <p class="lede">I design, machine, and static-fire the hardware that has to survive its own worst day &mdash; liquid rocket engines, propellant feed systems, and the ground equipment that operates them. Propulsion &amp; structures at SEDS UCSD; soft-materials research at the Cai Group.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="#projects">View Projects <span class="btn-arrow">&rarr;</span></a>
      <a class="btn" href="mailto:{EMAIL}">Get in Touch</a>
    </div>
    {placards([
        ("600<span>lbf</span>", "Thrust Chamber"),
        ("275<span>psi</span>", "Chamber Pressure"),
        ("3500<span>psi</span>", "COPV Pressurant"),
        ("&gt;80<span>%</span>", "C* Efficiency"),
        ("5+", "Static Fire Ops"),
    ])}
  </div>
</header>

<section id="about">
  <div class="wrap">
    <div class="two-col">
      <div class="reveal">
        <span class="eyebrow">About</span>
        <h2>Second-year ME with a habit of finishing what CAD starts.</h2>
        <p class="lede">I'm a Mechanical Engineering student at UCSD interested in mechanical, aerospace, and materials science work. I'm a member of the propulsion team at SEDS UCSD, responsible for the design and test of engines, propellant feed systems, and launch vehicles &mdash; and a member of the Cai Group, a materials science lab researching liquid crystal elastomers (LCEs) for robotics and medical applications.</p>
      </div>
      <div class="skills-grid reveal" style="align-self:stretch;">
        <div class="skill-col">
          <span class="eyebrow">Design &amp; Analysis</span>
          <ul>
            <li>CAD &amp; GD&amp;T</li>
            <li>Finite Element Analysis</li>
            <li>SolidWorks · Fusion 360</li>
            <li>AutoCAD · Ansys</li>
          </ul>
        </div>
        <div class="skill-col">
          <span class="eyebrow">Manufacturing</span>
          <ul>
            <li>Manual &amp; CNC lathe / mill</li>
            <li>3D printing</li>
            <li>Drill press · bandsaw</li>
            <li>Laser cutting</li>
          </ul>
        </div>
        <div class="skill-col">
          <span class="eyebrow">Materials Research</span>
          <ul>
            <li>Soft material testing</li>
            <li>Composite layups</li>
            <li>Creep &amp; mechanical characterization</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="divider">

<section id="projects">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Selected Work</span>
        <h2>Projects</h2>
      </div>
      <p>Nine projects spanning liquid propulsion, vehicle structures, GNC test hardware, and materials research &mdash; each built, machined, or tested first-hand.</p>
    </div>
    <div class="project-grid">
      {project_card("moonshine.html", "Propulsion", "Moonshine Engine Chamber", "600 lbf film-cooled LOX/IPA thrust chamber and nozzle, sized in CEA and machined in-house.", ["600 LBF","275 PSI","STAINLESS"], img="assets/img/moonshine-nozzle-desk.jpg")}
      {project_card("vesper.html", "Propellant Systems", "Vesper — LOX/IPA Rocket", "Full propellant feed system and ground support equipment for a LOX/IPA sounding rocket.", ["FILL/VENT/MAIN/PRESS","GSE"], img="assets/img/vesper-workshop-table.jpg")}
      {project_card("testing.html", "Test &amp; Validation", "Static Fire Testing", "Hydrostatic proof, cryo cold flow, and 5+ static fire campaigns as pad technician.", ["3 STATIC FIRES","&gt;80% C*"], img="assets/img/testing-static-fire-stand.jpg")}
      {project_card("riptide.html", "Structures", "Riptide — LOX/LNG Lander", "Structures and landing-leg manufacturing for a bi-propellant sounding vehicle built for powered landings.", ["LOX-LNG","LANDING LEGS"], img="assets/img/riptide-lathe-footpad.jpg")}
      {project_card("lander-jr.html", "GNC Test Stand", "Lander Jr", "Propeller-driven test stand emulating a landing rocket's dynamics for GNC development.", ["LIDAR","AVIONICS BAY"], img="assets/img/landerjr-teststand-cad.jpg")}
      {project_card("boeing.html", "Industry", "Boeing Internship", "Factory layout design for the ORCA XLUUV program, plus a 3D-printed shop-safety fix.", ["FACTORY LAYOUT","SAFETY"], icon="factory")}
      {project_card("robot.html", "Competition", "Golden Oreo Robot", "A cascading-lift competition robot built in a month, FRC-style.", ["LIFT MECHANISM","1-MONTH BUILD"], icon="robot")}
      {project_card("research.html", "Materials Science", "Cai Group Research", "Creep testing of liquid crystal elastomers and design of a tremor-mimicking hand.", ["LCE","SOFT ROBOTICS"], icon="molecule")}
      {project_card("misc.html", "Writing", "Misc — Instructables", "An Autodesk-featured guide to modeling true-to-scale aircraft from 3-view drawings.", ["AUTODESK AMBASSADOR"], icon="plane")}
    </div>
  </div>
</section>

<section class="contact-band" id="contact">
  <div class="wrap reveal">
    <span class="eyebrow">Get in Touch</span>
    <h2>Building something that needs to fly, machine, or hold pressure?</h2>
    <p class="lede">I'm always glad to talk propulsion, manufacturing, or materials &mdash; reach out by email or phone.</p>
    <div class="contact-links">
      <a class="btn btn-primary" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="btn" href="tel:{PHONE.replace(' ','').replace('(','').replace(')','')}">{PHONE}</a>
    </div>
  </div>
</section>
'''
    html += footer()
    write("index.html", html)


# ==================================================================
# GENERIC PROJECT-PAGE BUILDER
# ==================================================================

def project_page(fname, current, eyebrow, title, lede, hero_img=None, hero_render=None, hero_icon=None,
                  spec_items=None, sections=None, gallery_items=None, side=None, note=None):
    desc = lede.replace('&mdash;','-').replace('&amp;','and')[:150]
    html = head(f"{title} — Alexander Chen", desc, current)
    html += nav(current)

    # hero
    if hero_img:
        html += f'''<header class="phero">
  <div class="phero-media"><img src="{hero_img}" alt="{title}"></div>
  <div class="phero-content wrap">
    <a class="back-link" href="index.html#projects">&larr; All Projects</a>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</header>
'''
    elif hero_render:
        html += f'''<header class="phero render-hero">
  <div class="grid-bg"></div>
  <div class="phero-render-frame"><img src="{hero_render}" alt="{title} CAD render"></div>
  <div class="phero-content wrap">
    <a class="back-link" href="index.html#projects">&larr; All Projects</a>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</header>
'''
    else:
        icon_svg = ICONS.get(hero_icon, "")
        html += f'''<header class="phero noimg">
  <div class="grid-bg"></div>
  <div class="phero-icon-frame">{icon_svg}</div>
  <div class="phero-content wrap">
    <a class="back-link" href="index.html#projects">&larr; All Projects</a>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</header>
'''

    if spec_items:
        html += f'<section class="spec-row"><div class="wrap">{placards(spec_items)}</div></section>\n'

    html += '<section><div class="wrap"><div class="two-col">\n<div class="content-block reveal">\n'
    for sec in sections:
        html += f"<h2>{sec['h']}</h2>\n"
        if sec.get('p'):
            html += f"<p>{sec['p']}</p>\n"
        if sec.get('bullets'):
            html += bullets(sec['bullets'])
        if sec.get('quote'):
            html += f'<div class="quote-block">{sec["quote"]}</div>\n'
    if note:
        html += f'<p class="small" style="margin-top:24px;">{note}</p>\n'
    html += '</div>\n'
    html += side
    html += '</div></div></section>\n'

    if gallery_items:
        html += f'''<section style="padding-top:0;">
  <div class="wrap">
    <span class="eyebrow">Gallery</span>
    {gallery(gallery_items)}
  </div>
</section>
'''

    html += pagerow(current)
    html += footer()
    write(fname, html)


# ==================================================================
# INDIVIDUAL PROJECT PAGES
# ==================================================================

def build_moonshine():
    project_page(
        "moonshine.html", "moonshine.html",
        "Project · Propulsion", "Moonshine Engine Chamber",
        "A 600&nbsp;lbf, 275&nbsp;psi stainless-steel film-cooled thrust chamber and nozzle for a LOX/IPA bipropellant engine &mdash; sized in NASA's CEA, tuned for injector stiffness, and machined start to finish in the SEDS UCSD shop.",
        hero_img="assets/img/moonshine-nozzle-desk.jpg",
        spec_items=[("600<span>lbf</span>","Thrust"),("275<span>psi</span>","Chamber Pressure"),("Film-<span>cooled</span>","Cooling"),("LOX<span>/ IPA</span>","Propellants"),("17-4<span>SS</span>","Material")],
        sections=[
            {"h":"Design", "bullets":[
                "Owned the design of the thrust chamber and nozzle, sized for 600&nbsp;lbf thrust at 275&nbsp;psi chamber pressure.",
                "Used MATLAB's combustion toolbox, interfacing with NASA's CEA, to size throat area and nozzle expansion ratio.",
                "Ran many design iterations to land on a target injector stiffness &mdash; balancing pressure drop against throttling range, shown in the 1C throttle map below.",
            ]},
            {"h":"Manufacturing", "bullets":[
                "Manufactured the flange, chamber, nozzle, and propellant manifold on manual and CNC lathes and mills.",
                "Built CAM toolpaths in Fusion 360 to drive CNC manufacturing of the chamber and nozzle.",
            ]},
        ],
        gallery_items=[
            ("assets/img/moonshine-throttle-map.jpg","1C throttle map — pressure, injector stiffness, mass flow, and corrected Isp vs. thrust"),
            ("assets/img/moonshine-flange-inspection.jpg","Inspecting a machined flange"),
            ("assets/img/moonshine-manual-lathe.jpg","Manual lathe work on chamber stock"),
            ("assets/img/moonshine-cnc-mill.jpg","CNC milling the nozzle profile"),
        ],
        side=sidebar("Design lead, manufacturing", "MATLAB + NASA CEA, Fusion 360 CAM, manual &amp; CNC lathe/mill", "SEDS UCSD Propulsion",
                      [("testing.html","See it static-fired"), ("vesper.html","The rocket it flies on")]),
    )

def build_vesper():
    project_page(
        "vesper.html", "vesper.html",
        "Project · Propellant Systems", "Vesper — LOX/IPA Rocket",
        "A liquid oxygen / isopropyl alcohol sounding rocket built to fly the Moonshine engine. I designed, built, and tested the full propellant feed system and the ground support equipment used to operate it.",
        hero_img="assets/img/vesper-workshop-table.jpg",
        spec_items=[("LOX<span>/ IPA</span>","Propellants"),("Fill·Vent","Main·Press"),("Pneumatic","GSE Actuation"),("COPV","Pressurant Fed")],
        sections=[
            {"h":"Propellant Feed System", "bullets":[
                "Designed, manufactured, integrated, and tested the full propellant feed system, including the fill, vent, main, and pressurization valves for the fuel and oxidizer tanks.",
                "Ran finite element analysis on structural components to confirm margins under flight and ground-test loads before machining.",
            ]},
            {"h":"Ground Support Equipment", "bullets":[
                "Built and tested Ground Support Equipment for pneumatic actuation of vehicle valves and regulation of tank pressure.",
                "Generated CNC toolpaths and machined GSE hardware in the SEDS UCSD shop.",
            ]},
        ],
        gallery_items=[
            ("assets/img/vesper-cad-render.jpg","Vesper airframe, CAD"),
            ("assets/img/vesper-vehicle-integration.jpg","Fully integrated vehicle ahead of static fire"),
            ("assets/img/vesper-fea-analysis.jpg","FEA on a GSE actuation bracket"),
            ("assets/img/vesper-cnc-screen.jpg","Cutting GSE hardware on the CNC mill"),
        ],
        side=sidebar("Propellant systems, GSE", "SolidWorks, Ansys FEA, Fusion 360 CAM", "SEDS UCSD Propulsion",
                      [("moonshine.html","The engine it flies"), ("testing.html","Static fire &amp; test campaign")]),
    )

def build_testing():
    project_page(
        "testing.html", "testing.html",
        "Project · Test &amp; Validation", "Moonshine &amp; Vesper — Static Fire Testing",
        "Getting a rocket engine from CAD to a repeatable static fire means proving every system before it sees flight-like pressure. The test campaign for the Moonshine engine and Vesper vehicle, from hydrostatic proof through pad operations.",
        hero_img="assets/img/testing-static-fire-wide.jpg",
        spec_items=[("3","Static Fires"),("&gt;80<span>%</span>","C* Efficiency"),("5+","Pad Ops"),("3500<span>psi</span>","COPV Pressurant"),("1.5&times;","MEOP Hydro Proof")],
        sections=[
            {"h":"Engine Testing", "bullets":[
                "Conducted a hydrostatic proof test, vehicle integration, and 3 successful static fires at different mixture ratios for the LOX/IPA engine.",
                "Calculated a &gt;80% c* efficiency from chamber pressure and water-flow-rate data recorded during static fire.",
                "Conducted manifold and injector water flow tests to determine discharge coefficients (CdA) from pressure transducer and turbine flow meter data.",
            ]},
            {"h":"Vehicle &amp; Pad Operations", "bullets":[
                "Performed pad technician operations across 5+ static fire attempts.",
                "Validated engine and rocket fluid systems through successful full-vehicle static fires of the 600&nbsp;lbf film-cooled engine, run on a COPV-fed pressurant system at 3500&nbsp;psi.",
                "Developed and conducted a hydrostatic proof test on the LOX and IPA tanks at 1.5&times; the maximum expected operating pressure.",
                "Conducted pressurized vehicle leak checks and cryogenic cold flows with liquid nitrogen to validate the fluids system.",
            ]},
        ],
        gallery_items=[
            ("assets/img/testing-static-fire-plume.jpg","LOX/IPA plume — the blue-to-magenta color comes from the combustion chemistry"),
            ("assets/img/testing-static-fire-stand.jpg","Full-vehicle static fire on the test stand"),
            ("assets/img/testing-injector-waterflow.jpg","Injector water flow test for CdA characterization"),
        ],
        side=sidebar("Pad technician, test engineer", "Pressure transducers, turbine flow meters, LN2 cold flow", "SEDS UCSD Propulsion",
                      [("moonshine.html","Engine design &amp; manufacturing"), ("vesper.html","Vehicle &amp; feed system")]),
    )

def build_riptide():
    project_page(
        "riptide.html", "riptide.html",
        "Project · Structures", "Riptide — LOX/LNG Lander",
        "SEDS UCSD's in-house R&amp;D effort in active engine control &mdash; throttling and thrust vectoring &mdash; built around Riptide, a bi-propellant LOX-LNG sounding vehicle designed for suborbital flights to 1,000&nbsp;ft with a powered landing.",
        hero_img="assets/img/riptide-lathe-footpad.jpg",
        spec_items=[("LOX<span>/ LNG</span>","Propellants"),("1,000<span>ft</span>","Target Apogee"),("Powered","Landing Recovery")],
        sections=[
            {"h":"Structures &amp; Manufacturing", "bullets":[
                "Designed angled solenoid manifold mounts and manufactured them using a metal bender and mill.",
                "Resized the rocket body module length and mounting-hole pattern, then manufactured the module on a bandsaw, mill, and drill press.",
                "Manufactured the landing legs, ankle joint, and footpad &mdash; generating CAM toolpaths in Fusion 360 to CNC and lathe stock metal.",
            ]},
        ],
        gallery_items=[
            ("assets/img/riptide-body-module-cad.jpg","Resized rocket body module — CAD"),
            ("assets/img/riptide-fusion-cam.jpg","Fusion 360 CAM simulation for the footpad"),
            ("assets/img/riptide-lathe-footpad.jpg","Lathing footpad stock"),
        ],
        side=sidebar("Structures", "Fusion 360, metal bender, CNC lathe &amp; mill", "SEDS UCSD Lander (Riptide)",
                      [("lander-jr.html","GNC test stand for this vehicle")]),
        note='Team page: <a href="https://www.sedsucsd.org/lander" style="color:var(--blue)">sedsucsd.org/lander</a> (not always up to date).',
    )

def build_landerjr():
    project_page(
        "lander-jr.html", "lander-jr.html",
        "Project · GNC Test Stand", "Lander Jr",
        "Riptide's in-house testbed for guidance, navigation, and control: a propeller-powered drone that emulates the flight dynamics of the thrust-vector-controlled lander, used to develop and de-risk GNC algorithms before they fly on real propellant.",
        hero_render="assets/img/landerjr-teststand-cad.jpg",
        spec_items=[("Propeller-<span>driven</span>","Dynamics Emulation"),("LiDAR","Ground Sensing"),("Balanced","Center of Mass")],
        sections=[
            {"h":"Structures &amp; Avionics", "bullets":[
                "The Lander Jr test stand is a propeller-powered drone that emulates the dynamics of the self-landing rocket, used to develop guidance, navigation, and control schemes for the thrust-vector-controlled vehicle.",
                "Designed the 3D-printed LiDAR mount at an angle that lets the LiDAR see the ground without interference from the rest of the airframe.",
                "Redesigned the avionics bay around the mass of each piece of electronics, placing the heavier batteries to counteract the LiDAR and servos and keep the center of mass balanced.",
            ]},
        ],
        gallery_items=[
            ("assets/img/landerjr-avionics-cad.jpg","Avionics bay layout, mass-balanced around LiDAR and servos"),
        ],
        side=sidebar("GNC structures", "SolidWorks, 3D printing", "SEDS UCSD Lander (Riptide)",
                      [("riptide.html","The vehicle Lander Jr emulates")]),
    )

def build_boeing():
    project_page(
        "boeing.html", "boeing.html",
        "Experience · Industry", "Boeing — Manufacturing Engineering Intern",
        "A summer at Boeing's Huntington Beach site, producing factory layouts for a building vacated since COVID and improving shop-floor safety on legacy machinery.",
        hero_icon="factory",
        spec_items=[("Huntington","Beach Site"),("ORCA","XLUUV Program"),("Factory Layout","Software")],
        sections=[
            {"h":"Factory Layout — ORCA XLUUV", "bullets":[
                "Used Boeing's factory layout software to build 3D layouts of industrial machinery and office space for a building vacated at the Huntington Beach site since COVID.",
                "Measured existing machinery on the floor to build accurate as-built representations in the software.",
                "One layout was used by engineers to allocate assembly space for the ORCA XLUUV program; another was used to plan cubicle placement for the engineers overseeing it.",
                "Met with the software's developers, who incorporated the layouts into Boeing's company-wide tool.",
            ]},
            {"h":"Shop Safety &amp; Composites", "bullets":[
                "Designed a 3D-printed dust funnel to improve safety on two bandsaws flagged by the Boeing Fire Department &mdash; the outdated machines couldn't clear wood dust into the shop vacuum, creating a flammable buildup.",
                "Learned carbon-fiber layup technique from the composite manufacturing engineers on the floor.",
            ]},
        ],
        side=sidebar("Manufacturing engineering intern", "Factory layout software, hand measurement, 3D printing", "Boeing — Huntington Beach", []),
        note="Photography from this internship is subject to Boeing's proprietary-content review before release &mdash; cleared images can be dropped into <code>assets/img/</code> and referenced here.",
    )

def build_robot():
    project_page(
        "robot.html", "robot.html",
        "Project · Competition", "Golden Oreo — Competition Robot",
        "A UCSD MAE department challenge: design, fabricate, and compete with a robot in a single month, FRC-style. Golden Oreo picks up rings and hangs them on branches &mdash; the higher the branch, the more it scores.",
        hero_icon="robot",
        spec_items=[("1<span>mo.</span>","Build Window"),("Cascade","Lift Mechanism"),("Ring &amp;","Branch Scoring")],
        sections=[
            {"h":"Design", "bullets":[
                "Drew on past FIRST Robotics experience to create the team's initial concept, built around reaching high branches quickly.",
                "Designed and fabricated the lifting arm around a linear cascading-slide lift, chosen for its ability to reach anywhere from ring pick-up height to the highest branch.",
            ]},
        ],
        side=sidebar("Lift mechanism design", "CAD, rapid fabrication", "UCSD MAE Robot Competition", []),
    )

def build_research():
    project_page(
        "research.html", "research.html",
        "Research · Materials Science", "Cai Group — Soft Materials &amp; Mechanical Hand",
        "Research assistant in the Cai Group at UCSD, which studies the mechanics and chemistry of soft materials &mdash; synthesized polymers and biological tissue alike &mdash; for applications in artificial muscle, soft robotics, and biomedical devices.",
        hero_icon="molecule",
        spec_items=[("LCE vs.","3M VHB Creep"),("MATLAB","Analysis"),("Tremor Hand","In Progress")],
        sections=[
            {"h":"Liquid Crystal Elastomers", "bullets":[
                "Fabricated samples and ran creep experiments across different crosslinking concentrations of liquid crystal elastomers (LCEs), benchmarked against commercial 3M VHB tape.",
                "Analyzed creep behavior in MATLAB to compare LCE formulations against the VHB baseline.",
            ]},
            {"h":"Tremor-Mimicking Hand", "bullets":[
                "Currently designing an actuated mechanical hand that reproduces tremor patterns associated with Parkinson's disease.",
                "The hand will be used to test candidate glove materials from the lab for their ability to damp tremor when worn.",
            ]},
        ],
        side=sidebar("Research assistant", "MATLAB, mechanical testing, sample fabrication", "Cai Group, UCSD",
                      []),
        note='Lab site: <a href="https://sites.google.com/ucsd.edu/caigroup/home" style="color:var(--blue)">sites.google.com/ucsd.edu/caigroup</a>',
    )

def build_misc():
    project_page(
        "misc.html", "misc.html",
        "Writing · Autodesk Ambassador", "Miscellaneous — Instructables",
        "As an Autodesk ambassador, I wrote a guide to modeling true-to-scale airplanes in CAD directly from three-view drawings &mdash; featured in Instructables' First&nbsp;Time&nbsp;Authors contest.",
        hero_icon="plane",
        spec_items=[("Featured","First Time Authors"),("3-View","Drawing Workflow")],
        sections=[
            {"h":"Designing True-to-Scale 3D Printed Airplane Models", "bullets":[
                "Published a step-by-step Instructable on modeling airplanes from three-view drawings, aimed at makers without a CAD background.",
                "Featured in Instructables' First Time Authors contest as an Autodesk ambassador.",
            ]},
        ],
        side=sidebar("Author", "Fusion 360, technical writing", "Autodesk Ambassador Program",
                      []),
        note='Read it: <a href="https://www.instructables.com/Designing-True-to-Scale-3D-Printed-Airplane-Models/" style="color:var(--blue)">instructables.com/Designing-True-to-Scale-3D-Printed-Airplane-Models</a>',
    )


if __name__ == "__main__":
    build_index()
    build_moonshine()
    build_vesper()
    build_testing()
    build_riptide()
    build_landerjr()
    build_boeing()
    build_robot()
    build_research()
    build_misc()
    print("\\nDone.")

