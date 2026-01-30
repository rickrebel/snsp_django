from django.db import models
from django.utils import timezone


class Institution(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(
        max_length=100, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'institution'

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_internal = models.BooleanField(default=True)
    icon = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'program'

    def __str__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'action'

    def __str__(self):
        return self.name
