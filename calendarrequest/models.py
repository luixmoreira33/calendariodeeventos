import logging

from django.db import models, transaction
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from core.behaviours.trackable import Trackable
from core.utils.choices import CITY
from .utils import send_email_notification

from setup.models import Setup

from events.models import Event

from lodge.models import Lodge

CustomUser = get_user_model()


class StoreRequest(Trackable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Qual é a sua loja?',
        help_text='Escreva o nome completo da sua loja com o número. Ex: LOJA FULANO DE TAL Nº 0000',
    )
    city = models.CharField(
        max_length=255,
        choices=CITY,
        verbose_name='Cidade',
        help_text='Selecione a cidade onde a loja está localizada',
    )
    number = models.CharField(
        max_length=20,
        verbose_name='Número',
        blank=True,
        null=True
    )
    approved = models.BooleanField(
        default=False,
        verbose_name='Aprovado',
        help_text='Marque como aprovado se a loja foi aprovada e cadastrada',
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Solicitação de Loja'
        verbose_name_plural = 'Solicitações de Loja'


@receiver(post_save, sender=StoreRequest)
def create_lodge_on_approval(sender, instance, created, **kwargs):
    logger = logging.getLogger(__name__)
    setup = Setup.objects.last()

    if created and setup:
        # Use transaction.on_commit to avoid transaction issues
        transaction.on_commit(lambda: _send_store_request_notification(instance, setup, logger))

    if instance.approved and not created and setup:
        # Use transaction.on_commit to avoid transaction issues
        transaction.on_commit(lambda: _create_lodge_and_notify(instance, setup, logger))


def _send_store_request_notification(instance, setup, logger):
    """
    Helper function to send store request notification after transaction commit
    """
    try:
        send_email_notification(
            subject='Nova Solicitação de Criação de Loja',
            template_name='email/store_request_notification.html',
            context={
                'store_request': instance,
                'login_url': setup.url
            },
            recipient_list=[setup.admin_email]
        )
        logger.info(f"Store request notification sent to {setup.admin_email}")
    except Exception as e:
        logger.error(f"Error sending store request notification: {e}")


def _create_lodge_and_notify(instance, setup, logger):
    """
    Helper function to create lodge and send approval notification after transaction commit
    """
    try:
        lodge, created = Lodge.objects.get_or_create(
            name=instance.name,
            defaults={
                'city': instance.city,
                'number': instance.number,
            }
        )
        
        logger.info(f"Lodge {'created' if created else 'found'}: {lodge.name}")
        
        # Send approval notification email to the user
        send_email_notification(
            subject='Sua solicitação de loja foi aprovada',
            template_name='email/store_request_approval.html',
            context={
                'store_request': instance,
                'lodge': lodge,
                'login_url': setup.url
            },
            recipient_list=[instance.user.email]
        )
        
        logger.info(f"Store approval email sent to {instance.user.email}")
        
    except Exception as e:
        logger.error(f"Error in lodge creation/notification: {e}")


class CancelEventRequest(Trackable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name='Evento',
    )
    reason = models.TextField("Motivo", blank=True)
    reviewed = models.BooleanField("Revisado", default=False)

    def __str__(self):
        return f"Cancelamento de {self.event.title} - {'Revisado' if self.reviewed else 'Pendente'}"
    
    class Meta:
        verbose_name = 'Solicitação de Cancelamento de Evento'
        verbose_name_plural = 'Solicitações de Cancelamento de Evento'


class UserRequest(Trackable):
    name = models.CharField(
        max_length=255,
        verbose_name='Nome',
        help_text='Escreva o nome do usuário',
    )
    surname = models.CharField(
        max_length=255,
        verbose_name='Sobrenome',
        help_text='Escreva o sobrenome do usuário',
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Escreva o email do usuário',
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Telefone',
        help_text='Escreva o telefone do usuário',
    )
    profession = models.ForeignKey(
        'setup.Profession',
        on_delete=models.SET_NULL,
        verbose_name='Profissão',
        help_text='Selecione sua profissão',
        blank=True,
        null=True
    )
    message = models.TextField(
        verbose_name='Mensagem',
        help_text='Escreva a mensagem do usuário',
        blank=True,
        null=True
    )
    lodge_name = models.CharField(
        max_length=255,
        verbose_name='Nome da loja',
        help_text='Escreva o nome da loja',
    )
    lodge_number = models.CharField(
        max_length=20,
        verbose_name='Número da loja',
        help_text='Escreva o número da loja',
    )
    approved = models.BooleanField(
        default=False,
        verbose_name='Aprovado',
        help_text='Marque como aprovado se o usuário foi aprovado e cadastrado',
    )

    def __str__(self):
        profession_str = f" ({self.profession})" if self.profession else ""
        return f"Solicitação de {self.name}{profession_str} - {self.email} - {self.lodge_number}"
    
    class Meta:
        verbose_name = 'Solicitação de Usuário'
        verbose_name_plural = 'Solicitações de Usuário'


@receiver(post_save, sender=UserRequest)
def create_user_on_approval(sender, instance, created, **kwargs):
    """
    Signal to create a CustomUser when a UserRequest is approved and send email notification
    """
    logger = logging.getLogger(__name__)
    if instance.approved and not created:
        # Use transaction.on_commit to avoid transaction issues
        transaction.on_commit(lambda: _create_user_and_notify(instance, logger))


def _create_user_and_notify(instance, logger):
    """
    Helper function to create user and send notifications after transaction commit
    """
    setup = Setup.objects.last()
    random_password = get_random_string(12)

    try:
        # Create the user
        user = CustomUser.objects.create_user(
            username=instance.email,
            email=instance.email,
            password=random_password,
            first_name=instance.name,
            last_name=instance.surname,
            phone_number=instance.phone,
            profession=instance.profession,
            is_staff=True
        )
        
        logger.info(f"User created successfully: {user.email}")
        
        # Try to find and associate the lodge
        try:
            from lodge.models import Lodge
            lodge = Lodge.objects.get(number=instance.lodge_number)
            
            # Create UserLodge association
            from accounts.models import UserLodge
            UserLodge.objects.create(
                user=user,
                lodge=lodge
            )
            
            logger.info(f"User {user.email} associated with lodge {lodge.name}")
            
        except Lodge.DoesNotExist:
            logger.warning(f"Lodge with number {instance.lodge_number} not found for user {instance.email}")
        except Exception as e:
            logger.error(f"Error associating user with lodge: {e}")
        
        # Send approval email with password only if setup exists
        if setup:
            try:
                send_email_notification(
                    subject='Sua solicitação de cadastro foi aprovada',
                    template_name='email/user_request_approval.html',
                    context={
                        'user': instance,
                        'password': random_password,
                        'login_url': setup.url
                    },
                    recipient_list=[instance.email]
                )
                logger.info(f"Approval email sent to {instance.email}")
            except Exception as e:
                logger.error(f"Error sending approval email: {e}")
        else:
            logger.warning(f"No Setup configuration found. Approval email not sent for {instance.email}")
        
    except Exception as e:
        logger.error(f"Error creating user for {instance.email}: {e}")
