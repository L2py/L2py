import logging

from common.request import Request
from common.response import Response

LOG = logging.getLogger(f"l2py.{__name__}")


class PacketTransport:
    def __init__(self, transport, session, middleware):
        self._transport = transport
        self.session = session
        self.middleware = middleware

    @property
    def peer(self):
        return self._transport.get_extra_info("peername")

    def read(self, data):
        request = Request(data, self.session)
        for middleware in self.middleware:
            middleware.before(self.session, request)
        return request

    def write(self, response: Response):
        for middleware in self.middleware[::-1]:
            middleware.after(self.session, response)
        LOG.debug(f"SENDING: %s", response.packet)
        return self._transport.write(bytes(response.data))

    def close(self):
        return self._transport.close()
