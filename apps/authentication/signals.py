import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()
logger = logging.getLogger(__name__)

EMAIL_SUBJECT = "Welcome to DevHubs"
FROM_EMAIL = "no-reply@devhubs.com"
TEMPLATE_PATH = 'emails/welcome_email.html'

def send_welcome_email(username, email):
    """
    Sends a welcome email to the new user.
    
    Args:
        username (str): The username of the new user.
        email (str): The email address of the new user.
    """
    try:
        # Render the email template
        html_message = render_to_string(TEMPLATE_PATH, {'username': username})

        send_mail(
            subject=EMAIL_SUBJECT,
            message="",  # No plain text message since we are using HTML
            from_email=FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
        )
        logger.info(f"Welcome email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {email}: {e}")

@receiver(post_save, sender=User)
def send_welcome_email_on_user_creation(sender, instance, created, **kwargs):
    """
    Signal receiver that sends a welcome email when a new user is created.
    
    Args:
        sender (Model): The model class.
        instance (Model instance): The actual instance being saved.
        created (bool): A boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        send_welcome_email(instance.username, instance.email)