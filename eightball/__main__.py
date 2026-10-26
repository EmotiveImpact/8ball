"""Run with python -m eightball. Binds to loopback, never all interfaces."""
import os
import secrets
from pathlib import Path
import uvicorn
from .store import Store
from .api import make_app


def main():
    os.umask(0o077)
    db = os.getenv('EIGHTBALL_DB', str(Path.home() / '.eightball' / 'cases.sqlite3'))
    token = os.getenv('EIGHTBALL_TOKEN') or secrets.token_urlsafe(32)
    host = None
    if os.getenv('EIGHTBALL_AGENCY_CONFIG'):
        from .agency_host import load_host
        host = load_host(os.environ['EIGHTBALL_AGENCY_CONFIG'], db)
    app = make_app(Store(db), token, agency_host=host)
    print('\n8BALL V0.2 workspace: http://127.0.0.1:8048/v2/\nLegacy alpha: http://127.0.0.1:8048/\n')
    if host is None:
        print('Operator token (paste into the sign-in screen):\n' + token + '\n')
    else:
        print('Agency host enabled; local operator token is NOT accepted. Open /v2/agency.html.\n')
    print('Fictional/test data only. This is not a production agency service.\n')
    uvicorn.run(app, host='127.0.0.1', port=8048, access_log=False)


if __name__ == '__main__':
    main()
