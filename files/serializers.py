from rest_framework import serializers
from files.models import File
from django.contrib.auth.models import User

class FileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = File
        fields = ['id','user', 'created', 'file', 'size', 'title', 'extention']
        # id and created is read-only by default
        # don't know if it illogical to keep them in fileds
        read_only_fields = ['size', 'title', 'extention']
        
class UserSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(
        many=True, queryset=File.objects.all()
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'files']

