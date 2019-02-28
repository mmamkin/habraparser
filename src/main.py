import asyncio
from aiohttp import web, client
from modules.parser import MyHTMLParser

DEST_HOST = 'habr.com'
LOCAL_HOST = 'localhost'
LOCAL_PORT = 8080


async def handler(request):
    headers = dict(request.headers)
    headers['Host'] = DEST_HOST
    if 'Referer' in headers:
        headers['Referer'] = headers['Referer'].replace(
            'http://{}:{}'.format(LOCAL_HOST, LOCAL_PORT),
            'https://{}'.format(DEST_HOST))
    try:
        dest_url = 'https://{host}{path}'.format(host=DEST_HOST, path=request.rel_url)
        print('{} {}'.format(request.method, dest_url))
        body = None
        if request.can_read_body:
            body = await request.content.read()

        async with client.request(
                request.method, dest_url,
                headers=headers,
                data=body
        ) as r:
            r_headers = dict(r.headers)
            # т.к. результат автоматически распакован из gzip, то заголовки подчищаем
            if 'Content-Encoding' in r_headers:
                del r_headers['Content-Encoding']
            if 'Transfer-Encoding' in r_headers:
                del r_headers['Transfer-Encoding']

            response = web.StreamResponse(status=r.status, headers=r_headers)
            await response.prepare(request)

            # парсинг нужен только для html
            if not r_headers.get('Content-Type', '').startswith('text/html'):
                data = await r.content.read()
                await response.write(data)
                await response.write_eof()
                return response

            data = await r.content.read()
            if data:
                # список пар ссылок для замены ((old_href, new_href), ...)
                hrefs = (('https://{}/'.format(DEST_HOST), 'http://{}:{}/'.format(LOCAL_HOST, LOCAL_PORT)),)
                parser = MyHTMLParser(convert_charrefs=False, hrefs=hrefs)
                parser.feed(data.decode('utf8'))
                await response.write(parser.get_result().encode('utf8'))
            await response.write_eof()
            return response
    except Exception as e:
        print(e)
        return None


async def main():
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, LOCAL_HOST, LOCAL_PORT)
    await site.start()
    print("======= Serving on http://{}:{}/ ======".format(LOCAL_HOST, LOCAL_PORT))
    await asyncio.sleep(100 * 3600)


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    pass
loop.close()
