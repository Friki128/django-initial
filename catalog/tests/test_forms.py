from django.test import SimpleTestCase
from catalog.forms import RenewBookForm
import datetime 
from django.utils import timezone
from django import forms

class RenewBookFormTests(SimpleTestCase):
    def test_renewal_date_label(self):
        form = RenewBookForm()
        self.assertEqual('renewal date', form.fields['due_back'].label)
    
    def test_renewal_date_help_text(self):
        form = RenewBookForm()
        self.assertEqual('Enter a date between now and 4 weeks', form.fields['due_back'].help_text)
    
    def test_renew_book_form_fields(self):
        form = RenewBookForm()
        self.assertEqual(form._meta.fields, ['due_back'])

    def test_renewal_date_widget(self):
        form = RenewBookForm()
        self.assertTrue(isinstance(form.fields['due_back'].widget, forms.DateInput))

    def test_renewal_date_in_the_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_renewal_date_too_far_in_the_future(self):
        date = datetime.date.today() + datetime.timedelta(days=1) + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_renewal_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'due_back': date})
        self.assertTrue(form.is_valid())

    def test_renewal_date_max_date(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'due_back': date})
        self.assertTrue(form.is_valid())
