(function () {
  'use strict';
  const button = document.querySelector('.language');
  if (!button) return;
  function setLanguage(value) {
    const chinese = value === 'zh';
    document.documentElement.lang = chinese ? 'zh-Hans' : 'en';
    button.textContent = chinese ? 'English' : '中文';
    button.setAttribute('aria-label', chinese ? 'Switch to English' : '切换至中文');
  }
  let language = 'en';
  try { if (localStorage.getItem('ge-language') === 'zh') language = 'zh'; } catch (_) {}
  setLanguage(language);
  button.hidden = false;
  button.addEventListener('click', function () {
    language = document.documentElement.lang === 'en' ? 'zh' : 'en';
    setLanguage(language);
    try { localStorage.setItem('ge-language', language); } catch (_) {}
  });
})();
