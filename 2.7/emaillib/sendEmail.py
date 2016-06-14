from argparse import ArgumentParser
from getpass import getpass
from email import encoders, message_from_string
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import getaddresses
from mimetypes import guess_type
from smtplib import SMTP
from sys import stdin
import os

__all__ = ['DispatchEmail', 'MessageWithAttachment']
ABOUT = """
        This application you can use in three ways. First
        way (send message via smtp server). U have to
        indicate smtp server, yours email and receiver
        email. It is required. For more options (body,
        subject, etc.) check --help.
        Second way (printing to standard output). To follow
        this way u need to point key -e and both email:
        yours and receiver. Also to create file with output,
        just specify file with $ python send.py -e
        > my_email.eml
        Last way (sending message from
        standard input). Very simple step. Just point
        smtp server, it is required, other for yours wish.
        Example : $ cat my_email.eml | py send.py /options/
        :: If u will need some more options,
        find them in --help. Good Luck !
        """


def create_iteration(*args):
    """Function create iteration list. It added str or list to iteration"""
    cache = []
    for arg in args:
        if isinstance(arg, list):
            cache += arg
        elif isinstance(arg, (tuple, dict, set)):
            raise ValueError('Not provided this type %r' % (type(arg),))
        else:
            cache.append(arg)
    return cache


def get_args_parser(send_eml=True):
    """Function for parsing command from bash."""
    pars = ArgumentParser(description=ABOUT)
    if send_eml:
        pars.add_argument('--from', nargs=1, required=True,
                          help='yours email send', dest='sender')
        pars.add_argument('-r', '--receivers', nargs=1, required=True,
                          help='receiver')
        pars.add_argument('-s', '--smtp', nargs=1, help='smtp server',
                          default=[None])

    else:
        pars.add_argument('--from', nargs=1, help='yours email send',
                          dest='sender', default=[None])
        pars.add_argument('-r', '--receivers', nargs=1, help='receiver',
                          default=[None])
        pars.add_argument('-s', '--smtp', required=True, nargs=1,
                          help='smtp server')
    pars.add_argument('-c', '--cc', nargs='+', help='copies will send TO',
                      default=[])
    pars.add_argument('--subject', nargs='?', help='subject of message',
                      default='')
    pars.add_argument('-b', '--body', nargs='?', help='body of email',
                      default='')
    pars.add_argument('-p', '--port', nargs='?', type=int,
                      help='port of smpt server', default=25)
    pars.add_argument('-t', '--use-tls', nargs='?', type=bool,
                      help='user TLS protocol', const=True,
                      default=False, dest='tls')
    pars.add_argument('-f', '--files', nargs='+', help='files for sending',
                      default=[])
    pars.add_argument('-u', '--username', nargs='?',
                      help='username on smtp server')
    pars.add_argument('-e', '--create-eml', nargs='?', type=bool,
                      help='create EML file', const=True)
    pars.add_argument('-a', '--auth', nargs='?', type=bool,
                      help='on authentication', const=True)
    pars.add_argument('--charset', nargs='?', type=str,
                      help='charset of encoding eml file', default='us-ascii')
    # pars.add_argument('-h', '--help', action='help', help=ABOUT)
    return pars.parse_args()


def set_email_arguments(args):
    global FROM, TO, CC, SMTP_SERVER, PORT, USERNAME, \
        TLS, EML_CREATE, SUBJECT, BODY, FILES, CHARSET, AUTH

    FROM = args.sender[0]
    TO = args.receivers[0]
    CC = args.cc

    SMTP_SERVER = args.smtp[0]
    PORT = args.port
    TLS = args.tls
    USERNAME = args.username
    EML_CREATE = args.create_eml
    AUTH = args.auth

    SUBJECT = args.subject
    BODY = args.body
    FILES = args.files
    CHARSET = args.charset


class DispatchEmail(object):
    """Class for configuration connection between MUA and MTA or MSA
    Provide method for send email and method for get sender and receiver
    from EML file.
    """

    def __init__(self,
                 sender,
                 receivers,
                 cc=None,
                 smtp=None,
                 port=25,
                 tls=False):
        """
        This constructor create configurations for server which
        will connect to MTA or MSA.
        """
        self.sender = sender
        self.receivers = receivers
        self.smtp = smtp
        self.cc = [] if cc is None else cc
        self.tls = tls
        self.port = port
        self.server = None
        self.message = None

    def auth(self, username, password=''):
        """Login user to server. Takes username and password
         for authentication.
        """
        if username is None:
            username = self.sender
        elif not username:
            raise AttributeError('Not set username')
        if not password:
            password = getpass('Password: ')

        self.server.login(username, password)

    def get_addressees(self, sender, receiver):
        if sender is None:
            sender = self.sender
        if receiver is None:
            if isinstance(self.receivers, str):
                receiver = self.receivers
            else:
                raise ValueError('Receiver must be str')
        return sender, receiver

    def create_smtp_server(self):
        """Connect to SMTP server, take value smtp, port and tls
        from attributes of instance.
        """
        assert isinstance(self.smtp, str), \
            TypeError('SMTP server has incorrect type, not str')
        assert self.smtp, \
            AttributeError('SMTP server is empty')
        if self.server is None:
            self.server = SMTP(self.smtp, self.port)
        if self.tls:
            self.server.starttls()

    def send_email(self, message):
        if isinstance(self.receivers, list):
            raise ValueError('Receiver not type str')
        self.cc.append(self.receivers)
        for receiver in self.cc:
            message.set_addresses(self.sender, receiver, self.cc)
            message = message.add_attachments()
            self.send(self.sender, receiver, message)

    def send(self, sender, receiver, message):
        """Method for send email via smtp server."""
        if not message:
            raise AttributeError('EML string was not given')
        if self.server is None:
            raise AttributeError('SMTP server not created')
        self.server.sendmail(sender, receiver, message)

    def set_sender_and_receiver(self, mbox):
        """
        Set sender and receiver to instance of DispatchEmail from EML file.
        """
        mperser = message_from_string(mbox)
        for header in ['from', 'to']:
            # Getting value/addresses from MIME header
            header_value = mperser.get_all(header, [])
            addresses = getaddresses(header_value)
            for real_name, em in addresses:
                if header == 'from':
                    self.sender = em
                if header == 'to':
                    self.receivers = em


class MessageWithAttachment(object):
    """Class provide opportunity to create multipart or plain type of message,
     set it and add files"""

    def __init__(self,
                 subject='',
                 body='',
                 files=None,
                 charset='us-ascii',
                 multipart=False,
                 create_mime=True):
        """Creates a multipart or plain type message.

        By default, creates a text/plain message, with proper
        Content-Type and MIME-Version headers.

        subject, body is the subject and body of the message

        files is the files of multipart message string. By default if None,
        class will create plain/text type of message, another way multipart.

        charset is the charset of body.

        multipart is flag for create multipart of plain type of message.

        message is instance of MIMEMultipart or MIMEText class
        """
        self.subject = subject
        self.files = files
        self.body = body
        self.charset = charset
        self.message = None
        if files:
            multipart = True
        self.multipart = multipart
        if create_mime:
            self.create_mime_message()

    def add_files(self, outer):
        """Function heck type of file and add files for outer."""
        for filename in self.files:
            path = os.path.abspath(filename)
            if not os.path.isfile(path):
                continue
            ctype, encoding = guess_type(path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(path)
                mmsg = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(path, 'rb')
                mmsg = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(path, 'rb')
                mmsg = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(path, 'rb')
                mmsg = MIMEBase(maintype, subtype)
                mmsg.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(mmsg)
            mmsg.add_header('Content-Disposition', 'attachment',
                            filename=filename)
            outer.attach(mmsg)

    def create_special_addresses(self, *args, **kwargs):
        """Function, which create special

        if group is True, message will contain only with receivers. Otherwise,
        contain for every receiver his alone addresses.
        """
        people = create_iteration(*args)
        sender, people = people[0], people[1:]
        if kwargs.get('group'):
            people = [people]
        for preceiver in people:
            self.set_addresses(sender=sender,
                               receiver=preceiver,
                               delete_cache=True)
            yield preceiver, self.add_attachments()

    def create_mime_message(self):
        """
        Create MIMEMultipart or MIMEText depending on the flag of multipart
        """
        if self.multipart:
            self.message = MIMEMultipart()
        else:
            self.message = MIMEText(_text='')

    def add_attachments(self):
        """Function which combine all functions for creating message"""
        if not self.message:
            raise AttributeError(
                "MIME type didn't match, run instance.create_mime_message()"
            )
        if self.body:
            assert isinstance(self.body, str)
            self.set_body()
        if self.files:
            assert isinstance(self.files, list)
            self.add_files(self.message)
        if self.subject:
            assert isinstance(self.body, str)
            self.message['Subject'] = self.subject
        return self.message.as_string()

    def set_addresses(self, sender, receiver, cc=None, delete_cache=False):
        """Function set addresses to message"""
        if not self.message:
            raise AttributeError(
                "MIME type didn't match, run instance.create_mime_message()"
            )
        if delete_cache:
            del self.message['From']
            del self.message['To']
        self.message['From'] = '<' + sender + '>'
        if isinstance(receiver, list):
            recs = ''.join(['<' + addr + '>, ' for addr in receiver])
        else:
            recs = '<' + receiver + '>'
        self.message['To'] = recs
        if cc is not None:
            ccaddrs = ['<' + copy + '>, ' for copy in cc if receiver != copy]
            self.message['CC'] = ''.join(ccaddrs)

    def set_body(self, body=None, charset=None):
        """Set body to message with charset"""
        if not self.message:
            raise AttributeError(
                "MIME type didn't match, run instance.create_mime_message()"
            )
        if body is None:
            body = self.body
        if charset is None:
            charset = self.charset
        self.message.set_payload(body, charset)


if __name__ == '__main__':
    # Sender, receiver and copies
    FROM = ''
    TO = ''
    CC = []

    # Connection settings
    SMTP_SERVER = ''
    PORT = 25
    TLS = True
    USERNAME = None
    PASSWORD = ''
    EML_CREATE = False
    AUTH = True

    # Message view
    SUBJECT = ''
    BODY = ''
    FILES = []
    CHARSET = 'utf-8'

    # Use special send with personal or only receivers addresses
    SEND_WITH_CC = True

    # Other conf
    TTY = stdin.isatty()

    """Check for whom parameter use: from here or key from terminal"""
    if not (FROM and TO and SMTP_SERVER and TTY):
        arguments = get_args_parser(TTY)
        set_email_arguments(arguments)

    email = DispatchEmail(sender=FROM, receivers=TO, cc=CC,
                          smtp=SMTP_SERVER, port=PORT, tls=TLS)

    if TTY:
        """If stdin was used for send email via API, else without it"""
        eml = MessageWithAttachment(subject=SUBJECT, body=BODY, files=FILES,
                                    charset=CHARSET)

        if EML_CREATE:
            """For creating EML or MBOX file without send."""
            eml.set_addresses(FROM, TO, CC)
            print eml.add_attachments()
        else:
            """Send email with custom headers"""
            email.create_smtp_server()

            if AUTH:
                email.auth(USERNAME, PASSWORD)

            if SEND_WITH_CC:
                email.send_email(eml)
            else:
                letters = eml.create_special_addresses(email.sender,
                                                       email.receivers,
                                                       email.cc,
                                                       group=True)
                for deliver, letter in letters:
                    email.send(sender=email.sender,
                               receiver=deliver,
                               message=letter)
    else:
        """Send email, taking message from standard input."""
        msg = stdin.read()
        email.create_smtp_server()
        email.set_sender_and_receiver(msg)
        if AUTH:
            email.auth(USERNAME)
        email.send(email.sender, email.receivers, msg)
