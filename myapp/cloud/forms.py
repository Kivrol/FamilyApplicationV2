from django import forms
from django.core.exceptions import ValidationError
from .models import CloudFile

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class UploadVideoFile(forms.ModelForm):
    class Meta:
        model = CloudFile
        fields = ['video_file']

    def clean_video_file(self):
        if self.cleaned_data['video_file'] is None:
            raise ValidationError("Файл не может быть пустым")
        return self.cleaned_data['video_file']


class UploadPhotoFile(forms.ModelForm):
    class Meta:
        model = CloudFile
        fields = ['photo_file']

    def clean_photo_file(self):
        if self.cleaned_data['photo_file'] is None:
            raise ValidationError("Файл не может быть пустым")
        return self.cleaned_data['photo_file']




class UploadDocFile(forms.ModelForm):
    class Meta:
        model = CloudFile
        fields = ['doc_file']

    def clean_doc_file(self):
        if self.cleaned_data['doc_file'] is None:
            raise ValidationError("Файл не может быть пустым")
        return self.cleaned_data['doc_file']


class UploadArchiveFile(forms.ModelForm):
    class Meta:
        model = CloudFile
        fields = ['archive_file']

    def clean_archive_file(self):
        if self.cleaned_data['archive_file'] is None:
            raise ValidationError("Файл не может быть пустым")
        return self.cleaned_data['archive_file']