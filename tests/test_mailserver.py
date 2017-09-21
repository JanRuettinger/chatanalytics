import pytest
import project.main.mail as mail
from flask import current_app


def test_mail_server_connection(testapp):

    server = current_app.config['IMAP_SERVER']
    user = current_app.config['MAIL_USERNAME']
    pwd = current_app.config['MAIL_PASSWORD']

    try:
        mail.connect(server, user, pwd)
    except:
        pytest.fail("Mail connection failed")


def test_mail_read(testapp):
    server = current_app.config['IMAP_SERVER']
    user = current_app.config['MAIL_USERNAME']
    pwd = current_app.config['MAIL_PASSWORD']

    m = mail.connect(server, user, pwd)
    resp, mails = m.search(None, "SEEN")
    mails = mails[0].split()
    assert len(mails) > 0
