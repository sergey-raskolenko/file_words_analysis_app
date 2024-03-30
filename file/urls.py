from django.urls import path
from file.apps import FileConfig
from file.views import FileUploadView, UploadedFileList, UploadedFileDetailView

app_name = FileConfig.name

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('files/', UploadedFileList.as_view(), name='file_list'),
    path('files/<int:pk>/', UploadedFileDetailView.as_view(), name='file_detail'),
]
