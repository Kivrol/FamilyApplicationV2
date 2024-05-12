from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from main.models import Family


class CloudFile(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    video_file = models.FileField(upload_to='files/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'mov', 'webm', 'avi'])])
    photo_file = models.FileField(upload_to='files/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'png', 'ico', 'jpeg', 'bmp', 'webp'])])
    doc_file = models.FileField(upload_to='files/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['doc', 'docx', 'pdf', 'odt', 'rtf', 'txt', 'ppt', 'pptx', 'xls', 'xlsx'])])
    archive_file = models.FileField(upload_to='files/', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['zip', 'rar', '7z', 'tar', 'gz'])])
    category = models.CharField(max_length=50, null=True, blank=True, choices=(('photo', 'Изображение'),
                                                                               ('doc', 'Документ'),
                                                                               ('archive', 'Архив'),
                                                                               ('video', 'Видео')))
    objects = models.Manager()

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        if self.video_file:
            return f'{self.video_file}'
        elif self.photo_file:
            return f'{self.photo_file.name}'
        elif self.doc_file:
            return f'{self.doc_file.name}'
        elif self.archive_file:
            return f'{self.archive_file.name}'
        return f'Пустой файл'
