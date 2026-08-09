from django.shortcuts import render
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from files.serializers import FileSerializer
from files.models import File

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'files': reverse('files', request=request, format=format),
            # ^ name of field ^ name of url it referse to 
            # 'users': reverse('users', request=request, format=format),
        }
    )

class FileView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()

class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()

# class UserView(generics.ListAPIView):
#     serializer_class = UserSerializer
