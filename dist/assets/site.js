(function () {
  var num = function (s) { return parseFloat(String(s).replace(/[^0-9.]/g, "")) || 0; };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };

  document.querySelectorAll("[data-calc]").forEach(function (c) {
    var q = function (id) { return c.querySelector("#" + id); };
    function run() {
      var price = num(q("c-price").value), down = num(q("c-down").value);
      var rate = num(q("c-rate").value) / 100 / 12, n = num(q("c-term").value) * 12;
      var loan = Math.max(price - down, 0);
      var pi = rate ? loan * rate / (1 - Math.pow(1 + rate, -n)) : loan / n;
      var tax = price * num(q("c-tax").value) / 100 / 12, ins = num(q("c-ins").value) / 12;
      c.querySelector("[data-out]").textContent = money(pi + tax + ins) + "/mo";
      c.querySelector("[data-break]").textContent = "Principal & interest " + money(pi) + " · Taxes " + money(tax) + " · Insurance " + money(ins) + " · Loan amount " + money(loan);
    }
    c.addEventListener("input", run);
    run();
  });

  document.querySelectorAll("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = form.querySelector(".msg");
      msg.className = "msg";
      var d = {};
      new FormData(form).forEach(function (v, k) { d[k] = String(v).trim(); });
      var missing = [];
      if (!d.goal) missing.push("what you'd like to do");
      if (!d.state) missing.push("the property state");
      if (!d.first_name || !d.last_name) missing.push("your name");
      if ((d.phone || "").replace(/\D/g, "").length < 10) missing.push("a 10-digit phone number");
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email || "")) missing.push("a valid email");
      if (d.consent !== "yes") missing.push("the consent checkbox");
      if (missing.length) { msg.className = "msg err"; msg.textContent = "Please add " + missing.join(", ") + "."; return; }
      var payload = { goal: d.goal, state: d.state, zip: d.zip, value: d.value, credit: d.credit,
        name: d.first_name + " " + d.last_name, phone: d.phone, email: d.email,
        consent: true, consentVersion: "2026-11-06", website: d.website || "" };
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true; btn.textContent = "Sending...";
      fetch("/api/lead", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) { if (!r.ok) throw new Error(); location.href = "/thank-you/"; })
        .catch(function () {
          btn.disabled = false; btn.textContent = "Get pre-qualified";
          msg.className = "msg err"; msg.textContent = "Your request didn't go through. Try again, or call 888-699-5777.";
        });
    });
  });
})();
