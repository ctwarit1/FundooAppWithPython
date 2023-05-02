import json
from datetime import datetime, timedelta

from django.db import models
from user.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    color = models.CharField(max_length=10, null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='notes_images', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField('notes.Label')


class Label(models.Model):
    name = models.CharField(max_length=150, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


@receiver(signal=post_save, sender=Note)
def notes_reminder(instance: Note, **kwargs):
    date = instance.reminder
    if date:
        current_date = datetime.now()
        time_data = instance.reminder
        reminder_date = time_data.date()
        no_of_days = (reminder_date - current_date.date()).days
        remainder_time = current_date + timedelta(days=no_of_days)
        crontab, created = CrontabSchedule.objects.get_or_create(
            hour=time_data.hour,
            minute=time_data.minute,
            day_of_month=remainder_time.day,
            month_of_year=time_data.month,
        )
        task_present = PeriodicTask.objects.filter(
            name=f'{instance.user.id}-{instance.id}-{instance.title}'
        )
        if task_present.exists():
            task_present = task_present.first()
            task_present.crontab = crontab
            task_present.save()
        else:
            PeriodicTask.objects.create(
                crontab=crontab,
                name=f'{instance.user.id}-{instance.id}-{instance.title}',
                task='notes.tasks.send_mail_func',
                args=json.dumps([instance.user.email, instance.title]),
            )

