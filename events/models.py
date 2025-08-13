import logging

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.db import transaction

from setup.models import Setup
from lodge.models import Lodge
from core.behaviours.trackable import Trackable
from calendarrequest.utils import send_email_notification
from events.googlecalendar.actions import get_calendar_service

logger = logging.getLogger(__name__)


class Event(Trackable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuário'
    )
    lodge = models.ForeignKey(
        Lodge,
        on_delete=models.CASCADE,
        verbose_name='Loja',
        blank=True,
        null=True
    )
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True)
    start_time = models.DateTimeField('Data/hora de início')
    end_time = models.DateTimeField('Data/hora de término')
    address = models.CharField('Endereço', max_length=500)
    google_event_id = models.CharField(
        'ID do evento do Google',
        max_length=255,
        blank=True,
        null=True,
        help_text='Valor preenchido automaticamente após o evento ser criado no Google Calendar.'
    )
    is_cancelled = models.BooleanField('Cancelado', default=False)

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'


@receiver(post_save, sender=Event)
def event_post_save(sender, instance, created, **kwargs):
    try:
        calendar_service = get_calendar_service()
        setup = Setup.objects.last()
        
        if created:
            google_event_id = calendar_service.create_event(instance)
            Event.objects.filter(pk=instance.pk).update(
                google_event_id=google_event_id
            )
            
            # Send notification email to user
            try:
                send_email_notification(
                    subject='Evento Criado com Sucesso',
                    template_name='email/event_created_notification.html',
                    context={
                        'event': instance,
                        'calendar_url': setup.calendar_url if setup else 'https://calendar.google.com/calendar'
                    },
                    recipient_list=[instance.user.email]
                )
            except Exception as email_error:
                logger.error(
                    "Error sending event creation notification email: %s",
                    str(email_error),
                    extra={
                        'event_id': instance.pk,
                        'event_title': instance.title,
                        'user_email': instance.user.email
                    }
                )
        else:
            if instance.is_cancelled:
                try:
                    calendar_service.delete_event(instance)
                    
                    # Send cancellation notification email to user
                    try:
                        send_email_notification(
                            subject='Evento Cancelado',
                            template_name='email/event_cancelled_notification.html',
                            context={'event': instance},
                            recipient_list=[instance.user.email]
                        )
                    except Exception as email_error:
                        logger.error(
                            "Error sending event cancellation notification email: %s",
                            str(email_error),
                            extra={
                                'event_id': instance.pk,
                                'event_title': instance.title,
                                'user_email': instance.user.email
                            }
                        )
                except Exception as e:
                    logger.error(
                        "Error deleting existing event from Google Calendar during update: %s",
                        str(e),
                        extra={
                            'event_id': instance.pk,
                            'event_title': instance.title,
                            'google_event_id': instance.google_event_id
                        }
                    )
            else:
                if instance.google_event_id:
                    calendar_service.update_event(instance)
    except Exception as e:
        logger.error(
            "Error syncing event with Google Calendar: %s",
            str(e),
            extra={
                'event_id': instance.pk,
                'event_title': instance.title,
                'is_new_event': created
            }
        )
