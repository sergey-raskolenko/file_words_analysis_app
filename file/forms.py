from django import forms
from django.core.exceptions import ValidationError

from config.settings import ALLOWED_FILE_FORMATS
from file.models import UploadedFile


class UploadedFileForm(forms.ModelForm):
    """
    Форма для загрузки файлов с проверкой его расширения
    """

    class Meta:
        model = UploadedFile
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_name = file.name
            if not file_name.endswith(tuple(ALLOWED_FILE_FORMATS)):
                raise ValidationError(
                    f"Неверный формат файла. Поддерживаются только файлы с расширением: "
                    f"{', '.join(ALLOWED_FILE_FORMATS)}"
                )
        return file
