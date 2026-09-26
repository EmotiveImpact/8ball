"""Bounded ASGI body replay. Do not trust Content-Length as the size check."""
import re
from starlette.responses import JSONResponse
from .source_contracts import SOURCE_BODY_LIMIT


def body_limit(path: str) -> int:
    return SOURCE_BODY_LIMIT if re.fullmatch(r'/api/v2/cases/[a-zA-Z0-9_-]+/sources/(preview|import)',path) else 300_000


class BoundedRequestBody:
    def __init__(self,app):
        self.app=app

    async def __call__(self,scope,receive,send):
        if scope['type']!='http' or scope.get('method') not in ('POST','PUT','PATCH'):
            return await self.app(scope,receive,send)
        cap=body_limit(scope.get('path',''))
        headers=dict(scope.get('headers',[]))
        try:declared=int(headers.get(b'content-length',b'-1'))
        except ValueError:declared=-1
        if declared<0 or declared>cap:
            return await JSONResponse({'detail':f'Request needs Content-Length of at most {cap} bytes'},413,headers={'Cache-Control':'no-store'})(scope,receive,send)
        body=bytearray()
        while True:
            message=await receive()
            if message['type']=='http.disconnect':return
            if message['type']!='http.request':continue
            chunk=message.get('body',b'')
            if len(body)+len(chunk)>cap:
                return await JSONResponse({'detail':'Request body exceeds its route limit'},413,headers={'Cache-Control':'no-store'})(scope,receive,send)
            body.extend(chunk)
            if not message.get('more_body',False):break
        if len(body)!=declared:
            return await JSONResponse({'detail':'Request body length does not match Content-Length'},413,headers={'Cache-Control':'no-store'})(scope,receive,send)
        delivered=False
        async def replay():
            nonlocal delivered
            if not delivered:
                delivered=True
                return {'type':'http.request','body':bytes(body),'more_body':False}
            return await receive()
        await self.app(scope,replay,send)
