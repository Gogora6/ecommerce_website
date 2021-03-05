from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(regex=r'(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9['
                                              r'8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2['
                                              r'70]|7|1)\d{1,14}$',
                                        message=_("Phone number must be entered in the format: '9999999999'. Up to 20 "
                                                  "digits allowed."))
