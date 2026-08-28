import os
from typing import override

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

# Create your models here.

def validate_file_size(value):
    limit = 10 * 1024 * 1024
    if value > limit:
            raise ValidationError("File too large, size should not exeed 10MB")

class File(models.Model):
    id = models.AutoField(primary_key=True)
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
            validate_file_size(self.file.size)
            self.size = self.file.size
            name, ext = os.path.splitext(self.file.name)
            self.title = slugify(name)[:100]
            self.extention = ext.lstrip('.')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created"]
