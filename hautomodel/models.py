from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# If you want every user to have an automatically generated Token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.
class AutoMLModel(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    model_type = models.CharField(max_length=30)
    automl_backend = models.CharField(max_length=30, null=True)
    accuracy_score = models.CharField(max_length=30, null=True)
    train_status = models.CharField(max_length=30, null=True)
    date_created = models.DateField(null=True)
    timestamp_created = models.DateField(null=True)
    columns = models.TextField(null=True)

    def __str__(self):
        return self.name