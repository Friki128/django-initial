from django.test import TestCase
from django.urls import reverse
from catalog.models import Author, Book, Genre, Language, BookInstance
from django.utils import timezone
import datetime
import uuid
from catalog.forms import RenewBookForm
from django.contrib.auth import get_user_model
User = get_user_model()

class AuthorListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors=15
        for id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Author {id}',
                last_name=f'Surname {id}',
            )

    def test_url_exist_at_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)

    def test_url_uses_correct_template(self):
        response = self.client.get(reverse('author-list'))
        self.assertTemplateUsed(response, 'catalog/author_list.html')
    
    def test_pagination_ammount(self):
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated']==True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_list_all_authors(self):
        response = self.client.get(reverse('author-list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated']==True)
        self.assertEqual(len(response.context['author_list']), 5)

class BookListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_books=15
        for id in range(number_of_books):
            Book.objects.create(
                title=f'Title {id}',
                summary=f'summary {id}',
                isbn=f'{id}',
                author=None,
            )

    def test_url_exist_at_location(self):
        response = self.client.get('/catalog/books/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, 200)

    def test_url_uses_correct_template(self):
        response = self.client.get(reverse('book-list'))
        self.assertTemplateUsed(response, 'catalog/book_list.html')
    
    def test_pagination_ammount(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated']==True)
        self.assertEqual(len(response.context['book_list']), 10)

    def test_list_all_books(self):
        response = self.client.get(reverse('book-list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated']==True)
        self.assertEqual(len(response.context['book_list']), 5)

class LoanListTest(TestCase):
    def setUp(self):
        user1=User.objects.create_user(username='user1', password='abcdefghi')
        user2=User.objects.create_user(username='user2', password='abcdefghi')
        user1.save()
        user2.save()

        author1=Author.objects.create(first_name='Kytheon', last_name='Jura')
        genre1=Genre.objects.create(name='Fantasy')
        language1=Language.objects.create(name='English')
        book1=Book.objects.create(title='War of The Spark', summary='Nicol Bolas attacks', isbn='abcd', author=author1)
        genre_book=Genre.objects.all()
        book1.genre.set(genre_book)
        book1.save()

        number_of_books = 30
        for copy in range(number_of_books):
            return_date=timezone.localtime()+datetime.timedelta(days=copy%5)
            borrower=user1 if copy%2==0 else user2
            status='m'
            BookInstance.objects.create(book=book1, imprint='Generic Imprint', status=status, borrower=borrower, due_back=return_date)

    def test_redirect_if_not_logged(self):
        response=self.client.get(reverse('loan-list'), follow=True)
        self.assertRedirects(response, '/catalog/accounts/login/?next=/catalog/loan/')
    
    def test_correct_template(self):
        login=self.client.login(username='user1', password='abcdefghi')
        response=self.client.get(reverse('loan-list'))
        self.assertEqual('user1', str(response.context['user']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loan_list.html')

    def test_only_borrowed_books(self):
        login=self.client.login(username='user1', password='abcdefghi')
        response=self.client.get(reverse('loan-list'))
        self.assertEqual('user1', str(response.context['user']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('loan_list' in response.context)
        self.assertEqual(len(response.context['loan_list']),0)

        books=BookInstance.objects.all()[:20]
        for book in books:
            book.status = 'o'
            book.save()

        response=self.client.get(reverse('loan-list'))
        self.assertEqual(len(response.context['loan_list']), 10)
        for book in response.context['loan_list']:
            self.assertEqual(book.status, 'o')
            self.assertEqual(book.borrower, response.context['user'])

    def test_pages_ordered_by_due_back(self):
        for book in BookInstance.objects.all():
            book.status='o'
            book.save()
        login=self.client.login(username='user1', password='abcdefghi')
        response = self.client.get(reverse('loan-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('loan_list' in response.context)
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(len(response.context['loan_list']), 10)
        date=0
        for book in response.context['loan_list']:
            if date==0:
                date=book.due_back
            else:
                self.assertTrue(date <= book.due_back)
                date=book.due_back

    def test_pagination_all_books(self): 
        for book in BookInstance.objects.all():
            book.status='o'
            book.save()
        login=self.client.login(username='user1', password='abcdefghi')
        response = self.client.get(reverse('loan-list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('loan_list' in response.context)
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(len(response.context['loan_list']), 5)

class RenewBookFormViewList(TestCase):
    def setUp(self):
        user1=User.objects.create_user(username='user1', password='abcdefghi')
        user2=User.objects.create_user(username='user2', password='abcdefghi')
        user1.save()
        user2.save()
        author1=Author.objects.create(first_name='Kytheon', last_name='Jura')
        genre1=Genre.objects.create(name='Fantasy')
        language1=Language.objects.create(name='English')
        book1=Book.objects.create(title='War of The spark', summary='Nicol Bolas attacks', isbn='AAAA', author=author1)
        genre_book=Genre.objects.all()
        book1.genre.set(genre_book)
        book1.save()

        self.book_instance1=BookInstance.objects.create(
            book=book1,
            status='o',
            borrower=user1,
            imprint='Generic Imprint'
        )
        self.book_instance2=BookInstance.objects.create(
            status='o',
            imprint='Generic Imprint',
            borrower=user2,
            book=book1
        )

    def test_redirect_if_not_logged(self):
        response=self.client.get(reverse('renew-book', kwargs={'pk': self.book_instance1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/accounts/login'))

    def test_logged_in_status_200(self):
        login=self.client.login(username='user1', password='abcdefghi')
        response=self.client.get(reverse('renew-book', kwargs={'pk': self.book_instance1.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        login=self.client.login(username='user1', password='abcdefghi')
        response=self.client.get(reverse('renew-book', kwargs={'pk': self.book_instance1.pk}))
        self.assertTemplateUsed(response, 'renew_book.html')

    def test_404_on_invalid_book_pk(self):
        test_uuid=uuid.uuid4()
        login=self.client.login(username='user1', password='abcdefghi')
        response=self.client.get(reverse('renew-book', kwargs={'pk': test_uuid}))
        self.assertEqual(response.status_code, 404)

    def test_date_correct_initial_value(self):
        login=self.client.login(username='user1', password='abcdefghi')
        response=self.client.get(reverse('renew-book', kwargs={'pk': self.book_instance1.pk}))
        expected_date=datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(expected_date, response.context['form'].initial['due_back'])
    
    def test_redirect_on_success(self):
        login=self.client.login(username='user1', password='abcdefghi')
        valid_date=datetime.date.today() + datetime.timedelta(weeks=2)
        response=self.client.post(reverse('renew-book', kwargs={'pk': self.book_instance1.pk}), {'due_back': valid_date}, follow=True)
        self.assertRedirects(response, '/catalog/loan/')
    
    def test_date_too_far_in_future(self):
        login=self.client.login(username='user1', password='abcdefghi')
        invalid_date=datetime.date.today() + datetime.timedelta(weeks=5)
        response=self.client.post(reverse('renew-book', kwargs={'pk': self.book_instance1.pk}), {'due_back': invalid_date})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'due_back', 'The date is too far in the future')
    def test_date_in_the_past(self):
        login=self.client.login(username='user1', password='abcdefghi')
        invalid_date=datetime.date.today() - datetime.timedelta(days=1)
        response=self.client.post(reverse('renew-book', kwargs={'pk': self.book_instance1.pk}), {'due_back': invalid_date})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'due_back', 'The date cannot be in the past')
        

