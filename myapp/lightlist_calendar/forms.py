from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import CalendarItem


class AddCalendarItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCalendarItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CalendarItem
        exclude = ['group', 'creator']
        widgets = {
            'start': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end': forms.TextInput(attrs={'type': 'datetime-local'}),
            'notification': forms.TextInput(attrs={'type': 'hidden'}),
        }

    def clean_start(self):
        print(self.cleaned_data)
        if self.cleaned_data['start'] < timezone.now():
            raise ValidationError("Начальная дата не может быть раньше текущей")
        return self.cleaned_data['start']

    def clean_end(self):
        if 'start' not in self.cleaned_data:
            raise ValidationError("Некорректная начальная дата")
        if self.cleaned_data['start'] > self.cleaned_data['end']:
            raise ValidationError("Конечная дата не может быть раньше начальной")
        if self.cleaned_data['end'] > self.cleaned_data['start'] + timezone.timedelta(days=28):
            raise ValidationError("Длительность события не должна превышать месяца")
        return self.cleaned_data['end']




class EditCalendarItemForm(forms.ModelForm):
    class Meta:
        model = CalendarItem
        exclude = ['group', 'creator']

    def clean_end(self):
        if self.cleaned_data['start'] > self.cleaned_data['end']:
            raise ValidationError("Конечная дата не может быть раньше начальной")
        if self.cleaned_data['end'] > self.cleaned_data['start'] + timezone.timedelta(days=28):
            raise ValidationError("Длительность события не должна превышать месяца")
        return self.cleaned_data['end']

    def clean_notification(self):
        if self.cleaned_data['notification'] is not None and self.cleaned_data['notification'] > self.cleaned_data[
            'end']:
            raise ValidationError("Напоминание не может быть позже конца события")
        if self.cleaned_data['notification'] is not None and self.cleaned_data['notification'] < self.cleaned_data[
            'start']:
            return None
        return self.cleaned_data['notification']
