import asyncio
import logging

from .transport import Transport
from .message import Message

LOGGER = 'api'


class Messenger:
    """A helper class to send multiple messages at the same time"""

    def __init__(self, *args):
        self.transports = {}
        for transport in args:
            if isinstance(transport, Transport):
                # verify if it's a valid transport.
                self.transports[transport.__class__.__name__.lower()] = transport
            else:
                logging.getLogger(LOGGER).error(
                    'The class %s is not a valid transport',
                    transport.__class__.__name__
                )


    def get_transport(self, message: Message):
        """Look for a transport to deliver the message within the current messenger"""
        for transport_name in message.transports():
            if transport_name.lower() in self.transports:
                return self.transports[transport_name.lower()]

        return None

    async def deliver(self, *args):
        """Send all the given messages looking for the apropiate transport"""
        coros = []
        for message in args:
            # raise if not a valid message class
            transport = self.get_transport(message)
            if not transport:
                msg = 'There is no transport for message %s' % message.__class__.__name__
                logging.getLogger(LOGGER).error(msg)
                raise Exception(msg)

            coros.append(transport.send(message))

        return tuple(await asyncio.gather(*coros))
