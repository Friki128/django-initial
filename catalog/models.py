from django.db import models
from django.urls import reverse
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint
from datetime import date
from django.conf import settings
import uuid

class Language(models.Model):
    
    #Attributes
    id=models.AutoField(primary_key=True, unique=True)
    name=models.CharField(max_length=25, unique=True)
    
    #Metadata
    class Meta:
        verbose_name="Language"
        constraints=[
            UniqueConstraint(
                Lower('name'),
                name='language-unique-name',
                violation_error_message="language already exists"
            ),
        ]

    #Methods
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

class Genre(models.Model):

    #Attributes
    id=models.AutoField(primary_key=True, unique=True)
    name=models.CharField(max_length=15, unique=True)
    
    #Metadata
    class Meta:
        verbose_name="Genre"
        constraints=[
            UniqueConstraint(
                Lower('name'),
                name="genre-unique-name",
                violation_error_message = "Genre already exists"
            ),
        ]

    #Methods
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])

class Book(models.Model):

    #Attributes
    title=models.CharField(max_length=50)
    summary=models.TextField()
    isbn=models.CharField('ISBN', max_length=13, unique=True, primary_key=True)
    author=models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    genre=models.ManyToManyField(Genre, help_text="Choose a genre")
    
    #Metadata
    class Meta:
        verbose_name="Book"

    #Methods
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.isbn)])
    
    def genre_display(self):
        return ','.join(genre.name for genre in self.genre.all())

class Author(models.Model):

    #Attributes
    id=models.AutoField(primary_key=True, unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(default="2000-01-01")
    date_of_death=models.DateField('died', null=True, blank=True)
    
    #Metadata
    class Meta:
        verbose_name="Author"
        ordering= ['last_name', 'first_name']
    
    #Methods
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])



class BookInstance(models.Model):

    #Attributes
    id=models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    book=models.ForeignKey('Book', on_delete=models.RESTRICT, null=False)
    imprint=models.CharField(max_length=200)
    due_back=models.DateField(null=True, blank=True)
    language=models.ForeignKey('Language', on_delete=models.RESTRICT, null=True)
    LOAN_STATUS=(
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Avaible'),
        ('r', 'reserved'),
    )
    status=models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m')
    borrower=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    #Metadata
    class Meta:
        verbose_name='Book Instance'
        ordering= ['due_back'] 
        permissions = (("can_mark_returned", "Set Book as Returned"),)

    #Methods
    def __str__(self):
        return f'{self.id}, {self.book.title}'
    def get_absolute_url(self):
        return reverse('BookInstance-detail', args=[str(self.id)])
    
    @property 
    def is_overdue(self):
        return bool(self.due_back and date.today()>self.due_back)
