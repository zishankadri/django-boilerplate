import uuid
from django.core.mail import send_mail
from django.conf import settings

def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:12]
    return code

# Wrapper for sending emails
def send_email(email, subject, message):
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list, fail_silently = False)
