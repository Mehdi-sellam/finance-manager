// Basic enhancements for navigation and form UX
(function(){
  function qs(sel){ return document.querySelector(sel); }
  function on(el, ev, cb){ if(el){ el.addEventListener(ev, cb); } }

  // Auto-focus first input in forms
  var firstInput = document.querySelector('form input, form select');
  if(firstInput){ firstInput.focus(); }

  // Namespace filter navigation
  var nsSel = qs('#namespace-select');
  on(nsSel, 'change', function(){
    var v = nsSel.value;
    var url = new URL(window.location.href);
    if(v){ url.searchParams.set('namespace_id', v); }
    else { url.searchParams.delete('namespace_id'); }
    window.location.href = url.toString();
  });

  // Popup messages
  function showPopup(msgs){
    if(!msgs || !msgs.length) return;
    var overlay = document.createElement('div');
    overlay.className = 'popup-overlay';
    var box = document.createElement('div');
    box.className = 'popup-box';
    var list = document.createElement('ul');
    msgs.forEach(function(m){
      var li = document.createElement('li');
      li.textContent = m.text || '';
      if(m.tags){ li.className = m.tags; }
      list.appendChild(li);
    });
    var btn = document.createElement('button');
    btn.textContent = 'Close';
    btn.addEventListener('click', function(){ document.body.removeChild(overlay); });
    box.appendChild(list);
    box.appendChild(btn);
    overlay.appendChild(box);
    document.body.appendChild(overlay);
  }
  if(window._msgs && Array.isArray(window._msgs)){ showPopup(window._msgs); }

  // Client-side validation: account create
  var accForm = qs('#account-create-form');
  on(accForm, 'submit', function(e){
    var ns = qs('form select[name="namespace_id"]');
    var name = qs('form input[name="name"]');
    var cur = qs('form select[name="currency"]');
    var errs = [];
    if(ns && !ns.value){ errs.push({ text: 'Namespace is required', tags: 'error' }); }
    if(name && !name.value.trim()){ errs.push({ text: 'Name is required', tags: 'error' }); }
    if(cur && !cur.value){ errs.push({ text: 'Currency is required', tags: 'error' }); }
    if(errs.length){ e.preventDefault(); showPopup(errs); }
  });

  // Client-side validation: simple transaction forms
  function validateTxn(formSel){
    var form = qs(formSel);
    on(form, 'submit', function(e){
      var acc = form ? form.querySelector('select[name="account_id"]') : null;
      var amount = form ? form.querySelector('input[name="amount"]') : null;
      var cur = form ? form.querySelector('select[name="currency"]') : null;
      var errs = [];
      if(acc && !acc.value){ errs.push({ text: 'Account is required', tags: 'error' }); }
      if(amount && (!amount.value || parseFloat(amount.value) <= 0)){ errs.push({ text: 'Amount must be positive', tags: 'error' }); }
      if(cur && !cur.value){ errs.push({ text: 'Currency is required', tags: 'error' }); }
      if(errs.length){ e.preventDefault(); showPopup(errs); }
    });
  }
  validateTxn('#transaction-in-form');
  validateTxn('#transaction-out-form');

  // Namespace switcher on namespace detail page
  var nsSwitch = qs('#ns-switch-select');
  on(nsSwitch, 'change', function(){
    var v = nsSwitch.value;
    if(v){ window.location.href = '/namespaces/' + v + '/'; }
  });
})();
