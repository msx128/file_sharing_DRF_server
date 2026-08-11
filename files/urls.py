from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from files import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root, name='root'),
    path('files', views.FileView.as_view(), name='files'),
    path('files/<int:pk>', views.FileDetailView.as_view(), name='file_details'),
    path('users', views.UserView.as_view(), name='users'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user_details'),
 ])
urlpatterns += [
    path('auth', include('rest_framework.urls')),
]
