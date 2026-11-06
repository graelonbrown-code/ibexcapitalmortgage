// Emails each pre-qualification request. Deploy: cd worker && npx wrangler deploy
const LICENSED = ['CA', 'CO', 'MT', 'TX', 'FL'];
const allowed = /^https:\/\/((www\.)?ibexcapitalmortgage\.com|([a-z0-9-]+\.)?ibexcapitalmortgage\.pages\.dev)$/;
const clean = (v, n) => String(v ?? '').replace(/[\r\n\t]+/g, ' ').trim().slice(0, n);
const json = (body, status) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });

export default {
  async fetch(request, env) {
    if (request.method !== 'POST') return json({ ok: false, error: 'Use the form to send a request.' }, 405);
    const origin = request.headers.get('origin') || '';
    if (!allowed.test(origin)) return json({ ok: false, error: 'This request was not sent from our site.' }, 403);
    let d; try { d = await request.json(); } catch { return json({ ok: false, error: 'Check the form and try again.' }, 400); }
    if (d.website) return json({ ok: true }, 200); // hidden field only bots fill in
    const lead = { goal: clean(d.goal, 60), state: clean(d.state, 4).toUpperCase(), zip: clean(d.zip, 10), value: clean(d.value, 30),
      credit: clean(d.credit, 30), name: clean(d.name, 120), phone: clean(d.phone, 30), email: clean(d.email, 160) };
    if (!lead.goal || !lead.state || !lead.name || lead.phone.replace(/\D/g, '').length < 10 ||
        !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(lead.email) || d.consent !== true)
      return json({ ok: false, error: 'Fill in every field and check the consent box.' }, 400);
    const route = LICENSED.includes(lead.state) ? 'IBEX (licensed state)' : 'PARTNER REFERRAL (Ibex not licensed)';
    const text = `New pre-qualification request from ibexcapitalmortgage.com\n\nRoute: ${route}\nGoal: ${lead.goal}\nState: ${lead.state}  ZIP: ${lead.zip}\nHome price/value: ${lead.value}\nCredit: ${lead.credit}\nName: ${lead.name}\nPhone: ${lead.phone}\nEmail: ${lead.email}\nContact consent: Yes (wording version ${clean(d.consentVersion, 20)})\nSubmitted: ${new Date().toISOString()}\nIP: ${request.headers.get('CF-Connecting-IP') || ''}\nPage: ${clean(request.headers.get('referer'), 200)}\n`;
    try {
      await env.LEADS.send({ from: { email: 'leads@ibexcapitalmortgage.com', name: 'Ibex Capital Mortgage' }, to: 'graelon.brown@gmail.com',
        replyTo: lead.email, subject: `Ibex lead: ${lead.goal} - ${lead.state} - ${route.startsWith('IBEX') ? 'Ibex' : 'Partner'}`, text });
      return json({ ok: true }, 200);
    } catch (e) {
      console.error('send failed', e && e.code);
      return json({ ok: false, error: "We couldn't send your request. Please call 888-699-5777." }, 502);
    }
  },
};
