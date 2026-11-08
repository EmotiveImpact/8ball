"""Register on a separate same-origin router; login cannot depend on agency auth."""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse

from eightball.oidc.login import ATTEMPT_COOKIE, LoginDenied, SESSION_COOKIE


def register_identity_routes(router: APIRouter, service):
    def same_origin(request):
        if request.headers.get('origin') != service.config.origin:
            raise HTTPException(403, 'Same-origin identity request required')

    def protect(response):
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

    def cookie(response, name, value, age):
        response.set_cookie(name, value, max_age=age, secure=True, httponly=True,
                            samesite='lax', path='/')

    @router.post('/identity/login')
    def login(request: Request):
        same_origin(request)
        service.cancel(request.cookies.get(ATTEMPT_COOKIE, ''))
        url, browser = service.begin()
        response = protect(JSONResponse({'authorization_url': url, 'external_login_required': True}))
        cookie(response, ATTEMPT_COOKIE, browser, 300)
        return response

    @router.get('/identity/callback')
    def callback(request: Request):
        params = request.query_params
        response = protect(JSONResponse({'detail': 'Login failed; start a new login'}, status_code=401))
        browser = request.cookies.get(ATTEMPT_COOKIE, '')
        try:
            if (set(params) != {'state', 'code', 'iss'}
                    or any(len(params.getlist(key)) != 1 for key in params)):
                service.cancel(browser)
                raise LoginDenied('Invalid response')
            session = service.complete(state=params['state'], browser=browser,
                                       code=params['code'], issuer=params['iss'])
            old = request.cookies.get(SESSION_COOKIE, '')
            service.logout(old)
            response = protect(RedirectResponse('/v2/', status_code=303))
            cookie(response, SESSION_COOKIE, session, service.config.session_seconds)
        except LoginDenied:
            pass
        response.delete_cookie(ATTEMPT_COOKIE, secure=True, httponly=True, samesite='lax', path='/')
        return response

    @router.get('/identity/session')
    def session(request: Request):
        try:
            identity = service.identity(request.cookies.get(SESSION_COOKIE, ''))
        except LoginDenied:
            raise HTTPException(401, 'A current agency session is required') from None
        return protect(JSONResponse({'identity': identity.model_dump(),
                                     'matter_access': 'requires_current_grants',
                                     'action_approved': False}))

    @router.post('/identity/logout')
    def logout(request: Request):
        same_origin(request)
        service.cancel(request.cookies.get(ATTEMPT_COOKIE, ''))
        service.logout(request.cookies.get(SESSION_COOKIE, ''))
        response = protect(JSONResponse({'logged_out': True, 'provider_session_ended': False}))
        for name in (SESSION_COOKIE, ATTEMPT_COOKIE):
            response.delete_cookie(name, secure=True, httponly=True, samesite='lax', path='/')
        return response
