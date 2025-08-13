from django.db import models

from core.behaviours.trackable import Trackable
from core.utils.choices import CITY


class Lodge(Trackable):
    name = models.CharField(
        max_length=255,
        verbose_name='Nome da loja'
    )
    city = models.CharField(
        max_length=255,
        verbose_name='Cidade',
        choices=CITY
    )
    number = models.CharField(
        max_length=20,
        verbose_name='Número',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'

