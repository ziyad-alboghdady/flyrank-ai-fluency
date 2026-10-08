#!/usr/bin/env python3
"""Static site generator for ziyadalboghdady.dev
Run:  python3 build_site.py      (writes into ./portfolio-site/)
Every page shares one head/header/footer so the identity kit stays consistent."""
import os, html, pathlib

ROOT = pathlib.Path(__file__).parent / "portfolio-site"
SITE = "https://ziyad-alboghdady.netlify.app"   # <-- update after you claim the Netlify name
EMAIL = "ziyadalboghdady@gmail.com"
GITHUB = "https://github.com/ziyad-alboghdady"
LINKEDIN = "https://www.linkedin.com/in/ziyad-alboghdady-a50ab8247"
FORM_ENDPOINT = "https://formspree.io/f/REPLACE_ME"  # <-- paste your Formspree form id

NAV = [("/", "Home"), ("/projects/", "Projects"), ("/about/", "About"), ("/contact/", "Contact")]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{path}">
<meta property="og:image" content="{site}/assets/img/og-card.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/"><span class="mark">&#123;ZB&#125;</span><span class="name">Ziyad Alboghdady</span></a>
    <nav class="nav" aria-label="Primary">
      {nav}
      <a class="btn btn-primary" href="/contact/">Contact me</a>
    </nav>
  </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site-foot">
  <div class="wrap">
    <div>&copy; 2026 Ziyad Alboghdady &middot; Backend software engineer &middot; Sakarya, Turkey</div>
    <div>
      <a href="mailto:{email}">Email</a> &middot;
      <a href="{github}" rel="noopener">GitHub</a> &middot;
      <a href="{linkedin}" rel="noopener">LinkedIn</a> &middot;
      <a href="/assets/Ziyad-Alboghdady-CV.pdf">CV (PDF)</a>
    </div>
    <!-- FlyRank graduate badge goes here once the capstone is approved (Week 7: Plant Your Flag). -->
  </div>
</footer>
</body>
</html>
"""

def page(path, title, desc, body):
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == path else "", l)
        for h, l in NAV)
    out = HEAD.format(title=title, desc=desc, site=SITE, path=path, nav=nav) + body + \
          FOOT.format(email=EMAIL, github=GITHUB, linkedin=LINKEDIN)
    d = ROOT / path.strip("/")
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out, encoding="utf-8")
    print("wrote", (d / "index.html").relative_to(ROOT.parent))

def ph(text):
    return '<div class="placeholder">%s</div>' % text

# ---------------------------------------------------------------- case data
CASES = [
 dict(slug="task-management-api",
   name="Task Management API",
   tag=".NET 9 &middot; PostgreSQL 16 &middot; Docker Compose &middot; Supabase Auth",
   stack=[".NET 9 Web API","C#","EF Core","PostgreSQL 16","Docker Compose","Supabase Auth","JWT middleware"],
   role="Sole engineer", period="2026", repo=GITHUB+"/dotnet-layered-architecture-task-api",
   summary="A containerised REST API where ownership is impossible to forget, token revocation is immediate, and the API never stores a password.",
   problem="""<p>A task API is only interesting once more than one person uses it. Then two things get hard: proving who
     the caller is, and guaranteeing that a caller can never touch another user's rows. Both are easy to get almost right
     &mdash; and &ldquo;almost right&rdquo; on an authorisation boundary is indistinguishable from broken.</p>""",
   did="""<ul>
     <li>Split the service into Controllers &rarr; Services &rarr; Repositories, with <code>ITasksRepository</code>
         implemented by <code>PostgresTasksRepository</code> over EF Core, so storage stays behind one seam.</li>
     <li>Made Supabase the identity provider and this API a pure resource server: <strong>it never stores a password
         and never signs a token</strong>, it only verifies them. One less thing to get catastrophically wrong.</li>
     <li>Put authentication in <code>SupabaseAuthMiddleware</code> rather than in controllers, so controllers contain
         no auth code at all. <code>ErrorHandlerMiddleware</code> wraps it from the outside, so an exception thrown by
         the auth guard is still handled.</li>
     <li><strong>Chose a network round-trip over a local JWKS signature check.</strong> Local verification is
         microseconds; the round-trip costs latency and fails when Supabase is down. I took the slower option because
         it rejects a revoked token immediately, where a local check honours it until it expires. When Supabase is
         unreachable the API returns 503, not 401 &mdash; an outage is not the caller's fault, and re-authenticating
         cannot fix it.</li>
     <li>Made ownership a <em>required parameter</em> on every repository query rather than a check inside each method,
         so it cannot be omitted by accident. The owner is always taken from the verified token, never the request body.</li>
     <li>Requesting someone else's task returns <strong>404, not 403</strong> &mdash; a 403 would confirm that the id exists.</li>
     <li>All configuration comes from environment variables; <code>appsettings.json</code> holds no secrets and no
         connection string. Missing config throws at startup with a readable message instead of a null reference on
         the first request.</li>
   </ul>""",
   came="""<ul>
     <li>Cross-user access is structurally impossible, not policed: the query will not compile without an owner.</li>
     <li>A revoked session stops working on the next request rather than at token expiry.</li>
     <li><code>docker compose up</code> brings the API and PostgreSQL 16 up together with a named volume, so data
         survives a reboot and a reviewer can run the whole thing without installing a database.</li>
     <li>The trade-off table is in the README, because the interesting part of this project is the decision, not the CRUD.</li>
   </ul>""",
   artifact="Swagger UI with a 401 and a 404 side by side, plus the docker compose up output showing both services healthy."),

 dict(slug="car-rental-system",
   name="Car Rental Management System",
   tag="ASP.NET Core MVC &middot; EF Core &middot; SQL Server",
   stack=["ASP.NET Core MVC","C#","EF Core","SQL Server","ASP.NET Core Identity","Triggers & stored functions"],
   role="Sole engineer", period="2026", repo=GITHUB+"/car-rental-management-system",
   summary="Seven modules over one relational core &mdash; cars, customers, employees, contracts, payments and licences &mdash; with the invariants pushed down into the database rather than trusted to the UI.",
   problem="""<p>A rental company's data is all constraints: a car cannot be on two contracts at once, a contract cannot
     exist without a valid licence, a payment cannot outlive its contract. Enforce those only in C# and they hold until
     the day someone writes to the database another way.</p>""",
   did="""<ul>
     <li>Modelled the domain across seven modules &mdash; cars catalogue, customers, employees, rental contracts,
         payments, licences and accounts &mdash; each with its own controller and a clean MVC separation.</li>
     <li>Used EF Core with code-first migrations for the schema, but kept <strong>constraints, stored functions and
         triggers in SQL</strong> so the invariants live with the data, not only with the application.</li>
     <li>Added ASP.NET Core Identity for authentication and role-based authorisation over provisioning, pricing and
         rental history.</li>
     <li>Committed the SQL scripts and seed data to <code>db/</code> so the schema is reviewable on its own, without
         reading the C#.</li>
   </ul>""",
   came="""<ul>
     <li>The rules survive a direct write. Anything that bypasses the app still meets the same constraints.</li>
     <li>A reviewer can read the schema without reading the application &mdash; which is how a reviewer actually reads.</li>
     <li>Views stay free of query logic; data access lives where it can be changed once.</li>
   </ul>""",
   artifact="ERD of the schema, plus a rejected invalid contract showing the constraint firing."),

 dict(slug="university-management-platform",
   name="University Management System",
   tag="ASP.NET Core MVC + Web API &middot; EF Core",
   stack=["ASP.NET Core MVC","Web API","EF Core","ASP.NET Identity","Repository pattern","DTOs","Pagination"],
   role="Sole engineer", period="2026", repo=GITHUB+"/ASP.NET-University-Management-System",
   summary="One domain served two ways &mdash; Razor views for staff, a REST API for everything else &mdash; without duplicating the data layer.",
   problem="""<p>The same university data needed a UI for staff and a JSON API for other systems. The naive answer is
     two codebases that drift apart within a month. The real question was how much could be shared before the sharing
     itself became the problem.</p>""",
   did="""<ul>
     <li>Shared one repository layer and one <code>DbContext</code> between MVC controllers and API controllers, so a
         query is written once and both surfaces inherit it.</li>
     <li>Kept the <em>shapes</em> separate: ViewModels for Razor, DTOs for the API. Sharing the data access is cheap;
         sharing the response shape is how an API ends up leaking form state.</li>
     <li>Put pagination on both surfaces from the start &mdash; <code>?pageNumber=1&amp;pageSize=5</code> &mdash;
         because an unbounded student list is a production incident waiting for enrolment season.</li>
     <li>Used ASP.NET Identity with role-based authorisation, with destructive operations (deleting a student) reserved
         to admins.</li>
     <li>Handled student photo upload to <code>wwwroot/StudentPictures</code> rather than storing binaries in the database.</li>
   </ul>""",
   came="""<ul>
     <li>Adding a field means one entity, one repository method, and two small shape changes &mdash; not two features.</li>
     <li>List endpoints stay flat in response time as records grow.</li>
     <li>The API is usable by something that is not my own UI, which is the only real test of whether it is an API.</li>
   </ul>""",
   artifact="Side-by-side: the Razor student list and GET /api/students?pageNumber=1&pageSize=5 returning the same data."),

 dict(slug="polite-scraper",
   name="The Polite Scraper",
   tag="C# / .NET 9 &middot; rate limiting, caching, partial failure",
   stack=["C#",".NET 9","HttpClient","Schema validation","On-disk cache","Exponential backoff"],
   role="Sole engineer", period="2026", repo=GITHUB+"/polite-scraper",
   summary="Turns three pages of messy HTML into 60 schema-validated JSON records without ever being rude to the server &mdash; and without losing good data when one page is broken.",
   problem="""<p>Writing something that fetches 60 pages takes an afternoon. Writing one that a server operator would not
     want blocked is a different problem: it has to identify itself, pace itself, never retry an answer, and keep the
     records it already has when one page fails.</p>""",
   did="""<ul>
     <li>Checked before collecting, and wrote the check down: what the site is, what <code>robots.txt</code> says,
         whether terms exist, whether any personal data is involved. <strong>A 404 on robots.txt means no rules were
         stated, not that anything goes</strong> &mdash; it removes a prohibition, not the obligation to behave.</li>
     <li>Confined every network call to one class, <code>PoliteHttpClient</code>, so the rules are enforced in a single
         place instead of remembered at each call site.</li>
     <li>Set an identifying User-Agent with a contact address, and made the program warn when it is unset. A scraper
         nobody can contact is an anonymous one.</li>
     <li>500 ms delay plus jitter: 60 requests in two seconds looks like an attack; spread over ~35 seconds it looks
         like a reader.</li>
     <li>Retried only timeouts and 5xx, with exponential backoff. <strong>A 404 is never retried &mdash; it is an
         answer, not an accident.</strong></li>
     <li>Added an on-disk cache so repeated runs are byte-identical and cost the server nothing, and emitted a run
         report and an error file alongside the data.</li>
   </ul>""",
   came="""<ul>
     <li>A cold run takes ~41 seconds, 22 of which is deliberate waiting. A second run finishes in under a second,
         entirely from cache.</li>
     <li>A broken page produces an error record, not a lost dataset &mdash; partial failure stays partial.</li>
     <li>Reruns are byte-identical, which makes the output diffable and the whole thing testable.</li>
   </ul>""",
   artifact="Terminal output of a cold run and a cached rerun side by side, plus a slice of books.json."),
]

# ---------------------------------------------------------------- home
featured = "".join("""
  <article class="card">
    <h3><a href="/projects/{slug}/">{name}</a></h3>
    <p>{summary}</p>
    <ul class="stack">{chips}</ul>
    <p class="more"><a href="/projects/{slug}/">Read the decisions &rarr;</a></p>
  </article>""".format(slug=c["slug"], name=c["name"], summary=c["summary"],
                       chips="".join("<li>%s</li>" % s for s in c["stack"][:4]))
  for c in CASES[:2])

home = """
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Backend software engineer</p>
    <h1 class="claim">I build reliable, testable ASP.NET&nbsp;Core backends with strict layered boundaries and clean data design.</h1>
    <p class="lede">ASP.NET Core is my primary stack, supported by Spring Boot, relational database design, REST APIs,
      real-time communication with SignalR, and practical AI integration where it earns its place.</p>
    <ul class="stack">
      <li>ASP.NET Core</li><li>C#</li><li>PostgreSQL</li><li>EF Core</li><li>SignalR</li><li>Spring Boot</li>
    </ul>
    <div class="actions">
      <a class="btn btn-primary" href="/projects/">Explore my work</a>
      <a class="btn btn-ghost" href="{github}" rel="noopener">View GitHub</a>
      <a class="btn btn-ghost" href="/contact/">Contact me</a>
    </div>
  </div>
</section>
<hr class="rule">
<section>
  <div class="wrap">
    <div class="section-head">
      <h2>Featured case studies</h2>
      <p>Each case is the same three beats: the problem, what I did and decided, what came of it.</p>
    </div>
    <div class="grid grid-2">{featured}</div>
    <p style="margin-top:var(--s3)"><a href="/projects/">All four case studies &rarr;</a></p>
  </div>
</section>
<hr class="rule">
<section>
  <div class="wrap">
    <div class="section-head"><h2>How I work</h2></div>
    <ul class="plain">
      <li><span class="k">Boundaries first</span><span class="v">Controllers move HTTP, services hold rules, repositories hold storage. One reason to change each.</span></li>
      <li><span class="k">Schema before query</span><span class="v">Normalise, then write the query. Most &ldquo;performance problems&rdquo; are modelling problems.</span></li>
      <li><span class="k">Reversible choices</span><span class="v">Persistence behind an interface, so today&rsquo;s shortcut is not tomorrow&rsquo;s rewrite.</span></li>
      <li><span class="k">I ship what I understand</span><span class="v">If I cannot explain a line, it does not go in.</span></li>
    </ul>
  </div>
</section>
""".format(featured=featured, github=GITHUB)

page("/", "Ziyad Alboghdady — Backend Software Engineer (ASP.NET Core)",
     "Early-career backend engineer building reliable, testable ASP.NET Core systems: layered APIs, relational schema design, SignalR, and practical AI integration.",
     home)

# ---------------------------------------------------------------- projects index
cards = "".join("""
  <article class="card">
    <h3><a href="/projects/{slug}/">{name}</a></h3>
    <p class="v" style="font-family:var(--font-mono);font-size:.8rem;color:var(--accent)">{tag}</p>
    <p>{summary}</p>
    <ul class="stack">{chips}</ul>
    <p class="more"><a href="/projects/{slug}/">Read the decisions &rarr;</a></p>
  </article>""".format(slug=c["slug"], name=c["name"], tag=c["tag"], summary=c["summary"],
                       chips="".join("<li>%s</li>" % s for s in c["stack"]))
  for c in CASES)

page("/projects/", "Case studies — Ziyad Alboghdady",
     "Four backend case studies: a layered ASP.NET Core Web API, a 14-table car rental system, a university management platform, and a SignalR real-time service.",
     """
<section>
  <div class="wrap">
    <div class="section-head">
      <h1>Case studies</h1>
      <p>Four systems, strongest first. Every one lists the decision I made and what it cost me.</p>
    </div>
    <div class="grid grid-2">%s</div>
  </div>
</section>""" % cards)

# ---------------------------------------------------------------- case pages
for i, c in enumerate(CASES):
    nxt = CASES[(i + 1) % len(CASES)]
    body = """
<section>
  <div class="wrap">
    <p class="eyebrow">Case study</p>
    <h1>{name}</h1>
    <p class="lede">{summary}</p>
    <div class="meta">
      <div><span class="k">Stack</span><span class="v">{stackline}</span></div>
      <div><span class="k">Role</span><span class="v">{role}</span></div>
      <div><span class="k">When</span><span class="v">{period}</span></div>
      <div><span class="k">Source</span><span class="v"><a href="{repo}" rel="noopener">GitHub repository</a></span></div>
    </div>

    <div class="beats">
      <div class="beat"><h2>The problem</h2>{problem}</div>
      <div class="beat"><h2>What I did &amp; decided</h2>{did}</div>
      <div class="beat"><h2>What came of it</h2>{came}</div>
    </div>

    <figure>
      {artifact}
      <figcaption>Real capture from the build &mdash; not a rendering.</figcaption>
    </figure>

    <div class="actions">
      <a class="btn btn-primary" href="/contact/">Invite me to a technical interview</a>
      <a class="btn btn-ghost" href="{repo}" rel="noopener">Read the code</a>
    </div>
    <p style="margin-top:var(--s3)">Next case: <a href="/projects/{nslug}/">{nname}</a></p>
  </div>
</section>""".format(name=c["name"], summary=c["summary"],
                     stackline=" &middot; ".join(c["stack"]), role=c["role"], period=c["period"],
                     repo=c["repo"], problem=c["problem"], did=c["did"], came=c["came"],
                     artifact=ph("REAL CAPTURE SLOT<br>" + c["artifact"] +
                                 "<br>Save as /assets/img/" + c["slug"] + ".png"),
                     nslug=nxt["slug"], nname=nxt["name"])
    page("/projects/%s/" % c["slug"], "%s — Ziyad Alboghdady" % c["name"], c["summary"], body)

# ---------------------------------------------------------------- about
page("/about/", "About — Ziyad Alboghdady",
     "Early-career backend software engineer at Sakarya University. ASP.NET Core, C#, PostgreSQL, EF Core, Spring Boot.",
     """
<section>
  <div class="wrap">
    <h1>About</h1>
    <p class="lede">I am an early-career backend software engineer specialising in ASP.NET Core and C#, with hands-on
      experience in Spring Boot and relational database design.</p>

    <p>I treat software as an engineering discipline rather than a pile of frameworks: choose the right abstraction,
      design the schema before writing the query, and understand every line that ships. My CV shows what I have studied.
      This site shows how I think, build, and decide.</p>

    <p>What I am after is a junior backend role on a team that reviews code seriously. If that is the team you are
      building, the fastest next step is a technical interview.</p>

    <h2>Toolkit</h2>
    <ul class="plain">
      <li><span class="k">Languages</span><span class="v">C#, Java, SQL, JavaScript</span></li>
      <li><span class="k">Frameworks</span><span class="v">ASP.NET Core (Web API + MVC), EF Core, Spring Boot, SignalR</span></li>
      <li><span class="k">Data</span><span class="v">PostgreSQL, SQLite, normalised schema design, transactions</span></li>
      <li><span class="k">Practice</span><span class="v">Layered architecture, SOLID, DTO boundaries, OpenAPI, Docker</span></li>
      <li><span class="k">AI</span><span class="v">Structured prompting, evals, MCP connectors &mdash; used where it adds value</span></li>
    </ul>

    <h2>Education &amp; recognition</h2>
    <ul class="plain">
      <li><span class="k">Sakarya University</span><span class="v">Computer Engineering &mdash; 3.93 GPA (most recent semester)</span></li>
      <li><span class="k">Rise Global</span><span class="v">Finalist</span></li>
      <li><span class="k">IoT &amp; AI Competition</span><span class="v">Participant</span></li>
      <li><span class="k">Languages</span><span class="v">Arabic (native), English, Turkish</span></li>
    </ul>

    <h2>Currently learning</h2>
    <p>Background jobs and scheduling, containerised deploys, and how far a relational model can carry a system before
      you genuinely need something else.</p>

    <figure>
      """ + ph("REAL PHOTO SLOT<br>One plain headshot, natural light, neutral background.<br>Save as /assets/img/ziyad.jpg &mdash; must be a real photo, never generated.") + """
      <figcaption>A real photo, because the subject is a person.</figcaption>
    </figure>

    <div class="actions">
      <a class="btn btn-primary" href="/contact/">Get in touch</a>
      <a class="btn btn-ghost" href="/assets/Ziyad-Alboghdady-CV.pdf">Download CV</a>
    </div>
  </div>
</section>""")

# ---------------------------------------------------------------- contact
page("/contact/", "Contact — Ziyad Alboghdady",
     "Contact Ziyad Alboghdady — early-career backend software engineer (ASP.NET Core, C#, PostgreSQL).",
     """
<section>
  <div class="wrap">
    <h1>One next step</h1>
    <p class="lede">I am looking for a junior or early-career backend software engineering role. If the case studies
      answered your question, the useful next move is a technical interview.</p>

    <form id="contact-form" action="{endpoint}" method="POST">
      <div>
        <label for="name">Your name</label>
        <input id="name" name="name" type="text" autocomplete="name" required>
      </div>
      <div>
        <label for="email">Your email</label>
        <input id="email" name="email" type="email" autocomplete="email" required>
      </div>
      <div>
        <label for="message">What would you like to talk about?</label>
        <textarea id="message" name="message" required></textarea>
      </div>
      <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn-primary" type="submit">Send message</button>
      <p class="form-note">Goes straight to my inbox. No newsletter, no tracking.</p>
      <p id="form-status" class="status" hidden role="status"></p>
    </form>

    <h2 style="margin-top:var(--s4)">Or reach me directly</h2>
    <ul class="plain">
      <li><span class="k">Email</span><span class="v"><a href="mailto:{email}">{email}</a></span></li>
      <li><span class="k">GitHub</span><span class="v"><a href="{github}" rel="noopener">{github}</a></span></li>
      <li><span class="k">LinkedIn</span><span class="v"><a href="{linkedin}" rel="noopener">{linkedin}</a></span></li>
      <li><span class="k">Based in</span><span class="v">Sakarya, Turkey &mdash; open to remote and relocation</span></li>
    </ul>
  </div>
</section>
<script src="/assets/contact.js" defer></script>""".format(endpoint=FORM_ENDPOINT, email=EMAIL, github=GITHUB, linkedin=LINKEDIN))

# ---------------------------------------------------------------- 404
(ROOT / "404.html").write_text(
    HEAD.format(title="Not found — Ziyad Alboghdady", desc="Page not found.", site=SITE, path="/404.html",
                nav="".join('<a href="%s">%s</a>' % (h, l) for h, l in NAV)) +
    """<section><div class="wrap"><p class="eyebrow">404</p><h1>That page does not exist.</h1>
    <p class="lede">The link is probably older than the site. The four case studies are all here:</p>
    <div class="actions"><a class="btn btn-primary" href="/projects/">Go to the case studies</a>
    <a class="btn btn-ghost" href="/">Back home</a></div></div></section>""" +
    FOOT.format(email=EMAIL, github=GITHUB, linkedin=LINKEDIN), encoding="utf-8")
print("wrote portfolio-site/404.html")

# ---------------------------------------------------------------- static extras
(ROOT / "assets" / "favicon.svg").write_text(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
 '<rect width="64" height="64" rx="14" fill="#0F172A"/>'
 '<text x="32" y="42" font-family="JetBrains Mono, monospace" font-size="26" font-weight="600" '
 'fill="#2563EB" text-anchor="middle">{}</text></svg>'.format("&#123;ZB&#125;"), encoding="utf-8")

(ROOT / "assets" / "contact.js").write_text("""// Progressive enhancement: keep the user on the page after a Formspree submit.
// Without JS the form still posts normally and Formspree shows its own page.
const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');
form?.addEventListener('submit', async (e) => {
  if (!form.action.includes('formspree.io') || form.action.includes('REPLACE_ME')) return;
  e.preventDefault();
  status.hidden = false; status.className = 'status'; status.textContent = 'Sending…';
  try {
    const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
    if (res.ok) { form.reset(); status.className = 'status ok'; status.textContent = 'Sent. I reply within a day or two.'; }
    else { throw new Error('Bad response ' + res.status); }
  } catch (err) {
    status.className = 'status err';
    status.innerHTML = 'That did not go through. Email me directly at <a href="mailto:%s">%s</a>.';
  }
});
""".replace('%s', EMAIL), encoding="utf-8")

(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE, encoding="utf-8")

urls = ["/", "/projects/", "/about/", "/contact/"] + ["/projects/%s/" % c["slug"] for c in CASES]
(ROOT / "sitemap.xml").write_text(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 + "".join("  <url><loc>%s%s</loc></url>\n" % (SITE, u) for u in urls) + "</urlset>\n", encoding="utf-8")

(ROOT / "_headers").write_text("""/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
/assets/*
  Cache-Control: public, max-age=31536000, immutable
""", encoding="utf-8")

print("done")
