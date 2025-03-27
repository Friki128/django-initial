from django.test import TestCase
from catalog.models import Author
import datetime

class AuthorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Kytheon', last_name='Jura', date_of_birth='1999-12-31', date_of_death='2019-03-21')
        Author.objects.create(first_name='Jace', last_name='Belereen')

    def test_first_name(self):
        author = Author.objects.get(id=1)
        first_name=author.first_name
        self.assertEqual(first_name, 'Kytheon')

    def test_last_name(self):
        author = Author.objects.get(id=1)
        last_name=author.last_name
        self.assertEqual(last_name, 'Jura')

    def test_date_of_birth(self):
        author = Author.objects.get(id=1)
        date_of_birth=author.date_of_birth
        self.assertEqual(date_of_birth, datetime.date(1999,12,31))
    
    def test_date_of_death(self):
        author = Author.objects.get(id=1)
        date_of_death=author.date_of_death
        self.assertEqual(date_of_death, datetime.date(2019,3,21))

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        label=author._meta.get_field('first_name').verbose_name
        self.assertEqual(label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        label=author._meta.get_field('last_name').verbose_name
        self.assertEqual(label, 'last name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        label=author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(label, 'died')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        label=author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(label, 'date of birth')

    def test_default_date_of_birth(self):
        author = Author.objects.get(id=2)
        date_of_birth=author.date_of_birth
        self.assertEqual(date_of_birth, datetime.date(2000,1,1))

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max=author._meta.get_field('first_name').max_length
        self.assertEqual(max, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max=author._meta.get_field('last_name').max_length
        self.assertEqual(max, 100)

    def test_str_method(self):
        author = Author.objects.get(id=1)
        expected_name='Kytheon Jura'
        self.assertEqual(str(author), expected_name)

    def test_get_absolute_url_method(self):
        author = Author.objects.get(id=1)
        expected_url='/catalog/author/1'
        self.assertEqual(author.get_absolute_url(), expected_url)
    
    def test_author_ordering(self):
        order=Author._meta.ordering
        self.assertEqual(['last_name', 'first_name'], order)

    def test_author_verbose_name(self):
        verbose_name=Author._meta.verbose_name
        self.assertEqual('Author', verbose_name)
