from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel


class UserSettings(TimeStampedModel):
    """
    Model to store additional user settings and preferences. Extends User
    model.
    """
    user = models.OneToOneField(User, related_name='settings')
    credit = models.PositiveIntegerField(null=True,blank=True)
    checked = models.BooleanField(default=False)

    def username(self):
        return self.user.username
    username.admin_order_field = 'user__username'

    class Meta:
        verbose_name_plural = 'User Settings'