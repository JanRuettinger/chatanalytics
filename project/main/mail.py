import imaplib
import email
from email.header import decode_header, make_header
import os
import zipfile
import time
import sys
from flask import current_app, render_template
from ..models import Analysis
from threading import Thread
from flask_mail import Message
from ..factory import mail


# Connect to an IMAP server
def connect(server, user, password):
    m = imaplib.IMAP4_SSL(server)
    try:
        m.login(user, password)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    m.select('INBOX')
    return m


# Download all attachment files for a given email
def downloaAttachmentsInEmail(m, emailid, outputdir):
    resp, data = m.fetch(emailid, '(RFC822)')
    email_body = data[0][1]
    mail = email.message_from_bytes(email_body)

    # Extract sender name and sender email address from the email
    sender = str(make_header(decode_header(mail['From'])))

    try:
        name, email_addr = sender.split('<')
        email_addr = email_addr.replace(">", "")
    except:
        print("Sender ohne Name")
        email_addr = sender
        name = " "

    if mail.get_content_maintype() != 'multipart':
        return -1

    # Each email address gets its own folder
    new_folder_name = "".join(email_addr.split("@")[0].split("."))

    outputdir = outputdir + new_folder_name + "/"
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)


    for part in mail.walk():
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            old_filename = part.get_filename()
            # Check if attachement contains "whatsapp chat"
            #if "whatsapp chat" not in old_filename.lower():
            #    return -1
            # Write file/attachment to disk
            if part.get_filename() is not None:
                sv_path = os.path.join(outputdir, old_filename)
                if not os.path.isfile(sv_path):
                    fp = open(sv_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

            # iOS: File is zipped; Android: File is a unzipped
            if ".txt" in old_filename:
                # File is from Android client
                # New Filename: DD_MM_YY_OLDFILENAME.txt
                new_filename = str((time.strftime("%d_%m_%Y"))) + "_" + \
                               old_filename
                os.rename(outputdir + old_filename, outputdir + new_filename)

            else:
                # File is from iOS client
                # New Filename: DD_MM_YY_OLDFILENAME.txt
                try:
                    new_filename = old_filename[:-3] + "txt"
                    unzip(outputdir + old_filename, outputdir)
                    os.rename(outputdir + '_chat.txt', outputdir + new_filename)
                    os.remove(outputdir + old_filename)  # remove zip file

                except:
                    return -1

            return (new_folder_name, name, email_addr, outputdir + new_filename)


# Download all the attachment files for all emails in the inbox.
def downloadAllAttachmentsInInbox(server, user, password, outputdir):
    list_new_mails = []
    m = connect(server, user, password)
    # resp, mails = m.search(None, "(UNSEEN)", '(SUBJECT "%s")' % ("Test"))
    resp, mails = m.search(None, "UNSEEN")
    mails = mails[0].split()
    print("Number of new emails: " + str(len(mails)))
    for emailid in mails:
        new_attachement = downloaAttachmentsInEmail(m, emailid, outputdir)
        if new_attachement != -1:
            list_new_mails.append(new_attachement)
        m.store(emailid, '+FLAGS', '\Seen') # Mark email as seen
    return list_new_mails


def check_new_mail():
    server = current_app.config['IMAP_SERVER']
    user = current_app.config['MAIL_USERNAME']
    password = current_app.config['MAIL_PASSWORD']

    m = connect(server, user, password)

    resp, mails = m.search(None, "UNSEEN")
    mails = mails[0].split()
    return len(mails)


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)


def get_new_chats():
    IMAP_SERVER = current_app.config['IMAP_SERVER']
    FROM_EMAIL = current_app.config['MAIL_USERNAME']
    FROM_PWD = current_app.config['MAIL_PASSWORD']
    OUTPUTDIR = current_app.config['OUTPUTDIR']

    return downloadAllAttachmentsInInbox(IMAP_SERVER, FROM_EMAIL,
                                         FROM_PWD, OUTPUTDIR)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, name, link_hash):
    app = current_app._get_current_object()
    result_url = app.config['RESULT_URL']
    link = str(result_url) + str(link_hash)
    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    #msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', name=name, link=link)
    mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
