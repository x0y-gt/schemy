from abc import ABC, abstractmethod

class Message(ABC):
    """Abstract class representing a message, all the messages using transports
    must inherit from this class"""

    @abstractmethod
    def transports(self):
        """Must return a list of the names of the transports allowed to send
        the message"""

    def delivery_instructions(self):
        """This is an optional method to override, it can be used to return
        extra information to the transport to be able to send the message"""
        return {}

    @abstractmethod
    def payload(self):
        """Used to return a dict based response that represents the message data"""
