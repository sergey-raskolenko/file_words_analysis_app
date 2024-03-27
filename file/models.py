from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to='data/', verbose_name='Файл')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'
        db_table = 'file'

    def __str__(self):
        return f'{self.file}'

    def __repr__(self):
        return f'File({self.file}, {self.uploaded_at}'


class ProcessedWord(models.Model):
    word = models.CharField(max_length=100, verbose_name='Слово')
    tf = models.IntegerField(verbose_name='Частота слова')
    idf = models.FloatField(verbose_name='Обратная частота документа')

    class Meta:
        verbose_name = 'Processed Word'
        verbose_name_plural = 'Processed Words'
        db_table = 'word'

    def __str__(self):
        return f'{self.word}'

    def __repr__(self):
        return f'Word({self.word}, {self.tf}, {self.idf})'
