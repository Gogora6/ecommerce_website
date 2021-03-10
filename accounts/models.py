from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from .options.choices import GenderChoices
from .options.validators import phone_number_validator
from .managers import UserManager


class User(AbstractUser):
    # Firstname, Lastname, is_staff(Def=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    gender = models.PositiveSmallIntegerField(choices=GenderChoices.choices, blank=True, null=True,
                                              verbose_name=_("Gender"))
    phone_number = models.CharField(max_length=50, verbose_name=_('Phone Number'), validators=[phone_number_validator])
    ip_address = models.GenericIPAddressField(verbose_name=_("User Register IP address"), blank=True, null=True)
    approve_email = models.BooleanField(default=False, verbose_name=_("Is this user email approved?"))

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')


class AddressToUser(models.Model):
    user = models.ForeignKey(
        to='accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='AddressToUser'
    )

    address = models.CharField(max_length=255, verbose_name=_('Address'))

    def __str__(self):
        return self.address
