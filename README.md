# ibexcapitalmortgage.com

Static site for Ibex Capital Mortgage on Cloudflare Pages. 75 pages: home with payment calculator, 9 loan program pages, 50 state pages (CA, CO, MT, TX, FL as Ibex-licensed; the rest as partner-lender referrals), pre-qualification, calculator, FAQ, about, contact, licensing, for-lenders, behind-on-mortgage, privacy, terms, accessibility.

## Edit and rebuild

Copy lives in `src/build.py`; state list in `src/states.py`. Licensed states and license numbers are in `LICENSED` at the top of `build.py` (numbers show on the site once filled in). Run `python3 src/build.py`, commit, push.

## Go-live steps (one time)

1. **Move DNS to Cloudflare.** Cloudflare > Add a site > ibexcapitalmortgage.com. Before switching nameservers at your registrar, confirm Cloudflare copied the **MX and TXT records** for info@ibexcapitalmortgage.com, or email will stop.
2. **Pages project.** Workers & Pages > Create > Pages > Connect to Git > this repo. Build command `node src/build.mjs`, output folder `dist`. Add custom domains `www.ibexcapitalmortgage.com` and `ibexcapitalmortgage.com`.
3. **Lead emails.** Turn on Email Routing for the domain and confirm graelon.brown@gmail.com as a destination. Then in `worker/` run `npx wrangler deploy`. Each lead email's subject says "Ibex" (licensed state) or "Partner" (refer out).
4. **Retire WordPress.** Once the new site is live on the domain, cancel the old WordPress hosting. Old page and blog URLs redirect to the new pages (`_redirects`).
5. Submit `https://www.ibexcapitalmortgage.com/sitemap.xml` in Google Search Console.

## Before launch

- Attorney review of the 45-state partner referral model: approved 2026-11-06.
- Add state license numbers to `LICENSED` if your states require them in ads.
- Add your secure application (loan software) link if you want an "Apply" button beyond pre-qualification.
