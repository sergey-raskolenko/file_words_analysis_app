from django.db import models
from django.contrib.postgres.fields import ArrayField

NULLABLE = {'null': True, 'blank': True}


class UploadedFile(models.Model):
    """
    Модель для загруженных файлов
    """
    file = models.FileField(upload_to='', verbose_name='Файл')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    cleaned_text = ArrayField(models.CharField(max_length=100), verbose_name='Очищенный список слов', **NULLABLE)

    class Meta:
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'
        db_table = 'file'

    def __str__(self):
        return str(self.file).split('/')[-1]

    def __repr__(self):
        return f'File({self.file}, {self.uploaded_at}'


class ProcessedWord(models.Model):
    """
    Модель для обработанных слов файла
    """
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, verbose_name='Файл')
    word = models.CharField(max_length=100, verbose_name='Слово')
    tf = models.FloatField(verbose_name='Частота слова', **NULLABLE)
    idf = models.FloatField(verbose_name='Обратная частота документа', **NULLABLE)

    class Meta:
        verbose_name = 'Processed Word'
        verbose_name_plural = 'Processed Words'
        db_table = 'word'

    def __str__(self):
        return f'{self.word}'

    def __repr__(self):
        return f'Word({self.word}, {self.tf}, {self.idf})'
