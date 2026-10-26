"""Native loopback TLS agency journey; fictional seeded sessions and scanner.

No route interception, live IdP, provider call, malware-quality or human pass.
"""
from datetime import datetime, timedelta, timezone
import ipaddress
import json
import os
from pathlib import Path
import shutil
import socket
import sys
import tempfile
from threading import Thread
import time

import httpx
import uvicorn
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agency_fixture import make_fixture
from eightball.oidc.login import SESSION_COOKIE

OUT = Path(os.getenv('EIGHTBALL_ARTIFACTS', str(ROOT/'artifacts/agency')))
checks = []


def check(name, passed):
    assert passed, name
    checks.append(name)


def main():
    if os.getenv('EIGHTBALL_BROWSER_BRIDGE') == '1':
        raise RuntimeError('Agency suite requires native HTTP/TLS, not bridge')
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        tmp = Path(directory)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        origin = f'https://localhost:{port}'
        env = make_fixture(tmp, origin=origin)
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')])
        now = datetime.now(timezone.utc)
        cert = x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now-timedelta(minutes=1)).not_valid_after(now+timedelta(hours=1)).add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost'), x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]), critical=False).sign(key, hashes.SHA256())
        (tmp/'cert.pem').write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        (tmp/'key.pem').write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        server = uvicorn.Server(uvicorn.Config(env.app, host='127.0.0.1', port=port, access_log=False,
            log_level='error', ssl_keyfile=str(tmp/'key.pem'), ssl_certfile=str(tmp/'cert.pem')))
        thread = Thread(target=server.run, daemon=True)
        thread.start()
        try:
            for _ in range(150):
                if server.started:
                    break
                time.sleep(.02)
            assert server.started
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True, executable_path=os.getenv('EIGHTBALL_BROWSER') or shutil.which('chromium'), args=['--no-sandbox'])
                context = browser.new_context(ignore_https_errors=True, viewport={'width': 1440, 'height': 1000})
                context.add_cookies([{'name': SESSION_COOKIE, 'value': env.cookies['author'], 'url': origin, 'secure': True, 'httpOnly': True, 'sameSite': 'Lax'}])
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                try:
                    page.goto(origin+'/v2/agency.html')
                    expect(page.locator('#configuration')).to_contain_text('Explicit engineering host')
                    page.locator('#case-context [name=case_id]').fill(env.case.id)
                    page.locator('#case-context button').first.click()
                    expect(page.locator('#vault h2')).to_have_text('Evidence vault')
                    check('configured agency desk opens the current authorised case', page.locator('#case-panels').is_visible())
                    page.locator('#vault input[type=file]').set_input_files({'name':'fictional.txt','mimeType':'text/plain','buffer':b'Fictional original, not a verified observation.'})
                    page.locator('#vault input[type=datetime-local]').fill((now+timedelta(days=9)).strftime('%Y-%m-%dT%H:%M'))
                    page.get_by_role('button', name='Upload into quarantine').click()
                    expect(page.locator('#vault')).to_contain_text('quarantined')
                    check('native upload remains quarantined before explicit scan', not page.get_by_role('button', name='Download released original').count())
                    page.get_by_role('button', name='Request explicit scan').click()
                    expect(page.locator('#vault')).to_contain_text('released')
                    check('explicit fixture scan releases original without attesting a fact', page.get_by_role('button', name='Download released original').count() == 1)
                    with page.expect_download() as pending:
                        page.get_by_role('button', name='Download released original').click()
                    check('native authorised download preserves exact original bytes', Path(pending.value.path()).read_bytes() == b'Fictional original, not a verified observation.')
                    page.get_by_text('Versioned domain packs · read-only', exact=True).click()
                    page.locator('#packs').click()
                    expect(page.locator('#pack-results')).to_contain_text('fixer')
                    check('four pinned fictional packs inspectable without case mutation', all(value in page.locator('#pack-results').inner_text() for value in ('neutral','sales','support','fixer')))
                    page.locator('summary').filter(has_text='Reviewed reference library').click()
                    expect(page.locator('#knowledge')).to_contain_text('not a global negative')
                    check('empty accessible knowledge search does not assert global absence', True)
                    page.get_by_text('Scoped operations and fictional pilot findings', exact=True).click()
                    page.locator('#operations-open button').click()
                    expect(page.locator('#operations-results')).to_contain_text('incident')
                    check('scoped operation record opens through real host route', 'incident' in page.locator('#operations-results').inner_text())
                    page.screenshot(path=str(OUT/'8BALL-Agency-Desk.png'), full_page=True)
                    for width in (390, 768, 1440):
                        page.set_viewport_size({'width':width,'height':1000})
                        check(f'agency desk fits {width}px without horizontal overflow', page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                    from endstate.events import IncomingEvent
                    from eightball.agency_access import CurrentAuthority
                    from eightball.store import digest
                    with env.store.connection() as db:
                        source_id = db.execute('SELECT id FROM vault_originals').fetchone()[0]
                    authority = CurrentAuthority(env.registry, lambda: env.sessions.identity(env.cookies['author']))
                    with env.host.as_current(authority):
                        receipt = env.host.events.ingest(case_id=env.case.id, identity=env.identities['author'], event=IncomingEvent(
                            organisation_id=env.scope.organisation_id, matter_id=env.scope.matter_id,
                            source_id=source_id, source_version='1', event_id='native-controlled-worker',
                            kind='source_received', base_revision=env.case.revision,
                            text='Fictional original, not a verified observation.'))
                        review = env.host.events.review_source(case_id=env.case.id, identity=env.identities['author'],
                            sequence=receipt.sequence, expected_revision=env.case.revision,
                            receipt_sha256=digest(receipt.model_dump(mode='json')),
                            rationale='Explicit fictional fixture processing consent, not fact approval')
                        work = env.host.events.enqueue(case_id=env.case.id, identity=env.identities['author'],
                            sequence=receipt.sequence, expected_revision=env.case.revision, review_id=review['id'], request_id='native-review')
                        env.host.events.processor = lambda *_: 'Controlled unreviewed suggestion; not model inference.'
                        result = env.host.events.process(case_id=env.case.id, work_id=work, worker=env.identities['author'])
                        assert result['state'] == 'awaiting_review'
                    page.goto(origin+f'/v2/event-review.html?case={env.case.id}&work={work}&session=1')
                    page.get_by_role('button', name='Open current session review').click()
                    expect(page.get_by_label('Original source', exact=True)).to_contain_text('Fictional original')
                    expect(page.get_by_label('Original processing output', exact=True)).to_contain_text('not model inference')
                    check('current cookie session opens exact source and separately unreviewed worker result', True)
                    page.get_by_role('button', name='Lock review', exact=True).click()
                    check('locking session review clears original material and graph', page.get_by_label('Original source', exact=True).count() == 0)
                    page.goto(origin+'/v2/agency.html')
                    page.locator('#case-context [name=case_id]').fill(env.case.id)
                    page.locator('#case-context button').first.click()
                    expect(page.locator('#vault h2')).to_have_text('Evidence vault')
                    page.get_by_text('Scoped operations and fictional pilot findings', exact=True).click()
                    env.registry.revoke('author')
                    with page.expect_response(lambda response: response.url.endswith('/operations')) as response:
                        page.locator('#operations-refresh').click()
                    check('revoked principal denied by operations host', response.value.status == 403)
                    expect(page.locator('#case-panels')).to_be_hidden()
                    check('durable grant revocation clears cached private panels', not page.locator('#vault').inner_text().strip())
                    page.locator('#case-context [name=case_id]').fill(env.other.id)
                    page.locator('#case-context button').first.click()
                    expect(page.locator('#context-status')).to_contain_text('Access unavailable')
                    check('cross-tenant exact case cannot populate private panels', not page.locator('#case-panels').is_visible())
                    check('no browser module runtime errors', not errors)
                    report = dict(checks_passed=len(checks), checks=checks, network='Native loopback HTTPS/TLS',
                        errors=errors, model_inference_tested=False, independent_review_performed=False,
                        human_accessibility_tested=False, limits=['Fictional seeded durable sessions, not real OIDC provider acceptance.',
                        'Controlled scanner result is not malware-quality acceptance.',
                        'Controlled worker suggestion is not model inference.', 'No paid inference, real-client pilot or external sends.'])
                    (OUT/'browser-agency-report.json').write_text(json.dumps(report, indent=2)+'\n')
                    print(json.dumps(report, indent=2))
                except Exception:
                    page.screenshot(path=str(OUT/'failure.png'), full_page=True)
                    (OUT/'failure.html').write_text(page.content())
                    raise
                finally:
                    browser.close()
        finally:
            server.should_exit = True
            thread.join(timeout=5)


if __name__ == '__main__':
    main()
