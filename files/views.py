from typing import override
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions
from files.serializers import FileSerializer, UserSerializer
from files.models import File
from files.permissions import IsOwnerOrReadOnly

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'files': reverse('files', request=request, format=format),
            # ^ name of field ^ name of url it referse to 
            'users': reverse('users', request=request, format=format),
        }
    )

class FileView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = FileSerializer
    queryset = File.objects.all()

    @override
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # we don't need to override functions in filedetailview because
        # we can assume it's already created so user field is already exists

class FileDetailView(generics.RetrieveDestroyAPIView):
    # don't know if I need put method
    # if I would need to change save method
    # like: if self.file.title ? changing title possible : auto
    # but how to change readonly fields? probaly make it not read-only
    # maybe just open title field and let user decide change it or not
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = FileSerializer
    queryset = File.objects.all()

class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
