from django.utils.translation import gettext_lazy as _
from django.db.models import IntegerChoices


class GenderChoices(IntegerChoices):
    customer = 1, _("Male")
    washer = 2, _("Female")
    manager = 3, _("Other")
