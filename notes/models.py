from django.db import models
from user.models import User


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
