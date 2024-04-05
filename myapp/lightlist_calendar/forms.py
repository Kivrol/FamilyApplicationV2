from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import CalendarItem


class AddCalendarItemForm(forms.ModelForm):
    class Meta:
        model = CalendarItem
        exclude = ['group', 'creator']
        widgets = {
            'start': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end': forms.TextInput(attrs={'type': 'datetime-local'}),
            'notification': forms.TextInput(attrs={'type': 'datetime-local'})
        }

    def clean_end(self):
        can_validate = 'end' in self.cleaned_data and 'start' in self.cleaned_data and self.cleaned_data['end'] is not None
        if can_validate and self.cleaned_data['start'] > self.cleaned_data['end']:
            raise ValidationError("Конечная дата не может быть раньше начальной")
        if self.cleaned_data['end'] is None:
            return self.cleaned_data['start']+timezone.timedelta(minutes=10)
        return self.cleaned_data['end']

    def clean_notification(self):
        can_validate = 'end' in self.cleaned_data and 'notification' in self.cleaned_data and self.cleaned_data['notification'] is not None and self.cleaned_data['end'] is not None
        if can_validate and self.cleaned_data['notification'] > self.cleaned_data['end']:
            raise ValidationError("Напоминание не может быть позже конца события")
        if self.cleaned_data['notification'] is not None and self.cleaned_data['notification'] < timezone.now():
            raise ValidationError("Напоминание не может быть раньше текущей даты")
        return self.cleaned_data['notification']
