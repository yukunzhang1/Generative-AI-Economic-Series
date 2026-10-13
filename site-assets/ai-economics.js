(function () {
  'use strict';
  const root = document.querySelector('.ge-series');
  if (!root) return;
  const toggle = root.querySelector('.ge-language');
  function setLanguage(lang) {
    root.dataset.geLanguage = lang;
    root.lang = lang === 'zh' ? 'zh-Hans' : 'en';
    toggle.textContent = lang === 'zh' ? 'English' : '中文';
    toggle.setAttribute('aria-label', lang === 'zh' ? 'Switch to English' : '切换至中文');
  }
  let lang = 'en';
  try { if (localStorage.getItem('ge-language') === 'zh') lang = 'zh'; } catch (e) {}
  setLanguage(lang);
  toggle.hidden = false;
  toggle.addEventListener('click', function () {
    const next = root.dataset.geLanguage === 'en' ? 'zh' : 'en';
    setLanguage(next);
    try { localStorage.setItem('ge-language', next); } catch (e) {}
  });
  const copy = root.querySelector('.ge-copy');
  if (copy && navigator.clipboard) {
    copy.hidden = false;
    copy.addEventListener('click', async function () {
      const status = root.querySelector('.ge-copy-status');
      const zh = root.dataset.geLanguage === 'zh';
      try {
        await navigator.clipboard.writeText(root.querySelector('.ge-citation code').textContent);
        status.textContent = zh ? '已复制' : 'Copied';
      } catch (e) {
        status.textContent = zh ? '请选中上方文本复制' : 'Select the citation above to copy it.';
      }
    });
  }
})();
