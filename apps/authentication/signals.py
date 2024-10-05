# signals.py

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()

def send_welcome_email(username, email):
    subject = "Welcome to DevHubs"
    
    # Render the email template
    html_message = render_to_string('emails/welcome_email.html', {'username': username})

    send_mail(
        subject=subject,
        message="",  # No plain text message since we are using HTML
        from_email="no-reply@devhubs.com",
        recipient_list=[email],
        html_message=html_message,
    )

@receiver(post_save, sender=User)
def send_welcome_email_on_user_creation(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance.username, instance.email)
