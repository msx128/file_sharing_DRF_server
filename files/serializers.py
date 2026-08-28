from django.contrib.auth.models import User
from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = File
        fields = ['id','user', 'created', 'file', 'size', 'title', 'extension']
        # id and created is read-only by default
        # don't know if it illogical to keep them in fileds
        read_only_fields = ['size', 'title', 'extension', 'id']

    def create(self,validated_data):
        validated_data['user'] = self.context['request'].user
        return File.objects.create(**validated_data)
        
class UserSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(
        many=True, queryset=File.objects.all()
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'files']

