import asyncio
from Crypto.Util.number import getPrime
from gmpy2 import powmod, invert
from hashlib import md5
from os import listdir
from ..exceptions import HandshakeError, UnameError, CodeTransmissionError


class DSA:
    def __init__(self, p, q, e):
        self.p = p
        self.q = q
        self.e = e
        self.n = p * q
        self.d = invert(e, (p - 1) * (q - 1))

    def sign(self, message):
        m = int.from_bytes(md5(message).digest(), "big")
        return powmod(m, self.d, self.n)


ExitException = KeyboardInterrupt


async def server_main(r, w):
    addr = writer.get_extra_info('peername')
    uname = md5(addr.encode('ascii')).hexdigest()
    code = (await reader.read(10000)).decode('utf-8')
    code_file = open(f'../tmp/{uname}.py', 'w')
    code_file.write(f'#{addr}\n')
    code_file.write(code)
    code_file.write('\n')
    if len(listdir('../tmp/')) > 1:
        raise ExitException


def server_start():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server_main, '0.0.0.0', 31488, loop=loop)
    server = loop.run_until_complete(coro)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except ExitException:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
