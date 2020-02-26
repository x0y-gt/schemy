import asyncio
import logging
from abc import ABC, abstractmethod
from .message import Message

LOGGER = 'api'


class Transport(ABC):
    """Abstract class for channels to deliver notifications"""


    @classmethod
    def get_payload(cls, message: Message):
        """Return a tuple with the payload of the message and the
        delivery instructions"""
        payload = message.payload()
        instructions = message.delivery_instructions()
        if not payload:
            msg = 'Payload of message %s is empty' % message.__class__.__name__
            logging.getLogger(LOGGER).error(msg)
            raise Exception(msg)

        return payload, instructions


    @abstractmethod
    async def send(self, message: Message):
        """Method used to send a message using the current transport"""
