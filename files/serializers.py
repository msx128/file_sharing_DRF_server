from rest_framework import serializers
from files.models import File
from django.contrib.auth.models import User

class FileSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = File
        fields = ['id', 'title', 'extention', 'size', 'created', 'file']
        
