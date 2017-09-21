import pytest
import project.main.mail as mail


def test_mail_server_connection(app):

    server = app.config['IMAP_SERVER']
    user = app.config['MAIL_USERNAME']
    pwd = app.config['MAIL_PASSWORD']

    try:
        mail.connect(server, user, pwd)
    except:
        pytest.fail("Mail connection failed")


def test_mail_read(app):
    server = app.config['IMAP_SERVER']
    user = app.config['MAIL_USERNAME']
    pwd = app.config['MAIL_PASSWORD']

    m = mail.connect(server, user, pwd)
    resp, mails = m.search(None, "SEEN")
    mails = mails[0].split()
    assert len(mails) > 0
