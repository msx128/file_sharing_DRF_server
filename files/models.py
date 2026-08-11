import os
from typing import override
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class File(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='./filebase')
    size = models.BigIntegerField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='files'
    )
    title = models.CharField(max_length=100)
    extention = models.CharField(max_length=20, blank=True)

    @override
    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
            name, ext = os.path.splitext(self.file.name)
            self.title = slugify(name)[:100]
            self.extention = ext.lstrip('.')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created"]
