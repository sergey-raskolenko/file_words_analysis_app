from django.urls import path
from file.apps import FileConfig
from file.views import upload_file, file_list, processed_file_detail

app_name = FileConfig.name

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('files/<int:file_id>/', processed_file_detail, name='file_detail'),
]
