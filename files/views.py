from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
import logging
from typing import override

from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from files.models import File
from files.permissions import IsOwnerOrReadOnly
from files.serializers import FileSerializer, UserSerializer

# Create your views here.

logger = logging.getLogger(__name__)

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

    @override
    def perform_destroy(self, instance):
        if instance.file:
            try:
                instance.file.delete(save=False)
        # same as instance.file.storage.delete(instance.file.name)
        # preferable to add some tracking solution which would queue deletion on failure
            except Exception as e:
                logger.error(f"Failed to delete file from S3: {e}")
        return super().perform_destroy(instance) # <- this whould delete postgres instance

class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Refreash token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
            
