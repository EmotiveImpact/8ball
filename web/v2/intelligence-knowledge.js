// An isolated mount: the authenticated caller supplies case-scoped API methods.
export function mountKnowledge(root, api) {
  let generation = 0;
  let disposed = false;
  const node = (tag, text) => {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    return element;
  };
  const heading = node('h2', 'Reviewed reference library');
  const notice = node('p', 'Hypotheses only. A review never verifies facts, approves actions or changes a selected course. Search stays within this case and matter.');
  const form = node('form');
  const label = node('label', 'Search title and summary ');
  const query = node('input');
  query.type = 'search';
  query.maxLength = 300;
  label.append(query);
  const submit = node('button', 'Search');
  submit.type = 'submit';
  const status = node('p');
  status.setAttribute('role', 'status');
  const results = node('div');
  const detail = node('section');
  detail.setAttribute('aria-label', 'Exact reference and review');
  root.classList.add('intelligence-knowledge');
  form.append(label, submit);
  root.replaceChildren(heading, notice, form, status, results, detail);

  const error = () => { status.textContent = 'Unable to load this reference. Access, source support or revision may have changed. Reload to retry.'; };
  async function open(itemId) {
    const current = ++generation;
    detail.replaceChildren();
    status.textContent = 'Loading exact version and source support…';
    try {
      const data = await api.read(itemId, {history: true});
      if (disposed || current !== generation) return;
      status.textContent = '';
      const item = data.item;
      const title = node('h3', item.draft.title);
      title.tabIndex = -1;
      detail.append(title, node('p', `${item.draft.kind} · version ${item.version} · ${data.retired ? 'retired' : item.review_status}`), node('p', `Exact draft SHA-256: ${item.draft_sha256}`));
      for (const [key, title] of [['summary', 'Summary'], ['assumptions', 'Assumptions'], ['authority_requirements', 'Authority requirements'], ['confirmation_criteria', 'Confirmation criteria'], ['limitations', 'Limitations']]) {
        detail.append(node('h4', title), node('p', Array.isArray(item.draft[key]) ? item.draft[key].join('\n') : item.draft[key]));
      }
      detail.append(node('h4', 'Exact source support'));
      for (const support of item.draft.sources) {
        detail.append(node('p', `${support.source_id} · code points ${support.start}–${support.end} · SHA-256 ${support.sha256}`), node('blockquote', support.quote));
      }
      if (!item.draft.sources.length) detail.append(node('p', 'No source references: starter hypothesis only.'));
      const history = node('details');
      history.append(node('summary', 'Inspect exact graph and immutable history'), node('pre', JSON.stringify({graph: item.draft.graph, history: data.history}, null, 2)));
      detail.append(history);
      if (!data.retired) reviewForm(data, current);
      title.focus();
    } catch {
      if (!disposed && current === generation) error();
    }
  }

  function reviewForm(data, current) {
    const form = node('form');
    const verdictLabel = node('label', 'Review disposition ');
    const verdict = node('select');
    for (const [value, text] of [['', 'Choose explicitly'], ['use_as_reference', 'Use as reference hypothesis'], ['needs_changes', 'Needs changes'], ['reject', 'Reject']]) {
      const option = node('option', text);
      option.value = value;
      verdict.append(option);
    }
    verdict.required = true;
    verdictLabel.append(verdict);
    const rationaleLabel = node('label', 'Reason for this exact version ');
    const rationale = node('textarea');
    rationale.required = true;
    rationale.maxLength = 12000;
    rationaleLabel.append(rationale);
    const scopeLabel = node('label', 'Your specialist review scope (not certification) ');
    const scope = node('input');
    scope.required = true;
    scope.maxLength = 180;
    scopeLabel.append(scope);
    const save = node('button', 'Record review of this version');
    save.type = 'submit';
    const requestId = crypto.randomUUID().replaceAll('-', '');
    form.append(verdictLabel, rationaleLabel, scopeLabel, save);
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (disposed || current !== generation || !form.reportValidity()) return;
      save.disabled = true;
      status.textContent = 'Recording review; this does not approve any action…';
      try {
        await api.write(data.item.item_id, {
          expected_revision: data.revision, expected_case_revision: data.case_revision,
          request_id: requestId, review: {version: data.item.version,
            draft_sha256: data.item.draft_sha256, verdict: verdict.value,
            rationale: rationale.value, specialist_scope: scope.value}
        });
        if (!disposed && current === generation) await open(data.item.item_id);
      } catch {
        if (!disposed && current === generation) {
          status.textContent = 'Review was not confirmed. Reload the exact version before retrying; no automatic retry was sent.';
        }
      }
    });
    detail.append(form);
  }

  async function search(event) {
    event?.preventDefault();
    const current = ++generation;
    detail.replaceChildren();
    results.replaceChildren();
    status.textContent = 'Checking current access and source support…';
    try {
      const data = await api.search(query.value);
      if (disposed || current !== generation) return;
      status.textContent = data.items.length ? (data.truncated ? 'Results limited. Narrow your search.' : 'Current accessible references. Lexical matches are not semantic recommendations.') : 'No accessible references matched in this checked case. This is not a global negative conclusion.';
      for (const item of data.items) {
        const button = node('button', `${item.draft.title} · v${item.version} · ${item.review_status}`);
        button.type = 'button';
        button.addEventListener('click', () => open(item.item_id));
        results.append(button);
      }
    } catch {
      if (!disposed && current === generation) error();
    }
  }
  form.addEventListener('submit', search);
  search();
  return () => { disposed = true; generation++; root.replaceChildren(); root.classList.remove('intelligence-knowledge'); };
}
