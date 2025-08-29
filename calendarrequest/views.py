import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import UserRequestForm
from .utils import send_email_notification
from setup.models import Setup

logger = logging.getLogger(__name__)


def user_request_view(request):
    if request.method == 'POST':
        form = UserRequestForm(request.POST)
        setup = Setup.objects.last()

        if form.is_valid():
            user_request = form.save()
            logger.info(f"User request created: {user_request.email}")
            
            # Only send emails if setup exists
            if setup:
                try:
                    # Send email to admin
                    send_email_notification(
                        subject='Nova solicitação de cadastro de usuário',
                        template_name='email/user_request_notification.html',
                        context={
                            'user_request': user_request,
                            'login_url': setup.url
                        },
                        recipient_list=[setup.admin_email]
                    )
                    logger.info(f"Admin notification sent to {setup.admin_email}")
                except Exception as e:
                    logger.error(f"Error sending admin notification: {e}")
                
                try:
                    # Send confirmation email to user
                    send_email_notification(
                        subject='Sua solicitação de cadastro foi recebida',
                        template_name='email/user_request_confirmation.html',
                        context={'user_request': user_request},
                        recipient_list=[user_request.email]
                    )
                    logger.info(f"User confirmation sent to {user_request.email}")
                except Exception as e:
                    logger.error(f"Error sending user confirmation: {e}")
            else:
                logger.warning("No Setup configuration found. Emails not sent.")

            messages.success(request, 'Sua solicitação foi enviada com sucesso! Você receberá um email quando sua solicitação for analisada.')
            return redirect('calendarrequest:user_request')
    else:
        form = UserRequestForm()
    
    return render(request, 'user_request.html', {'form': form})
