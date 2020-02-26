import json

from ..message import Message

class MailGunEmail(Message):
    """Message to send emails using mailgun API"""

    def __init__(self, sender, to, subject):
        self._payload = {
            'from': sender,
            'to': [to],
            'subject': subject,
            'text': None,
            'html': None,
            'template': None,
        }

    def sender(self, sender):
        self._payload['from'] = sender

    def to(self, to: str):
        self._payload['to'].append(to)

    def subject(self, subject: str):
        self._payload['subject'] = subject

    def text(self, text: str):
        self._payload['text'] = text

    def html(self, html: str):
        self._payload['html'] = html

    def template(self, template: str, variables):
        """Method to specify the template and variables"""
        self._payload['template'] = template
        self._payload['h:X-Mailgun-Variables'] = json.dumps(variables)

    def transports(self):
        return ['MailgunTransport', 'HttpTransport']

    def delivery_instructions(self):
        # Specify the path of the mailgun api to send messages
        return {'path': '/messages'}

    def payload(self):
        return {k:v for k, v in self._payload.items() if v}
