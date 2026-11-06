"""Builds ibexcapitalmortgage.com into ../dist. Run: python3 src/build.py"""
import json, os, re, html, datetime
from states import STATES, slug

ROOT = os.path.join(os.path.dirname(__file__), "..", "dist")
SITE = "https://www.ibexcapitalmortgage.com"
BRAND = "Ibex Capital Mortgage"
LEGAL = "Ibex Capital, Inc."
NMLS = "2288114"
NMLS_URL = f"https://www.nmlsconsumeraccess.org/EntityDetails.aspx/COMPANY/{NMLS}"
PHONE = "888-699-5777"
PHONE_TEL = "+18886995777"
EMAIL = "info@ibexcapitalmortgage.com"
ADDRESS = "1084 N. El Camino Real #171, Encinitas, CA 92024"
HOURS = "Mon to Sat, 8 a.m. to 8 p.m. Pacific"
DEBT = "https://debtreliefpath.net"
# States where Ibex holds its own license. Add license numbers when you have them; blank ones are hidden.
LICENSED = {"CA": "", "CO": "", "MT": "", "TX": "", "FL": ""}
TODAY = datetime.date.today().isoformat()
E = html.escape
PAGES = []

LOGO = ('<svg viewBox="0 0 34 34" aria-hidden="true"><rect width="34" height="34" rx="4" fill="#1D4F73"/>'
        '<path d="M4 27 L12 15 L16 20 L22 9 L30 27 Z" fill="#D6E7EF"/>'
        '<path d="M19 11 C 17 6, 22 3, 26 5" stroke="#B9852A" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>')
RIDGE = ('<svg class="ridge" viewBox="0 0 1200 22" preserveAspectRatio="none" aria-hidden="true">'
         '<path d="M0 21 L140 12 L220 17 L360 4 L470 15 L560 9 L700 19 L820 6 L930 14 L1040 8 L1200 18" '
         'fill="none" stroke="#B9852A" stroke-width="1.6" vector-effect="non-scaling-stroke"/></svg>')
EHO = ('<svg viewBox="0 0 40 40" aria-label="Equal Housing Opportunity" role="img"><path d="M20 4 L37 16 H33 V35 H7 V16 H3 Z" '
       'fill="none" stroke="#FFFFFF" stroke-width="2.4"/><rect x="13" y="20" width="14" height="3" fill="#FFF"/><rect x="13" y="26" width="14" height="3" fill="#FFF"/></svg>')

CONSENT = (f"By checking this box, I agree that {LEGAL} and, if Ibex isn't licensed in my state, the licensed lender it refers me to "
           "may contact me about home loan options at the phone number and email I provided, including by calls and texts that may use "
           "automated technology or prerecorded messages. Consent is not required to get a loan; you can call us instead. "
           "Message and data rates may apply. Reply STOP to opt out.")


def lic_line():
    names = {a: n for n, a, *_ in STATES}
    parts = []
    for a, num in LICENSED.items():
        parts.append(f"{names[a]}{' (license ' + E(num) + ')' if num else ''}")
    return ", ".join(parts)


FOOT = (f"{LEGAL}, NMLS #{NMLS}. Licensed to originate residential mortgage loans in {lic_line()}. "
        "In other states, Ibex does not make loans; we refer you to an independent lender licensed in your state, and we may be paid for that referral. "
        "This is not a commitment to lend. All loans are subject to credit approval, underwriting guidelines and property eligibility. "
        "Programs, rates and terms change without notice and aren't available in every state. Ibex is not acting on behalf of HUD, FHA, VA or USDA.")


def page(path, title, desc, body, schema=None, crumbs=None):
    ld = []
    if path == "/":
        ld.append({"@context": "https://schema.org", "@type": ["Organization", "FinancialService"], "name": BRAND, "legalName": LEGAL,
                   "url": SITE + "/", "telephone": PHONE_TEL, "email": EMAIL,
                   "address": {"@type": "PostalAddress", "streetAddress": "1084 N. El Camino Real #171", "addressLocality": "Encinitas",
                               "addressRegion": "CA", "postalCode": "92024", "addressCountry": "US"},
                   "identifier": {"@type": "PropertyValue", "propertyID": "NMLS", "value": NMLS},
                   "areaServed": [n for n, a, *_ in STATES if a in LICENSED], "sameAs": [NMLS_URL]})
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
        items += [{"@type": "ListItem", "position": i, "name": n, "item": SITE + p} for i, (n, p) in enumerate(crumbs, 2)]
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    ld += schema or []
    crumb_html = ""
    if crumbs:
        parts = ['<a href="/">Home</a>'] + [f'<a href="{p}">{E(n)}</a>' for n, p in crumbs[:-1]] + [E(crumbs[-1][0])]
        crumb_html = f'<nav class="crumbs" aria-label="Breadcrumb">{" / ".join(parts)}</nav>'
    body = body.replace("{{CRUMBS}}", crumb_html)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    doc = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}{path if path != '/404.html' else '/'}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE}{path}"><meta property="og:site_name" content="{BRAND}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">{ld_html}
</head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>NMLS #{NMLS} &nbsp;|&nbsp; {HOURS}</span><span><a href="tel:{PHONE_TEL}">{PHONE}</a></span></div></div>
<header class="site-head"><div class="wrap">
<a class="brand" href="/">{LOGO}{BRAND}</a>
<nav class="nav" aria-label="Main"><a href="/loan-options/">Loan options</a><a href="/refinance/">Refinance</a><a href="/states/">States</a>
<a href="/calculator/">Calculator</a><a href="/about-us/">About</a><a class="btn btn-primary" href="/apply-now/">Get pre-qualified</a></nav>
</div>{RIDGE}</header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap"><div class="foot-grid">
<div><h2>{BRAND}</h2><p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>{E(ADDRESS)}<br>{HOURS}</p>
<p><a href="{NMLS_URL}">NMLS Consumer Access #{NMLS}</a></p>
<div class="eho">{EHO}<span>Equal Housing Opportunity</span></div></div>
<div><h2>Loans</h2><ul>{"".join(f'<li><a href="/{k}/">{v["nav"]}</a></li>' for k, v in PROGRAMS.items())}</ul></div>
<div><h2>Company</h2><ul><li><a href="/about-us/">About us</a></li><li><a href="/contact-us/">Contact us</a></li><li><a href="/faq/">Questions</a></li>
<li><a href="/licensing/">Licensing</a></li><li><a href="/for-lenders/">For lenders</a></li><li><a href="/behind-on-mortgage/">Behind on your mortgage?</a></li>
<li><a href="/privacy/">Privacy policy</a></li><li><a href="/terms/">Terms of use</a></li><li><a href="/ada-accessibility-statement/">Accessibility</a></li>
<li><a href="{DEBT}">Debt help: Debt Relief Path</a></li></ul></div>
</div>
<p class="legal">{FOOT} &copy; {datetime.date.today().year} {LEGAL}</p></div></footer>
<script src="/assets/site.js" defer></script>
</body></html>"""
    out = os.path.join(ROOT, "index.html") if path == "/" else (os.path.join(ROOT, "404.html") if path == "/404.html" else os.path.join(ROOT, path.strip("/"), "index.html"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    PAGES.append(path)


def faq_html(f):
    return "".join(f"<details><summary>{E(q)}</summary><p>{a}</p></details>" for q, a in f)


def faq_schema(f):
    s = lambda x: re.sub("<[^>]+>", "", x)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": s(a)}} for q, a in f]}


def opts(pairs, sel=""):
    return "".join(f'<option value="{E(v)}"{" selected" if v == sel else ""}>{E(t)}</option>' for v, t in pairs)


STATE_OPTS = [("", "Choose your state")] + [(a, n) for n, a, *_ in STATES]
GOALS = [("", "Choose one"), ("Buy a home", "Buy a home"), ("Refinance to lower my payment", "Refinance to lower my payment"),
         ("Cash-out refinance", "Take cash out of my equity"), ("Investment property / DSCR", "Buy or refinance an investment property"),
         ("Behind on payments", "I'm behind on my mortgage")]


def form(state="", goal="", heading="Get pre-qualified"):
    return f"""<div class="card"><h2>{E(heading)}</h2>
<p class="small">Takes about a minute. No credit check and no Social Security number to start.</p>
<form class="form" data-lead novalidate>
<div class="field"><label for="f-goal">What would you like to do?</label><select id="f-goal" name="goal" required>{opts(GOALS, goal)}</select></div>
<div class="row"><div class="field"><label for="f-state">Property state</label><select id="f-state" name="state" required>{opts(STATE_OPTS, state)}</select></div>
<div class="field"><label for="f-zip">ZIP code</label><input id="f-zip" name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5"></div></div>
<div class="row"><div class="field"><label for="f-value">Home price or value</label><select id="f-value" name="value">{opts([("", "Choose a range"), ("Under $300k", "Under $300k"), ("$300k to $500k", "$300k to $500k"), ("$500k to $800k", "$500k to $800k"), ("$800k to $1.2M", "$800k to $1.2M"), ("Over $1.2M", "Over $1.2M")])}</select></div>
<div class="field"><label for="f-credit">Credit, roughly</label><select id="f-credit" name="credit">{opts([("", "Choose one"), ("Excellent (740+)", "Excellent (740+)"), ("Good (680 to 739)", "Good (680 to 739)"), ("Fair (620 to 679)", "Fair (620 to 679)"), ("Below 620", "Below 620"), ("Not sure", "Not sure")])}</select></div></div>
<div class="row"><div class="field"><label for="f-first">First name</label><input id="f-first" name="first_name" autocomplete="given-name" required></div>
<div class="field"><label for="f-last">Last name</label><input id="f-last" name="last_name" autocomplete="family-name" required></div></div>
<div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div class="hp" aria-hidden="true"><label for="f-website">Website</label><input id="f-website" name="website" tabindex="-1" autocomplete="off"></div>
<div class="field"><label class="consent"><input type="checkbox" name="consent" value="yes" required><span>{E(CONSENT)} See our <a href="/privacy/">privacy policy</a>.</span></label></div>
<button class="btn btn-primary" type="submit">Get pre-qualified</button>
<p class="msg" role="status" aria-live="polite"></p></form>
<p class="small">Rather talk? Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p></div>"""


CALC = """<div class="calc" data-calc><h2>Estimate your payment</h2>
<div class="grid">
<div><label for="c-price">Home price</label><input id="c-price" inputmode="numeric" value="550,000"></div>
<div><label for="c-down">Down payment</label><input id="c-down" inputmode="numeric" value="55,000"></div>
<div><label for="c-rate">Interest rate (%)</label><input id="c-rate" inputmode="decimal" value="6.5"></div>
<div><label for="c-term">Loan term</label><select id="c-term"><option value="30">30 years</option><option value="20">20 years</option><option value="15">15 years</option></select></div>
<div><label for="c-tax">Property tax (%/yr)</label><input id="c-tax" inputmode="decimal" value="1.1"></div>
<div><label for="c-ins">Insurance ($/yr)</label><input id="c-ins" inputmode="numeric" value="1,800"></div>
</div>
<div class="result" aria-live="polite"><div class="amount" data-out>$0</div><div class="breakdown" data-break></div></div>
<p class="small" style="margin:0.8rem 0 0">For illustration only. The rate you enter isn't an offer; your actual rate, APR and payment depend on your credit, loan type and property.</p></div>"""


PROGRAMS = {
"conventional-loans": dict(nav="Conventional loans", h1="Conventional loans",
    lede="The most common home loan, not backed by a government agency. Good credit and steady income get you the best terms.",
    body="""<h2>Who it fits</h2><p>Borrowers with solid credit, a stable income history and at least a small down payment. Conventional loans follow guidelines set by Fannie Mae and Freddie Mac, and loans within the annual conforming limit get the most competitive pricing.</p>
<h2>Down payment and mortgage insurance</h2><p>Some programs allow as little as 3% down for first-time buyers. With less than 20% down you'll pay private mortgage insurance (PMI), which you can ask to remove once you reach 20% equity and which drops off automatically at 22% on a normal payment schedule.</p>
<h2>What lenders look at</h2><ul><li>Credit score, usually 620 or higher</li><li>Debt-to-income ratio</li><li>Two years of income history</li><li>Cash for the down payment, closing costs and reserves</li></ul>""",
    faqs=[("Can I use a conventional loan for a second home or rental?", "Yes. Second homes and investment properties qualify, usually with a larger down payment and slightly higher pricing than a primary residence."),
          ("Is PMI permanent?", "No. On a conventional loan you can request cancellation at 20% equity, and it ends automatically at 22% based on the original schedule.")]),
"fha-loans": dict(nav="FHA loans", h1="FHA loans",
    lede="Insured by the Federal Housing Administration, FHA loans make it easier to buy with a smaller down payment or less-than-perfect credit.",
    body="""<h2>Who it fits</h2><p>First-time buyers, people rebuilding credit, and anyone with a modest down payment. The home must be your primary residence.</p>
<h2>Down payment and credit</h2><table class="facts"><tbody><tr><th>Credit score 580 or higher</th><td>3.5% minimum down payment</td></tr><tr><th>Credit score 500 to 579</th><td>10% minimum down payment</td></tr></tbody></table>
<p>Lenders can set stricter minimums than FHA's. Gift funds from family can cover the down payment.</p>
<h2>Mortgage insurance</h2><p>FHA loans carry an upfront mortgage insurance premium, which can be added to the loan, plus an annual premium paid monthly. Depending on your down payment, the annual premium lasts 11 years or the life of the loan, which is why many FHA borrowers later refinance into a conventional loan.</p>""",
    faqs=[("Can I get an FHA loan after bankruptcy?", "Often yes. FHA generally allows a new loan two years after a Chapter 7 discharge, and sometimes during a Chapter 13 plan with court approval."),
          ("Are there FHA loan limits?", "Yes. FHA sets maximum loan amounts by county each year. We'll check the limit for your area.")]),
"va-loans": dict(nav="VA loans", h1="VA home loans",
    lede="For eligible veterans, service members and some surviving spouses. No down payment and no monthly mortgage insurance in most cases.",
    body="""<h2>Who qualifies</h2><ul><li>Veterans who meet service requirements and weren't dishonorably discharged</li><li>Active-duty service members</li><li>National Guard and Reserve members with qualifying service</li><li>Certain surviving spouses</li></ul>
<p>You'll need a Certificate of Eligibility, which we can request for you.</p>
<h2>Why it stands out</h2><p>The VA guarantees part of the loan, so lenders can offer no-down-payment financing without private mortgage insurance. Most borrowers pay a one-time VA funding fee, which can be financed; veterans receiving VA disability compensation are generally exempt.</p>
<h2>Refinancing</h2><p>A VA Streamline (IRRRL) can lower the rate on an existing VA loan with limited paperwork, and a VA cash-out refinance can replace any loan type for eligible borrowers.</p>""",
    faqs=[("Can I use a VA loan more than once?", "Yes. Your entitlement can be restored after you sell and pay off a VA loan, and in some cases you can have two VA loans at once."),
          ("Does the home need to be my primary residence?", "Yes. You must intend to live in the home, though VA loans can be used for properties with up to four units if you live in one.")]),
"usda-loans": dict(nav="USDA loans", h1="USDA home loans",
    lede="Zero-down financing for homes in eligible rural and suburban areas, backed by the U.S. Department of Agriculture.",
    body="""<h2>Who it fits</h2><p>Moderate-income buyers purchasing a primary residence in a USDA-eligible area. Many towns outside major metros qualify, including areas you might not think of as rural.</p>
<h2>Requirements</h2><ul><li>The property must be in an eligible area (USDA publishes an eligibility map)</li><li>Household income must be within the limit for the county</li><li>The home must be your primary residence</li></ul>
<h2>Costs</h2><p>USDA guaranteed loans have an upfront guarantee fee and a small annual fee. There's no down payment requirement for eligible borrowers.</p>""",
    faqs=[("How do I know if a home is eligible?", "Send us the address. We'll check it against USDA's eligibility map and your household income against the county limit.")]),
"jumbo-loans": dict(nav="Jumbo loans", h1="Jumbo loans",
    lede="For loan amounts above the conforming limit, common in high-cost areas like coastal California and Colorado resort towns.",
    body="""<h2>Who it fits</h2><p>Buyers and homeowners who need to borrow more than the annual conforming loan limit set by the Federal Housing Finance Agency for their county.</p>
<h2>What to expect</h2><ul><li>Higher credit score requirements, often 700 or more</li><li>Larger down payments, commonly 10% to 20%</li><li>Cash reserves covering several months of payments</li><li>Full documentation of income and assets</li></ul>
<p>Jumbo pricing varies widely between investors, so shopping several of them matters more than with conforming loans.</p>""",
    faqs=[("Are jumbo rates always higher?", "Not always. Depending on the market, jumbo rates can be close to or even below conforming rates for strong borrowers.")]),
"refinance": dict(nav="Refinancing", h1="Refinance your mortgage",
    lede="Lower your rate or payment, shorten your term, switch out of an adjustable rate, or take cash out of your equity.",
    body="""<h2>Reasons to refinance</h2><ul><li><strong>Rate and term:</strong> lower your rate or change your term to save interest.</li><li><strong>Cash-out:</strong> borrow against your equity for renovations, tuition or high-interest debt.</li><li><strong>Remove mortgage insurance:</strong> move from FHA to conventional once you have enough equity.</li><li><strong>Fixed instead of adjustable:</strong> lock in a payment before an ARM adjusts.</li></ul>
<h2>Does it make sense?</h2><p>Compare your closing costs with your monthly savings to find your break-even point. If you plan to stay past that point, a refinance usually pays off. Restarting a 30-year term can lower your payment but raise total interest, so look at both numbers.</p>
<div class="callout"><p>Using a cash-out refinance to pay off credit cards turns unsecured debt into debt secured by your home. If you're struggling with payments, compare it with the options at <a href="https://debtreliefpath.net">Debt Relief Path</a> first.</p></div>""",
    faqs=[("How much equity do I need?", "Most conventional refinances need at least 3% to 5% equity for rate-and-term and 20% for cash-out. FHA and VA streamline refinances have their own rules."),
          ("How long does a refinance take?", "Often 30 to 45 days from application to closing, sometimes faster with an appraisal waiver.")]),
"dscr-loans": dict(nav="DSCR & investment loans", h1="DSCR and investment property loans",
    lede="Qualify for a rental property based on its rent, not your personal income.",
    body="""<h2>How DSCR loans work</h2><p>A debt service coverage ratio (DSCR) loan compares the property's expected rent with its monthly payment, taxes, insurance and HOA dues. If the rent covers the costs by enough, you can qualify without tax returns or pay stubs. These loans are for investment properties only, never a home you live in.</p>
<h2>What to expect</h2><ul><li>Larger down payments, commonly 20% to 25%</li><li>Higher rates than owner-occupied loans</li><li>Cash reserves, often several months of payments</li><li>Loans can close in your name or an LLC's</li></ul>
<h2>Other investment options</h2><p>If you have documented income, a conventional investment property loan may cost less. We'll compare both.</p>""",
    faqs=[("What DSCR do I need?", "Many lenders look for 1.0 or higher, meaning rent at least covers the payment. Some allow lower ratios with a bigger down payment.")]),
"first-time-homebuyers": dict(nav="First-time buyers", h1="First-time homebuyers",
    lede="Low-down-payment loans, down payment assistance and a clear walk through every step.",
    body="""<h2>Loans that help first-time buyers</h2><ul><li><a href="/fha-loans/">FHA</a>: 3.5% down with a 580 credit score.</li><li><a href="/conventional-loans/">Conventional</a> first-time buyer programs: as little as 3% down.</li><li><a href="/va-loans/">VA</a> and <a href="/usda-loans/">USDA</a>: no down payment for those who qualify.</li></ul>
<h2>Down payment assistance</h2><p>State housing finance agencies and many cities offer grants or low-cost second loans for down payments and closing costs. Rules and funding differ by state and change often, so we check what's open when you apply.</p>
<h2>The steps</h2><ol><li>Get pre-qualified so you know your price range.</li><li>Gather pay stubs, W-2s, bank statements and ID for a full pre-approval.</li><li>Shop with your agent and make an offer.</li><li>Lock your rate, complete the appraisal and underwriting.</li><li>Sign and get your keys.</li></ol>""",
    faqs=[("Who counts as a first-time buyer?", "For most programs, anyone who hasn't owned a home in the past three years."),
          ("How much do I need for closing costs?", "Closing costs are commonly 2% to 5% of the price. Sellers, assistance programs or lender credits can cover some of them.")]),
"203k-loans": dict(nav="Renovation (203k) loans", h1="FHA 203(k) renovation loans",
    lede="Buy or refinance a home and finance the repairs in one loan.",
    body="""<h2>How it works</h2><p>A 203(k) loan rolls the price of a home and the cost of renovating it into a single FHA-insured mortgage. It's useful for fixer-uppers that wouldn't qualify for regular financing as-is.</p>
<h2>Two versions</h2><table class="facts"><tbody><tr><th>Limited 203(k)</th><td>Smaller, non-structural projects such as kitchens, flooring, roofs and appliances, up to FHA's cap.</td></tr><tr><th>Standard 203(k)</th><td>Larger and structural work, with a HUD consultant overseeing the project.</td></tr></tbody></table>
<p>The home must be your primary residence, and work is done by licensed contractors with funds released as work is completed.</p>""",
    faqs=[("Can I do the work myself?", "Generally no. 203(k) projects use licensed contractors, and funds are paid out as work is inspected.")]),
}


def home():
    progs = "".join(f'<a href="/{k}/"><strong>{v["nav"]}</strong><span>{E(v["lede"].split(". ")[0].rstrip("."))}.</span></a>' for k, v in PROGRAMS.items())
    faqs = [("Which states does Ibex lend in?", f"Ibex is licensed in {lic_line()}. If your property is in another state, we'll refer you to an independent lender licensed there."),
            ("Will getting pre-qualified hurt my credit?", "No. Our pre-qualification form doesn't pull credit. A credit check happens only when you choose to apply, and we'll tell you first."),
            ("What do I need to apply?", "Usually recent pay stubs, two years of W-2s or tax returns, two months of bank statements and a photo ID. Self-employed borrowers and investors have other options."),
            ("How long does it take to close?", "Most purchases close in about 30 days. Refinances can be faster.")]
    body = f"""<section class="hero"><div class="wrap hero-grid">
<div><h1>Home loans, minus the guesswork</h1>
<p class="lede">Purchase, refinance, VA, FHA, jumbo and investor loans, with a loan officer who explains the numbers before you commit.</p>
<p class="actions"><a class="btn btn-primary" href="/apply-now/">Get pre-qualified</a><a class="btn btn-quiet" href="tel:{PHONE_TEL}">Call {PHONE}</a></p>
<p class="note">Licensed in California, Colorado, Montana, Texas and Florida. Partner lenders in every other state.</p></div>
{CALC}
</div></section>
<section class="band band-stone"><div class="wrap"><h2>Loan options</h2><div class="programs">{progs}</div></div></section>
<section class="band"><div class="wrap"><h2>How it works</h2><ol class="steps">
<li><h3>Pre-qualify</h3><p>A one-minute form, no credit check. A loan officer calls to talk through your goals.</p></li>
<li><h3>Compare</h3><p>We show you loan options side by side with rate, APR, payment and cash to close.</p></li>
<li><h3>Apply securely</h3><p>Upload documents through our secure application, never by email.</p></li>
<li><h3>Close</h3><p>We keep you updated through appraisal, underwriting and signing.</p></li></ol></div></section>
<section class="band band-stone"><div class="wrap prose"><h2>Behind on your mortgage?</h2>
<p>If you've missed payments or received a foreclosure notice, act now. Call your servicer, and see our guide to <a href="/behind-on-mortgage/">loan modification and foreclosure options</a>. For credit card or other debt, <a href="{DEBT}">Debt Relief Path</a> can connect you with settlement companies and bankruptcy attorneys.</p>
<h2>Common questions</h2>{faq_html(faqs)}</div></section>"""
    page("/", "Ibex Capital Mortgage: Home Loans, Refinancing, VA & FHA | NMLS 2288114",
         "Purchase and refinance loans from Ibex Capital Mortgage, licensed in CA, CO, MT, TX and FL, with partner lenders nationwide. Get pre-qualified without a credit check.",
         body, [faq_schema(faqs)])


def program_pages():
    for k, v in PROGRAMS.items():
        body = f"""<div class="wrap page-head">{{{{CRUMBS}}}}<h1>{E(v['h1'])}</h1><p class="lede">{E(v['lede'])}</p></div>
<div class="wrap page-grid"><article class="prose">{v['body']}
<h2>Questions</h2>{faq_html(v['faqs'])}
<p><a href="/loan-options/">Compare all loan options</a> &nbsp;|&nbsp; <a href="/states/">Find your state</a></p></article>
<aside class="side">{form(goal="Refinance to lower my payment" if k == "refinance" else ("Investment property / DSCR" if k == "dscr-loans" else "Buy a home"))}</aside></div>"""
        page(f"/{k}/", f"{v['h1']} | Ibex Capital Mortgage", v["lede"], body, [faq_schema(v["faqs"])],
             crumbs=[("Loan options", "/loan-options/"), (v["nav"], f"/{k}/")])
    rows = "".join(f'<tr><th><a href="/{k}/">{v["nav"]}</a></th><td>{E(v["lede"])}</td></tr>' for k, v in PROGRAMS.items())
    body = f"""<div class="wrap page-head">{{{{CRUMBS}}}}<h1>Loan options</h1><p class="lede">Every loan we offer, and who each one fits.</p></div>
<div class="wrap page-grid"><article class="prose"><table class="facts"><tbody>{rows}</tbody></table>
<p>Not sure which fits? A loan officer can compare two or three options with real numbers for your situation.</p></article><aside class="side">{form()}</aside></div>"""
    page("/loan-options/", "Mortgage Loan Options: Conventional, FHA, VA, USDA, Jumbo, DSCR | Ibex", "Compare home loan programs from Ibex Capital Mortgage and see which fits your situation.", body, crumbs=[("Loan options", "/loan-options/")])


def state_pages():
    for name, ab, *_ in STATES:
        s = slug(name)
        lic = ab in LICENSED
        if lic:
            who = f"Ibex Capital, Inc. is licensed to originate mortgage loans in {name} (NMLS #{NMLS}). Your loan officer works with you directly from pre-qualification to closing."
            h1 = f"{name} mortgage lender"
            title = f"{name} Home Loans & Refinancing | Ibex Capital Mortgage, NMLS {NMLS}"
            desc = f"Ibex Capital Mortgage is a licensed {name} mortgage lender offering purchase, refinance, FHA, VA, USDA, jumbo and DSCR loans."
            facts = f"<tr><th>Ibex licensed here</th><td>Yes. Ibex originates your loan directly.</td></tr>" + (f"<tr><th>State license</th><td>{E(LICENSED[ab])}</td></tr>" if LICENSED[ab] else "")
        else:
            who = (f"Ibex isn't licensed in {name}, so we don't make loans here. When you request a quote for {"an" if name[0] in "AEIOU" else "a"} {name} property, "
                   f"we refer you to an independent mortgage lender licensed in {name}. That lender sets your rate and terms and handles your loan. We may receive a referral fee, which doesn't change what you pay.")
            h1 = f"{name} home loans"
            title = f"{name} Home Loans: Compare Licensed Lenders | Ibex Capital Mortgage"
            desc = f"Get matched with a mortgage lender licensed in {name} for purchase, refinance, FHA, VA, USDA, jumbo and DSCR loans."
            facts = "<tr><th>Ibex licensed here</th><td>No. You'll work with a licensed partner lender.</td></tr>"
        faqs = [(f"What home loans are available in {name}?", f"Conventional, FHA, VA, USDA (in eligible areas), jumbo, renovation and investor DSCR loans are all used in {name}. Which one fits depends on your credit, down payment and the property."),
                (f"Is there down payment assistance in {name}?", f"{name}'s housing finance agency and many local governments offer down payment and closing cost help for qualifying buyers. Programs open and close often, so ask when you apply."),
                (f"What if I'm behind on my mortgage in {name}?", f"Contact your servicer right away and ask about a loan modification or forbearance. Free HUD-approved housing counselors serve {name} at 800-569-4287. See our <a href=\"/behind-on-mortgage/\">guide for homeowners behind on payments</a>.")]
        body = f"""<div class="wrap page-head">{{{{CRUMBS}}}}<h1>{E(h1)}</h1><p class="lede">Purchase and refinance loans for homes in {name}.</p></div>
<div class="wrap page-grid"><article class="prose">
<h2>Who you'll work with</h2><p>{who}</p>
<table class="facts"><tbody>{facts}<tr><th>Loan types</th><td>Conventional, FHA, VA, USDA, jumbo, 203(k), DSCR</td></tr><tr><th>Free housing counseling</th><td>HUD: 800-569-4287</td></tr></tbody></table>
<h2>Buying a home in {name}</h2><p>Get pre-qualified before you shop so you know your price range and can make a strong offer. First-time buyers in {name} can often combine an <a href="/fha-loans/">FHA</a> or <a href="/conventional-loans/">conventional</a> loan with state or local down payment assistance. Veterans should look at <a href="/va-loans/">VA loans</a>, and buyers outside major metro areas may qualify for <a href="/usda-loans/">USDA</a> zero-down financing.</p>
<h2>Refinancing in {name}</h2><p>A <a href="/refinance/">refinance</a> can lower your payment, remove mortgage insurance or turn equity into cash. Compare closing costs with your monthly savings to see how long it takes to break even.</p>
<h2>Investing in {name} rentals</h2><p><a href="/dscr-loans/">DSCR loans</a> let investors qualify on a property's rent instead of personal income.</p>
<h2>{name} questions</h2>{faq_html(faqs)}
<p><a href="/states/">All states</a></p></article><aside class="side">{form(state=ab, heading=f"Get pre-qualified in {name}")}</aside></div>"""
        page(f"/states/{s}/", title, desc, body, [faq_schema(faqs)], crumbs=[("States", "/states/"), (name, f"/states/{s}/")])
    links = "".join(f'<li{" class=lic" if a in LICENSED else ""}><a href="/states/{slug(n)}/">{n}</a></li>' for n, a, *_ in STATES)
    body = f"""<div class="wrap page-head">{{{{CRUMBS}}}}<h1>Home loans in every state</h1>
<p class="lede">Ibex lends directly in the states in bold. Everywhere else, we connect you with a licensed partner lender.</p></div>
<div class="wrap" style="padding-bottom:4rem"><ul class="states-grid">{links}</ul></div>"""
    page("/states/", "Mortgage Lenders by State | Ibex Capital Mortgage", "Home loans in all 50 states: Ibex lends directly in CA, CO, MT, TX and FL and refers borrowers elsewhere to licensed lenders.", body, crumbs=[("States", "/states/")])


def simple(path, title, desc, h1, content, with_form=False, crumb=None, lede=""):
    side = f'<aside class="side">{form()}</aside>' if with_form else ""
    body = f"""<div class="wrap page-head">{{{{CRUMBS}}}}<h1>{E(h1)}</h1>{f'<p class="lede">{lede}</p>' if lede else ''}</div>
<div class="wrap {'page-grid' if with_form else ''}" style="padding-bottom:4rem"><article class="prose">{content}</article>{side}</div>"""
    page(path, title, desc, body, crumbs=[(crumb or h1, path)])


def other_pages():
    simple("/apply-now/", "Get Pre-Qualified | Ibex Capital Mortgage", "Start your home loan with a one-minute pre-qualification. No credit check.", "Get pre-qualified", f"""
<p>Tell us what you're looking for and a loan officer will call you, usually the same business day. There's no credit check and we won't ask for your Social Security number here.</p>
<h2>What happens next</h2><ol><li>A loan officer reviews your goals and suggests one or two loan options.</li><li>If you'd like to move forward, you'll get a link to our secure online application to upload documents.</li><li>We pull credit only with your permission, then issue a pre-approval letter.</li></ol>
<div class="callout"><p>We will never ask you to email your Social Security number, bank statements or tax returns. Use the secure application link your loan officer sends.</p></div>""", True, lede="One minute, no credit check, no obligation.")
    simple("/calculator/", "Mortgage Payment Calculator | Ibex Capital Mortgage", "Estimate your monthly mortgage payment including taxes and insurance.", "Mortgage payment calculator", CALC + """
<h2>What's included</h2><p>The estimate covers principal and interest, property tax and homeowners insurance. It doesn't include mortgage insurance, HOA dues or flood insurance, which can add to your payment.</p>""", True)
    simple("/about-us/", "About Ibex Capital Mortgage", "Ibex Capital, Inc. is a mortgage company in Encinitas, California, licensed in CA, CO, MT, TX and FL.", "About Ibex", f"""
<p>{LEGAL} is a mortgage company based in Encinitas, California. Our team has worked in mortgage lending since 1995. We're licensed to originate loans in {lic_line()}, and we work with a network of wholesale lenders, so we can shop programs instead of offering only one bank's products.</p>
<h2>How we work</h2><ul><li>We explain the rate, APR, closing costs and monthly payment for each option before you choose.</li><li>We tell you when a loan isn't a good fit, including when refinancing wouldn't save you money.</li><li>Your documents go through a secure application, never email.</li></ul>
<h2>Licensing</h2><p>NMLS #{NMLS}. Verify our license on <a href="{NMLS_URL}">NMLS Consumer Access</a>. See <a href="/licensing/">licensing</a> for details.</p>""", True)
    simple("/contact-us/", "Contact Ibex Capital Mortgage", "Call, email or visit Ibex Capital Mortgage.", "Contact us", f"""
<table class="facts"><tbody><tr><th>Phone</th><td><a href="tel:{PHONE_TEL}">{PHONE}</a> (toll-free, call or text)</td></tr><tr><th>Email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
<tr><th>Mail</th><td>{E(ADDRESS)}</td></tr><tr><th>Hours</th><td>{HOURS}; closed Sunday</td></tr></tbody></table>
<p>To stop calls or texts, reply STOP to any text or email us with the number to remove.</p>""", True)
    faqs = [("What's the difference between pre-qualification and pre-approval?", "Pre-qualification is a quick estimate based on what you tell us. Pre-approval follows a credit check and review of your income and asset documents, and it carries more weight with sellers."),
            ("What's the difference between the rate and the APR?", "The interest rate sets your monthly principal and interest. The APR includes the rate plus certain loan costs such as origination fees and points, so it's the better number for comparing offers."),
            ("Should I pay points?", "Points lower your rate in exchange for cash at closing. They pay off if you keep the loan long enough to recover the cost through lower payments."),
            ("How much house can I afford?", "Lenders look at your debt-to-income ratio, typically keeping total monthly debts, including the new payment, within about 43% to 50% of gross income depending on the loan. Use the <a href=\"/calculator/\">calculator</a> to test payments."),
            ("Can I buy with a recent bankruptcy or foreclosure?", "Yes, after a waiting period that depends on the loan type and event, often two to seven years. FHA and VA tend to be the most forgiving."),
            ("Do you lend outside California?", f"Ibex lends directly in {lic_line()}. Elsewhere we refer you to a licensed partner lender."),
            ("Is my information secure?", "Our pre-qualification form doesn't collect Social Security numbers. Full applications use an encrypted portal.")]
    body = f"""<div class="wrap page-head">{{{{CRUMBS}}}}<h1>Common questions</h1></div>
<div class="wrap page-grid"><article class="prose">{faq_html(faqs)}</article><aside class="side">{form()}</aside></div>"""
    page("/faq/", "Mortgage Questions & Answers | Ibex Capital Mortgage", "Answers about pre-approval, APR, points, affordability and credit.", body, [faq_schema(faqs)], crumbs=[("Questions", "/faq/")])
    simple("/behind-on-mortgage/", "Behind on Your Mortgage? Loan Modification & Foreclosure Options", "What to do if you've missed mortgage payments or received a foreclosure notice.", "Behind on your mortgage?", f"""
<div class="callout"><p><strong>Got a foreclosure notice?</strong> Call your mortgage servicer today and ask about loss mitigation options. Free help is available from HUD-approved housing counselors at 800-569-4287.</p></div>
<h2>Options your servicer may offer</h2><ul><li><strong>Loan modification:</strong> a permanent change to your rate, term or balance.</li><li><strong>Forbearance:</strong> a temporary pause or reduction in payments.</li><li><strong>Repayment plan:</strong> catch up over several months.</li><li><strong>Partial claim</strong> (FHA): missed payments moved to a no-interest second lien.</li><li><strong>Short sale or deed in lieu:</strong> leave the home without a foreclosure.</li></ul>
<h2>When a refinance can help</h2><p>If you have equity and enough income, refinancing can replace a loan you're struggling with. We can review whether that's realistic before you fall further behind.</p>
<h2>If other debt is the problem</h2><p>When credit cards or medical bills are making the mortgage hard to pay, <a href="{DEBT}/loan-modification/">Debt Relief Path</a> can connect you with debt settlement companies, bankruptcy attorneys (Chapter 13 can pause a foreclosure), and mortgage modification help.</p>
<h2>Avoid scams</h2><p>No one is allowed to charge you a fee for loan modification help before you've received and accepted a written offer from your lender. Never sign over your deed, pay a stranger instead of your servicer, or stop paying because someone tells you to.</p>""", True, lede="You have more options than you might think, and they shrink the longer you wait.")
    simple("/for-lenders/", "Mortgage Leads for Licensed Lenders | Ibex Capital Mortgage", "Partner with Ibex to receive consumer mortgage referrals in states where Ibex isn't licensed.", "For licensed lenders", f"""
<p>Ibex receives home loan inquiries from borrowers in all 50 states. In states where we aren't licensed, we refer those borrowers to independent lenders licensed there.</p>
<h2>What partners receive</h2><ul><li>Purchase, refinance, cash-out, VA, FHA, jumbo and DSCR inquiries by state</li><li>Borrowers who asked to be contacted, with consent records kept for each referral</li><li>Exclusive referrals by state and loan type</li></ul>
<h2>What we ask of partners</h2><ul><li>An active NMLS license in each state you want referrals for</li><li>Prompt contact, usually within one business day</li><li>Compliance with RESPA, TILA and state advertising and referral rules</li></ul>
<p>To discuss a partnership, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call {PHONE}.</p>""")
    simple("/licensing/", "Licensing & Disclosures | Ibex Capital Mortgage", f"Ibex Capital, Inc. NMLS #{NMLS} licensing information.", "Licensing and disclosures", f"""
<table class="facts"><tbody><tr><th>Company</th><td>{LEGAL}</td></tr><tr><th>NMLS ID</th><td><a href="{NMLS_URL}">{NMLS}</a></td></tr>
{"".join(f'<tr><th>{n}</th><td>Licensed{(", license " + E(LICENSED[a])) if LICENSED[a] else ""}</td></tr>' for n, a, *_ in STATES if a in LICENSED)}</tbody></table>
<p>{FOOT}</p><p>Equal Housing Opportunity. We do business in accordance with the Federal Fair Housing Act and the Equal Credit Opportunity Act.</p>""")
    simple("/privacy/", "Privacy Policy | Ibex Capital Mortgage", "How Ibex Capital Mortgage collects, uses and protects your information.", "Privacy policy", f"""
<p class="small">Last updated {TODAY}</p>
<h2>What we collect</h2><p>When you contact us or fill out a form, we collect what you give us, such as your name, phone, email, property state and ZIP, loan goal, and approximate home value and credit range. We record the consent wording you agreed to, the time and the page. If you apply for a loan, we collect the information required for the application through a secure portal.</p>
<h2>How we use and share it</h2><p>We use your information to respond to you and to provide or arrange a loan. If your property is in a state where Ibex isn't licensed, we share your inquiry with a licensed partner lender so they can contact you. We share information with service providers who help us operate, and as required by law. We don't sell your information to data brokers. Our handling of nonpublic personal information from loan applications follows the Gramm-Leach-Bliley Act; our separate privacy notice is provided at application.</p>
<h2>Your choices</h2><p>Ask us to stop contacting you, to tell you what we have, or to delete it by emailing <a href="mailto:{EMAIL}">{EMAIL}</a> or calling {PHONE}. Reply STOP to any text. California residents have additional rights under the CCPA, which you can use the same way.</p>
<h2>Security</h2><p>We use administrative, technical and physical safeguards. Never send sensitive documents by email; use your secure application link.</p>""")
    simple("/terms/", "Terms of Use | Ibex Capital Mortgage", "Terms for using the Ibex Capital Mortgage website.", "Terms of use", f"""
<p class="small">Last updated {TODAY}</p><p>Information on this site is general and isn't a commitment to lend or an offer of any rate or terms. Calculator results are estimates for illustration. All loans are subject to credit approval and underwriting. Partner lenders we refer you to are independent and responsible for their own loans. Questions: {EMAIL}.</p>""")
    simple("/ada-accessibility-statement/", "Accessibility | Ibex Capital Mortgage", "Our commitment to an accessible website.", "Accessibility", f"""
<p>We want everyone to be able to use this site. It's built to meet WCAG 2.1 AA, including keyboard navigation, visible focus, readable contrast and screen reader labels. If something doesn't work for you, call {PHONE} or email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll help you directly and fix the issue.</p>""")
    simple("/thank-you/", "Thanks | Ibex Capital Mortgage", "We received your request.", "Thanks, we got your request", f"""
<p class="lede">A loan officer will reach out soon, usually the same business day.</p><p>Need us sooner? Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p><p><a href="/">Back to home</a></p>""")
    page("/404.html", "Page not found | Ibex Capital Mortgage", "Page not found.", '<div class="wrap page-head"><h1>We couldn\'t find that page</h1><p class="lede">Try the <a href="/">home page</a> or <a href="/loan-options/">loan options</a>.</p></div>')


OLD = {  # old WordPress URLs -> new pages
    "/sample-page-2/": "/", "/news-grid/": "/faq/", "/news-list/": "/faq/", "/blog/": "/faq/",
    "/home-loans-libby-mt/": "/states/montana/", "/the-pros-and-cons-of-a-20-down-payment/": "/first-time-homebuyers/",
    "/outsmart-these-4-refinancing-obstacles/": "/refinance/", "/5-equity-boosting-home-improvements/": "/203k-loans/",
    "/3-ways-to-reduce-your-mortgage-costs/": "/refinance/", "/4-financial-planning-myths-busted/": "/faq/",
    "/adjustable-rate-mortgages-demystified/": "/loan-options/", "/new-home-checklist-before-moving-in/": "/first-time-homebuyers/",
    "/5-telltale-signs-of-an-overpriced-listing/": "/first-time-homebuyers/", "/4-property-risks-that-can-impact-financing/": "/loan-options/",
    "/can-homebuyers-save-money-by-waiting/": "/first-time-homebuyers/", "/wp-admin/*": "/", "/wp-login.php": "/", "/shop/*": "/", "/cart/*": "/",
}


def extras():
    urls = [p for p in PAGES if p not in ("/404.html", "/thank-you/")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in urls] + ["</urlset>"]
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm))
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")
    llms = [f"# {BRAND}", "", f"> {LEGAL} (NMLS #{NMLS}), a mortgage company in Encinitas, CA, licensed in {lic_line()}. Offers purchase, refinance, conventional, FHA, VA, USDA, jumbo, 203(k) and DSCR loans. In other states it refers borrowers to licensed partner lenders. Phone {PHONE}.", "", "## Loans"]
    llms += [f"- [{v['nav']}]({SITE}/{k}/)" for k, v in PROGRAMS.items()] + ["", "## States"] + [f"- [{n}]({SITE}/states/{slug(n)}/){' (Ibex licensed)' if a in LICENSED else ''}" for n, a, *_ in STATES]
    llms += ["", "## Company", f"- [Licensing]({SITE}/licensing/)", f"- [Behind on your mortgage]({SITE}/behind-on-mortgage/)", f"- Related: [Debt Relief Path]({DEBT}) for debt settlement and bankruptcy referrals"]
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(llms) + "\n")
    red = ["https://ibexcapitalmortgage.com/* https://www.ibexcapitalmortgage.com/:splat 301"] + [f"{a} {b} 301" for a, b in OLD.items()]
    open(os.path.join(ROOT, "_redirects"), "w").write("\n".join(red) + "\n")
    open(os.path.join(ROOT, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n/assets/*\n  Cache-Control: public, max-age=604800\n")
    open(os.path.join(ROOT, "assets", "favicon.svg"), "w").write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))


if __name__ == "__main__":
    home(); program_pages(); state_pages(); other_pages(); extras()
    print(f"Built {len(PAGES)} pages")
