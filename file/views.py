from django.shortcuts import render

from file.forms import UploadedFileForm
from file.models import UploadedFile, ProcessedWord


def upload_file(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            # Логика по подсчету tf-idf слов в файле
    else:
        form = UploadedFileForm()
    return render(
        request, 'file/upload_file.html', {'form': form}
    )


def file_list(request):
    files = UploadedFile.objects.all()
    return render(
        request, 'file/file_list.html', {'files': files}
    )


# def processed_file_detail(request, file_id):
#     processed_words = ProcessedWord.objects.filter(file=file_id).order_by('-idf')[:50]
#     return render(
#         request, 'file/file_detail.html', {'processed_words': processed_words}
#     )
