from django.core.mail import send_mail

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
def send_verification_mail(user, current_site):
    subject="Aktywuj swoje konto w serwisie MaceWindu"
    message = render_to_string('email_templates/account_activation_email.html', {
        'username': user.username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject,message,'example@gmail.com',[user.email])