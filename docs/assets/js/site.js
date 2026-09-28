(function () {
  'use strict';

  var DEMO_NOTE = 'Это демо-версия сайта: заявка никуда не отправлена. На рабочем сайте администратор перезвонит вам в рабочее время.';

  // Мобильное меню
  var burger = document.querySelector('.burger');
  if (burger) {
    var header = document.querySelector('.header');
    var setNav = function (open) {
      if (open && header) {
        document.documentElement.style.setProperty('--nav-top', Math.max(0, header.getBoundingClientRect().bottom) + 'px');
      }
      document.body.classList.toggle('nav-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    };
    burger.addEventListener('click', function () {
      setNav(!document.body.classList.contains('nav-open'));
    });
    document.querySelectorAll('.mobile-nav a, .mobile-nav button').forEach(function (el) {
      el.addEventListener('click', function () { setNav(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setNav(false);
    });
  }

  // Маска телефона: +7 (___) ___-__-__
  function formatPhone(value) {
    var d = value.replace(/\D/g, '');
    if (d.charAt(0) === '8') d = '7' + d.slice(1);
    if (d && d.charAt(0) !== '7') d = '7' + d;
    d = d.slice(0, 11);
    if (!d) return '';
    var out = '+7';
    if (d.length > 1) out += ' (' + d.slice(1, 4);
    if (d.length >= 4) out += ')';
    if (d.length > 4) out += ' ' + d.slice(4, 7);
    if (d.length > 7) out += '-' + d.slice(7, 9);
    if (d.length > 9) out += '-' + d.slice(9, 11);
    return out;
  }
  document.addEventListener('input', function (e) {
    if (e.target.matches && e.target.matches('input[type="tel"]')) {
      e.target.value = formatPhone(e.target.value);
    }
  });

  // Формы записи
  function setError(field, on) {
    var wrap = field.closest('.field, .consent');
    if (wrap) wrap.classList.toggle('has-error', on);
    field.setAttribute('aria-invalid', on ? 'true' : 'false');
  }

  function successHtml(name) {
    var hello = name ? 'Спасибо, ' + name.replace(/[<>&"]/g, '') + '!' : 'Спасибо!';
    return '<div class="form-success" role="status">' +
      '<span class="ok"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg></span>' +
      '<b>' + hello + ' Заявка принята</b>' +
      '<p>' + DEMO_NOTE + '</p>' +
      '</div>';
  }

  function bindForm(form) {
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.querySelector('[name="name"]');
      var phone = form.querySelector('[name="phone"]');
      var consent = form.querySelector('[name="consent"]');
      var ok = true;
      if (name) {
        var badName = name.value.trim().length < 2;
        setError(name, badName);
        ok = ok && !badName;
      }
      if (phone) {
        var badPhone = phone.value.replace(/\D/g, '').length !== 11;
        setError(phone, badPhone);
        ok = ok && !badPhone;
      }
      if (consent) {
        setError(consent, !consent.checked);
        ok = ok && consent.checked;
      }
      if (!ok) {
        var first = form.querySelector('[aria-invalid="true"]');
        if (first) first.focus();
        return;
      }
      var body = form.querySelector('.form-body') || form;
      body.innerHTML = successHtml(name ? name.value.trim() : '');
    });
    form.addEventListener('input', function (e) {
      if (e.target.getAttribute('aria-invalid') === 'true') setError(e.target, false);
    });
  }
  document.querySelectorAll('form[data-booking]').forEach(bindForm);

  // Окно записи
  var dialog = document.getElementById('booking');
  if (dialog && typeof dialog.showModal === 'function') {
    var template = dialog.querySelector('.form-body').innerHTML;
    var reset = function () {
      dialog.querySelector('.form-body').innerHTML = template;
    };
    document.querySelectorAll('[data-book]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        reset();
        var dir = btn.getAttribute('data-direction');
        var doc = btn.getAttribute('data-doctor');
        var dirSelect = dialog.querySelector('[name="direction"]');
        var docSelect = dialog.querySelector('[name="doctor"]');
        if (dir && dirSelect) dirSelect.value = dir;
        if (doc && docSelect) docSelect.value = doc;
        var title = dialog.querySelector('[data-title]');
        if (title) title.textContent = btn.getAttribute('data-book-title') || 'Запись на приём';
        dialog.showModal();
        var first = dialog.querySelector('input[name="name"]');
        if (first) first.focus();
      });
    });
    dialog.addEventListener('click', function (e) {
      if (e.target === dialog) dialog.close();
    });
    dialog.querySelectorAll('[data-close]').forEach(function (b) {
      b.addEventListener('click', function () { dialog.close(); });
    });
  }

  // Фильтр врачей
  document.querySelectorAll('[data-filter]').forEach(function (group) {
    var target = document.getElementById(group.getAttribute('data-filter'));
    if (!target) return;
    var buttons = group.querySelectorAll('button[data-value]');
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var value = btn.getAttribute('data-value');
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
        target.querySelectorAll('[data-tags]').forEach(function (card) {
          var tags = card.getAttribute('data-tags').split(' ');
          card.hidden = value !== 'all' && tags.indexOf(value) === -1;
        });
        target.scrollLeft = 0;
      });
    });
  });

  // Стрелки прокрутки карточек
  document.querySelectorAll('[data-scroll]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.getElementById(btn.getAttribute('data-target'));
      if (!target) return;
      var card = target.querySelector('[data-tags]:not([hidden])');
      var step = card ? card.getBoundingClientRect().width + 20 : target.clientWidth * 0.8;
      target.scrollBy({ left: btn.getAttribute('data-scroll') === 'next' ? step : -step, behavior: 'smooth' });
    });
  });
})();
