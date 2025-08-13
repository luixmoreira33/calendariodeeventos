from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_notification(subject, template_name, context, recipient_list):
    """
    Helper function to send HTML emails with plain text fallback.
    
    Args:
        subject (str): Email subject
        template_name (str): Path to the HTML template
        context (dict): Context data for the template
        recipient_list (list): List of recipient email addresses
    """
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    ) 