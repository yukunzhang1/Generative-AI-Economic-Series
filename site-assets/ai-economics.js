(function(){
  'use strict';
  const button=document.querySelector('.language');
  if(!button)return;
  function setLanguage(value){const zh=value==='zh';document.documentElement.lang=zh?'zh-Hans':'en';button.textContent=zh?'English':'中文';button.setAttribute('aria-label',zh?'Switch to English':'切换至中文');}
  let language='en';try{if(localStorage.getItem('ge-language')==='zh')language='zh';}catch(_){}
  setLanguage(language);button.hidden=false;
  button.addEventListener('click',function(){language=document.documentElement.lang==='en'?'zh':'en';setLanguage(language);try{localStorage.setItem('ge-language',language);}catch(_){}});
  const dialog=document.querySelector('.image-dialog');
  if(!dialog || !dialog.showModal)return;
  let trigger;
  document.querySelectorAll('.paper-image').forEach(link=>link.addEventListener('click',event=>{
    if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
    event.preventDefault();trigger=link;
    const original=link.querySelector('img');dialog.querySelector('img').src=original.src;dialog.querySelector('img').alt=original.alt;
    dialog.querySelector('.dialog-title').textContent=link.closest('article').querySelector('h3').textContent;
    dialog.querySelector('.figure-source a').href=link.dataset.source;dialog.showModal();
  }));
  dialog.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',event=>{if(event.target===dialog){const b=dialog.getBoundingClientRect();if(event.clientX<b.left||event.clientX>b.right||event.clientY<b.top||event.clientY>b.bottom)dialog.close();}});
  dialog.addEventListener('close',()=>{if(trigger)trigger.focus();});
})();
