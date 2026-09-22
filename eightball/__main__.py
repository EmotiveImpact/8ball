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
    app = make_app(Store(db), token)
    print('\n8BALL local alpha: http://127.0.0.1:8048\n')
    print('Operator token (paste into the sign-in screen):\n' + token + '\n')
    print('Fictional/test data only. This is not a production agency service.\n')
    uvicorn.run(app, host='127.0.0.1', port=8048, access_log=False)


if __name__ == '__main__':
    main()
