import asyncio
from exceptions import HandshakeError

async def server_main(r, w):
    w.write(b'zdarova\n')
    await writer.drain()
    hello_answer = await reader.read(100)
    if hello_answer != b'zdarova\n':
        raise HandshakeError
    try:
        w.write(b'uname\n')
        await writer.drain()
        uname = (await reader.read(100)).decode()[:-1]
    except:
        raise UnameError

    try:
        w.write(b'code\n')
        await writer.drain()
        code = (await reader.read(10000)).decode()[:-1]
    except:
        raise CodeTransmissionError

def server_start():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server_main, '0.0.0.0', 31488, loop=loop)
    server = loop.run_until_complete(coro)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    while 1:
        loop.run_forever()
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
