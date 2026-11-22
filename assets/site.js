(() => {
  'use strict';
  const key = 'yanan-site-language';
  const body = document.body;
  // Explicit language URLs always take precedence; only the root restores a preference.
  try {
    if (body.dataset.root === 'true' && localStorage.getItem(key) === 'en') {
      location.replace('/en/' + location.search + location.hash);
      return;
    }
    if (body.dataset.root !== 'true') localStorage.setItem(key, body.dataset.language);
  } catch (_) { /* Language links also work when storage is unavailable. */ }
  document.querySelectorAll('.lang-link').forEach(link => {
    link.addEventListener('click', () => {
      try { localStorage.setItem(key, link.dataset.lang); } catch (_) {}
      link.href = new URL(link.getAttribute('href'), location.origin).pathname + location.search + location.hash;
    });
  });
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  if (toggle && nav) {
    document.documentElement.classList.add('js');
    const close = () => { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); };
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') { close(); toggle.focus(); } });
    document.addEventListener('click', event => { if (!event.target.closest('.header-inner')) close(); });
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', close));
  }
})();
