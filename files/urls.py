from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from files import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root, name='root'),
    path('files', views.FileView.as_view(), name='files'),
    path('files/<int:pk>', views.FileDetailView.as_view(), name='file_details')
 ])

