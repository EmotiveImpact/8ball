// Isolated mount seam: never reads or stores an identity token in JavaScript.
export function mountIdentity(container, {apiBase = '/api/v2'} = {}) {
  const title = document.createElement('h2');
  title.textContent = 'Agency identity';
  const status = document.createElement('p');
  status.setAttribute('role', 'status');
  const note = document.createElement('p');
  note.textContent = 'Sign-in does not grant matter access or approve an action. Local operator mode is unchanged.';
  const login = document.createElement('button');
  login.type = 'button'; login.textContent = 'Prepare provider sign-in';
  const logout = document.createElement('button');
  logout.type = 'button'; logout.textContent = 'Sign out of 8BALL'; logout.hidden = true;
  const external = document.createElement('a');
  external.textContent = 'Continue to configured identity provider';
  external.rel = 'noreferrer'; external.hidden = true;
  container.replaceChildren(title, status, note, login, external, logout);
  let disposed = false;
  const controller = new AbortController();
  async function request(path, method = 'GET') {
    const response = await fetch(`${apiBase}/identity/${path}`, {
      method, credentials: 'same-origin', cache: 'no-store', signal: controller.signal,
      ...(method === 'POST' ? {headers: {'Content-Type': 'application/json'}, body: '{}'} : {})
    });
    if (!response.ok) throw new Error('Agency sign-in is unavailable or expired. No access was granted.');
    return response.json();
  }
  async function refresh() {
    try {
      const result = await request('session');
      if (disposed) return;
      status.textContent = `Signed in as ${result.identity.subject} at ${result.identity.issuer}. Matter grants are checked for each operation.`;
      logout.hidden = false;
    } catch (error) {
      if (!disposed) status.textContent = error.message;
    }
  }
  login.addEventListener('click', async () => {
    login.disabled = true; external.hidden = true; external.removeAttribute('href');
    try {
      const result = await request('login', 'POST');
      if (disposed) return;
      const url = new URL(result.authorization_url);
      if (url.protocol !== 'https:' || url.username || url.password) throw new Error('Invalid provider configuration.');
      external.href = url.href; external.hidden = false;
      status.textContent = 'Continue only if you intend to sign in at this configured external provider. No matter access is implied.';
    } catch (error) {
      if (!disposed) status.textContent = error.message;
    } finally {
      if (!disposed) login.disabled = false;
    }
  });
  logout.addEventListener('click', async () => {
    logout.disabled = true;
    try {
      await request('logout', 'POST');
      if (disposed) return;
      logout.hidden = true; external.hidden = true; external.removeAttribute('href');
      status.textContent = 'Signed out of 8BALL. Your provider session may still be active.';
    } catch (error) {
      if (!disposed) status.textContent = error.message;
    } finally {
      if (!disposed) logout.disabled = false;
    }
  });
  refresh();
  return () => { disposed = true; controller.abort(); container.replaceChildren(); };
}
