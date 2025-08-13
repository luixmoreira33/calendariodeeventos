from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import UserRequestForm
from .utils import send_email_notification
from setup.models import Setup


def user_request_view(request):
    if request.method == 'POST':
        form = UserRequestForm(request.POST)
        setup = Setup.objects.last()

        if form.is_valid():
            user_request = form.save()
            
            # Send email to admin
            send_email_notification(
                subject='Nova solicitação de cadastro de usuário',
                template_name='email/user_request_notification.html',
                context={
                    'user_request': user_request,
                    'login_url': f"{setup.url}"
                },
                recipient_list=[setup.admin_email]
            )
            
            # Send confirmation email to user
            send_email_notification(
                subject='Sua solicitação de cadastro foi recebida',
                template_name='email/user_request_confirmation.html',
                context={'user_request': user_request},
                recipient_list=[user_request.email]
            )

            messages.success(request, 'Sua solicitação foi enviada com sucesso! Você receberá um email quando sua solicitação for analisada.')
            return redirect('calendarrequest:user_request')
    else:
        form = UserRequestForm()
    
    return render(request, 'user_request.html', {'form': form})
