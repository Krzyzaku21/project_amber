from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model


class Util:

    @staticmethod
    def send_mail(to_email: str, context: dict) -> EmailMessage:
        """
        Sending email token and rendering html response
        """
        html_template = strip_tags(render_to_string('accounts/register_email_send.html', {
            'token': context['token'],
            'domain': context['domain'],
        }))
        email = EmailMessage(
            subject='This is register email',
            body=html_template,
            to=[to_email],
        )
        email.send()

    @staticmethod
    def remove_user_time():
        """
        If user longer than 5min with flag is_verified == False, he was automatically deleted
        """
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            ten_minutes_later = (user.date_joined + timedelta(hours=0.05))
            if ten_minutes_later < timezone.now():
                if user.is_verified == False:
                    user.delete()
