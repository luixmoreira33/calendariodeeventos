from django.db import models

# Create your models here.

class Setup(models.Model):
    url = models.CharField(
        max_length=255,
        verbose_name='URL',
        help_text='Escreva a URL do sistema',
    )
    calendar_url = models.CharField(
        max_length=255,
        verbose_name='URL do Google Calendar',
        help_text='Escreva a URL do Google Calendar',
    )
    admin_email = models.EmailField(
        max_length=255,
        verbose_name='Email do administrador',
        help_text='Escreva o email do administrador',
    )

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
