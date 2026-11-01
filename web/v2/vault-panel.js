/* Isolated mount seam: host supplies authenticated request, not a stored token. */
export function mountVault(root, {caseId, request}) {
  if (!root || typeof request !== 'function' || !caseId) throw new Error('Vault mount context required.');
  const base = `/api/v2/cases/${encodeURIComponent(caseId)}/vault`;
  let disposed = false, epoch = 0, busy = false, uncertain = false, objects = [], message = '';
  const el = (tag, text, attrs = {}) => {
    const node = document.createElement(tag);
    if (text !== null) node.textContent = text;
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    return node;
  };
  const button = (label, action, disabled = busy || uncertain) => {
    const node = el('button', label, {type: 'button'});
    node.disabled = disabled;
    node.addEventListener('click', action);
    return node;
  };
  async function refresh() {
    const generation = ++epoch;
    busy = true; objects = []; render();
    try {
      const result = await request(base);
      if (disposed || generation !== epoch) return;
      objects = result; uncertain = false; message = 'Current vault state loaded. No facts or permissions changed.';
    } catch (error) {
      if (disposed || generation !== epoch) return;
      objects = []; uncertain = true; message = error.message || 'Access unavailable.';
    } finally {
      if (!disposed && generation === epoch) { busy = false; render(); }
    }
  }
  async function mutate(path, body) {
    const generation = epoch;
    busy = true; render();
    try {
      await request(path, {method: 'POST', body});
      if (disposed || generation !== epoch) return;
      await refresh();
    } catch (error) {
      if (disposed || generation !== epoch) return;
      busy = false; uncertain = true; objects = [];
      message = `${error.message || 'Request failed.'} The outcome may be unknown. Refresh before another command; no automatic retry.`;
      render();
    }
  }
  function render() {
    if (disposed) return;
    root.replaceChildren(); root.classList.add('vault-panel');
    root.append(el('h2', 'Evidence vault'), el('p', 'Fictional/local engineering only. Uploads remain quarantined until an explicitly configured scan releases them. A clean scan does not verify any claim.'),
      el('p', message || (busy ? 'Loading…' : ''), {role: 'status', 'aria-live': 'polite'}),
      button('Refresh vault', refresh, busy));
    const form = el('form', null), file = el('input', null, {type: 'file', accept: '.txt,.md', required: ''});
    const date = el('input', null, {type: 'datetime-local', required: ''});
    const fileLabel = el('label', 'Exact UTF-8 original (maximum 256 KiB) ');
    const dateLabel = el('label', 'Retain until (your local timezone; server minimum applies) ');
    fileLabel.append(file); dateLabel.append(date); form.append(fileLabel, dateLabel);
    const upload = el('button', 'Upload into quarantine', {type: 'submit'});
    upload.disabled = busy || uncertain; file.disabled = busy || uncertain; date.disabled = busy || uncertain;
    form.append(upload);
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (busy || uncertain || !file.files[0]) return;
      const selected = file.files[0], generation = epoch;
      if (selected.size > 262144 || selected.size === 0) {
        message = 'Choose a non-empty UTF-8 text original no larger than 256 KiB.'; render(); return;
      }
      busy = true; upload.disabled = true;
      try {
        const bytes = new Uint8Array(await selected.arrayBuffer());
        if (disposed || generation !== epoch) return;
        new TextDecoder('utf-8', {fatal: true}).decode(bytes);
        let binary = '';
        for (const value of bytes) binary += String.fromCharCode(value);
        await mutate(base, {filename: selected.name, content_base64: btoa(binary),
          media_type: selected.name.toLowerCase().endsWith('.md') ? 'text/markdown' : 'text/plain',
          retain_until: new Date(date.value).toISOString(), command_id: crypto.randomUUID()});
      } catch (error) {
        if (!disposed && generation === epoch) { busy = false; message = 'File/date could not be read; nothing was sent.'; render(); }
      }
    });
    root.append(form);
    for (const obj of objects) {
      const section = el('section', null, {'aria-label': `Original ${obj.object_id}`});
      section.append(el('h3', obj.filename), el('p', `${obj.status} · original v${obj.version} · vault revision ${obj.vault_revision}`),
        el('p', `SHA-256 ${obj.sha256}`), el('p', `${obj.size_bytes} bytes · retention ${obj.retain_until} · hold ${obj.hold ? 'active' : 'none'}`));
      const path = `${base}/${encodeURIComponent(obj.object_id)}`;
      const command = () => ({expected_revision: obj.vault_revision, command_id: crypto.randomUUID()});
      if (['quarantined', 'scan_failed'].includes(obj.status)) section.append(button('Request explicit scan', () => mutate(`${path}/scan`, command())));
      if (obj.status === 'released') section.append(button('Download released original', async () => {
        const generation = epoch;
        busy = true; render();
        try {
          const blob = await request(`${path}/download`, {method: 'POST', body: {
            expected_revision: obj.vault_revision, expected_sha256: obj.sha256}, responseType: 'blob'});
          if (disposed || generation !== epoch) return;
          const url = URL.createObjectURL(blob), link = el('a', 'Download', {href: url, download: obj.filename});
          link.click(); URL.revokeObjectURL(url);
          message = 'Original downloaded. This does not attest its contents.';
        } catch (error) {
          if (!disposed && generation === epoch) { objects = []; uncertain = true; message = 'Download unavailable. Refresh and recheck access.'; }
        } finally {
          if (!disposed && generation === epoch) { busy = false; render(); }
        }
      }));
      if (obj.status !== 'deleted_local') {
        const policy = el('form', null), reason = el('input', null, {required: '', minlength: '10', maxlength: '1000'});
        const label = el('label', 'Explicit policy rationale '); label.append(reason);
        const until = el('input', null, {type: 'datetime-local'}), untilLabel = el('label', 'New retention deadline '); untilLabel.append(until);
        policy.append(label, untilLabel);
        const act = (suffix, extra = {}) => {
          if (!reason.reportValidity()) return;
          mutate(`${path}/${suffix}`, {...command(), reason: reason.value, ...extra});
        };
        policy.append(button(obj.hold ? 'Release hold' : 'Apply hold', () => act('hold', {hold: !obj.hold})),
          button('Set retention', () => { if (until.value) act('retention', {retain_until: new Date(until.value).toISOString()}); }),
          button('Delete local ciphertext', () => {
            if (window.confirm('Delete this local ciphertext only? Retention, hold and dependent-source clearance must permit it. Backups and derived copies are NOT erased by this operation.')) act('delete-local');
          }));
        if (obj.status === 'scanning') policy.append(button('Cancel scan publication', () => act('cancel-scan')));
        section.append(policy);
      }
      root.append(section);
    }
  }
  refresh();
  return {refresh, dispose() { disposed = true; epoch++; objects = []; root.replaceChildren(); }};
}
