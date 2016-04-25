from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from guardian.shortcuts import get_perms
from userena import settings as userena_settings
from userena.managers import UserenaManager, UserenaBaseProfileManager
from userena.utils import get_gravatar, generate_sha1, get_protocol, \
    get_datetime_now, user_model_label
import datetime


class UserenaSignup(models.Model):
    """
    Userena model which stores all the necessary information to have a full
    functional user implementation on your Django website.
    """
    user = models.OneToOneField(user_model_label,
                                verbose_name=_('user'),
                                related_name='userena_signup')

    last_active = models.DateTimeField(_('last active'),
                                       blank=True,
                                       null=True,
                                       help_text=_('The last date that the user was active.'))

    activation_key = models.CharField(_('activation key'),
                                      max_length=40,
                                      blank=True)

    activation_notification_send = models.BooleanField(_('notification send'),
                                                       default=False,
                                                       help_text=_('Designates whether this user has already got a notification about activating their account.'))

    email_unconfirmed = models.EmailField(_('unconfirmed email address'),
                                          blank=True,
                                          help_text=_('Temporary email address when the user requests an email change.'))

    email_confirmation_key = models.CharField(_('unconfirmed email verification key'),
                                              max_length=40,
                                              blank=True)

    email_confirmation_key_created = models.DateTimeField(_('creation date of email confirmation key'),
                                                          blank=True,
                                                          null=True)

    objects = UserenaManager()

    