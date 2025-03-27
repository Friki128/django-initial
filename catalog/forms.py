from django.forms import ModelForm
from catalog.models import BookInstance
import datetime
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms

class RenewBookForm(ModelForm):
    class Meta:
        model=BookInstance
        fields=['due_back']
        labels={'due_back': _('renewal date')}
        help_texts={'due_back': _('Enter a date between now and 4 weeks')}
        widgets = {
            'due_back': forms.DateInput(attrs={'type': 'date'})
        }
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if data < datetime.date.today():
            raise ValidationError(_('The date cannot be in the past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('The date is too far in the future'))
        return data
