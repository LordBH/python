from sendEmail import DispatchEmail, MessageWithAttachment
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import unittest
import mock


class TestDispatchEmail(unittest.TestCase):
    def test_auth(self):
        dsptch_eml = DispatchEmail('', '')
        dsptch_eml.server = mock.MagicMock()

        username = 'username'
        password = 'password'
        dsptch_eml.auth(username, password)

        dsptch_eml.server.login.assert_called_once_with(username, password)

    def test_create_smtp_server(self):
        email = DispatchEmail('', '', smtp='smtp.softserveinc.com')
        email.create_smtp_server()
        self.assertIsInstance(email.server, SMTP)

    def test_send_email(self):
        dsptch_eml = DispatchEmail('sender', 'receiver')
        dsptch_eml.server = mock.MagicMock()

        attch = MessageWithAttachment()
        dsptch_eml.send_email(attch)

        sender = 'sender'
        receiver = 'receiver'
        eml = attch.create_eml(sender=sender, receiver=receiver, cc=[])

        dsptch_eml.server.sendmail.assert_called_once_with(
            sender, receiver, eml
        )

    def test_set_sender_and_receiver(self):
        eml = MIMEMultipart()
        eml['from'] = 'from@mail.com'
        eml['to'] = 'to@mail.com'
        eml_string = eml.as_string()

        email = DispatchEmail('', '')
        email.set_sender_and_receiver(eml_str=eml_string)

        self.assertEqual(eml['from'], email.sender)
        self.assertEqual(eml['to'], email.recepient)


class TestMessageWithAttachment(unittest.TestCase):
    def test_add_files(self):
        pass

    def test_create_eml(self):
        pass

    def test_set_addresses(self):
        eml = MessageWithAttachment()
        eml.create_mime_message()

        sender = 'test@www.com'
        receiver = 'receiver@qqq.com'
        cc = ['cc@qq.qq']

        eml._set_addresses(sender=sender, receiver=receiver, cc=cc)

        self.assertNotEqual(sender, eml.message['From'])
        self.assertNotEqual(receiver, eml.message['To'])
        self.assertNotEqual(cc, eml.message['CC'])

    def test_set_body(self):
        eml = MessageWithAttachment()
        eml.create_mime_message()

        body = 'Test'
        charset = 'utf-8'
        eml.set_body(body=body, charset=charset)

        self.assertEquals(body, eml.message.get_payload(decode=charset))

if __name__ == '__main__':
    unittest.main()
