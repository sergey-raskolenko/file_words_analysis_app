import os
from collections import Counter

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse, reverse_lazy

from config.settings import MEDIA_ROOT
from file.forms import UploadedFileForm
from file.models import UploadedFile, ProcessedWord
from file.services import clean_text


def upload_file(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            # Логика по подсчету tf-idf слов в файле
    else:
        form = UploadedFileForm()
    return render(
        request, 'file/uploadedfile_form.html', {'form': form}
    )


class FileUploadView(CreateView):
    model = UploadedFile
    form_class = UploadedFileForm

    def get_success_url(self):
        return reverse('file:upload_file')

    def form_valid(self, form):

        self.object = form.save()
        file_path = os.path.join(MEDIA_ROOT, str(self.object.file))
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            self.object.cleaned_text = clean_text(text)

        self.object.save()

        # Подсчет TF
        word_counts = Counter(self.object.cleaned_text)
        total_words = len(self.object.cleaned_text)

        word_objects = []

        for word, count in word_counts.items():
            tf = round(count / total_words, 3)
            word_objects.append(ProcessedWord(word=word, file=self.object, tf=tf))

        ProcessedWord.objects.bulk_create(word_objects)

        # Подсчет IDF
        word_count_per_file = ProcessedWord.objects.values('word').annotate(num_files=Count('file'))
        files_amount = UploadedFile.objects.all().count()

        for item in word_count_per_file:
            idf = item['num_files'] / files_amount
            ProcessedWord.objects.filter(word=item['word']).update(idf=idf)

        return super().form_valid(form)


class UploadedFileList(ListView):
    model = UploadedFile
    success_url = reverse_lazy('file:file_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['files'] = UploadedFile.objects.all()

        return context_data


class UploadedFileDetailView(DetailView):
    model = UploadedFile

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['processed_words'] = ProcessedWord.objects.filter(file=self.object.id).order_by('-idf', '-tf')[:50]
        return context_data
