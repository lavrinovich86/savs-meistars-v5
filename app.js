// SAVS meistars — versija 05.
// Bez atkarībām. Viss darbojas arī tad, ja skripts neielādējas: visi slāņi
// tad paliek redzami, izvēlne ir atvērta saraksta veidā, un forma paļaujas
// uz pārlūka validāciju.

(function () {
  'use strict';

  // --- mobilā izvēlne -------------------------------------------------------

  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');

  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (ev) {
      if (ev.target.closest('a')) {
        nav.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // --- rasējumu slāņi -------------------------------------------------------
  // Slāņi ir uzklājami: katrs slēdzis pievieno vai noņem savu slāni virsū
  // pārējiem, nevis pārslēdz skatu. Izslēgto slāņu saraksts glabājas
  // paša SVG data-off atribūtā, un CSS to nolasa.

  function setLayer(svg, layer, on) {
    var off = (svg.getAttribute('data-off') || '').split(/\s+/).filter(Boolean);
    var at = off.indexOf(layer);
    if (on && at !== -1) off.splice(at, 1);
    if (!on && at === -1) off.push(layer);
    if (off.length) svg.setAttribute('data-off', off.join(' '));
    else svg.removeAttribute('data-off');
  }

  Array.prototype.forEach.call(document.querySelectorAll('.layer'), function (btn) {
    btn.addEventListener('click', function () {
      var svg = document.getElementById(btn.dataset.target);
      if (!svg) return;
      var on = btn.getAttribute('aria-pressed') !== 'true';
      btn.setAttribute('aria-pressed', String(on));
      setLayer(svg, btn.dataset.layer, on);
    });
  });

  // --- pakalpojuma izvēle no kartes ----------------------------------------

  Array.prototype.forEach.call(document.querySelectorAll('[data-service]'), function (card) {
    card.addEventListener('click', function () {
      var sel = document.getElementById('f-service');
      if (sel) sel.value = card.dataset.service;
    });
  });

  // --- kontaktforma ---------------------------------------------------------

  var form = document.getElementById('form');
  if (!form) return;

  var fields = [
    { input: 'f-name', err: 'e-name' },
    { input: 'f-contact', err: 'e-contact' },
    { input: 'f-msg', err: 'e-msg' }
  ];

  function check(f) {
    var el = document.getElementById(f.input);
    var err = document.getElementById(f.err);
    var ok = el.value.trim().length > 0;
    err.hidden = ok;
    el.setAttribute('aria-invalid', String(!ok));
    return ok;
  }

  fields.forEach(function (f) {
    document.getElementById(f.input).addEventListener('input', function () {
      if (document.getElementById(f.err).hidden === false) check(f);
    });
  });

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    var ok = true;
    var first = null;
    fields.forEach(function (f) {
      if (!check(f)) {
        ok = false;
        if (!first) first = document.getElementById(f.input);
      }
    });
    if (!ok) { first.focus(); return; }

    var sel = document.getElementById('f-service');
    var subject = 'Iecere: ' + sel.options[sel.selectedIndex].text;
    var body = [
      'Vārds: ' + document.getElementById('f-name').value.trim(),
      'Saziņai: ' + document.getElementById('f-contact').value.trim(),
      'Joma: ' + sel.options[sel.selectedIndex].text,
      '',
      document.getElementById('f-msg').value.trim()
    ].join('\n');

    window.location.href = 'mailto:info@savs.lv?subject='
      + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });
}());
