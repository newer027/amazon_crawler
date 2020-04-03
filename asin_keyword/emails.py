from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string


def send_email(email, message,title):
    print("send email to the user")
    #if cookie_sele():
    c = Context({'email': email, 'message': message, 'title':title})

    email_subject = render_to_string(
        'feedback/email/feedback_email_subject.txt', c).replace('\n', '')
    email_body = render_to_string('feedback/email/feedback_email_body.txt', c)

    mail = EmailMessage(
        email_subject, email_body, settings.DEFAULT_FROM_EMAIL,[email])
    return mail.send(fail_silently=False)
