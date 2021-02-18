from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    """
        Patient information in hospital database
    """
    CHOICES = [(True, 'Infected'), (False, 'Cured'), ('Suspected', 'Suspected')]
    uid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, blank=False, default='')
    surname = models.CharField(max_length=70, blank=False, default='')
    address = models.CharField(max_length=256, blank=False, default='')
    email = models.CharField(max_length=256, blank=False, default='')
    city = models.CharField(max_length=70, blank=False, default='')
    region = models.CharField(max_length=70, blank=False, default='')
    postal = models.CharField(max_length=70, blank=False, default='')
    country = models.CharField(max_length=70, blank=False, default='')
    phone = models.CharField(max_length=70, blank=False, default='')
    status = models.CharField(max_length=20, choices=CHOICES, null=True, default='')
    notes = models.TextField(null=True, blank=True)
    created_at = models.CharField(max_length=70, blank=False, default='')
    hashing = models.CharField(max_length=100, blank=False, default='')
