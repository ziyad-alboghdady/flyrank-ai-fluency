// Progressive enhancement: keep the user on the page after a Formspree submit.
// Without JS the form still posts normally and Formspree shows its own page.
const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');
form?.addEventListener('submit', async (e) => {
  if (!form.action.includes('formspree.io') || form.action.includes('REPLACE_ME')) return;
  e.preventDefault();
  status.hidden = false; status.className = 'status'; status.textContent = 'Sending…';
  try {
    const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
    if (res.ok) { form.reset(); status.className = 'status ok'; status.textContent = 'Sent. I reply within a day or two.'; }
    else { throw new Error('Bad response ' + res.status); }
  } catch (err) {
    status.className = 'status err';
    status.innerHTML = 'That did not go through. Email me directly at <a href="mailto:ziyadalboghdady@gmail.com">ziyadalboghdady@gmail.com</a>.';
  }
});
