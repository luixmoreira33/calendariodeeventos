from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from lodge.models import Lodge
from setup.models import Profession


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=15,
        verbose_name=_('Número de telefone'),
        blank=True,
        null=True
    )
    profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        verbose_name=_('Profissão'),
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username 

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')


class UserLodge(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Usuário')
    )
    lodge = models.ForeignKey(
        Lodge,
        on_delete=models.CASCADE,
        verbose_name=_('Loja')
    )

    def __str__(self):
        return f"{self.user.username} - {self.lodge.name}"

    class Meta:
        verbose_name = _('Loja')
        verbose_name_plural = _('Lojas')


class Brother(CustomUser):
    class Meta:
        proxy = True
        verbose_name = _('Irmão')
        verbose_name_plural = _('Irmãos')
        ordering = ['first_name', 'last_name']
