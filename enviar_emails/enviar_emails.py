import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

import pandas as pd

MY_ADDRESS = 'ACA VA EL SU CORREO ELECTRONICO EN MINUSCULA Y TODO JUNTO. RESPETAR LAS COMILLAS'
PASSWORD = 'CONTRASEÑA ENTRE LAS COMILLAS'


def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    df = pd.read_csv(filename)

    names = list(df['NOMBRE'])
    emails = list(df['EMAIL'])

    return names, emails


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return template_file_content#Template(template_file_content) #template_file_content in case name is not included


def main():
    file_ = 'EMAILS'
    msg_file = 'msg'
    names, emails = get_contacts(file_+'.csv')  # read contacts
    message_template = read_template(msg_file+'.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='mail.aswell.com.ar', port=25)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    errors = 0
    # For each contact, send the email:
    for name, email in zip(names, emails):
        print('Sending msg...')
        msg = MIMEMultipart()  # create a message

        # add in the actual person name to the message template
        message = message_template#.substitute(NAME=name.title()) #not necessary unless you have place holders in the msg
        # setup the parameters of the message
        msg['From'] = formataddr((str(Header('Juan Estevez A.', 'utf-8')), MY_ADDRESS))
        msg['To'] = email
        msg['Subject'] = 'ENTRE LAS COMILLAS VA EL ASUNTO '

        # add in the message body
        # 'html' instead of plain
        msg.attach(MIMEText(message, 'html'))

        try:
            # send the message via the server set up earlier.
            s.send_message(msg)
            print('Message sent to ', name, email, sep='\t')
        except:
            print('ERROR!!! Message NOT sent to ', name, email, sep='\t')
            errors =+ 1
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()
    print('All messages were sent successfully.')
    print(errors,' errors occurred!')

if __name__ == '__main__':
    main()