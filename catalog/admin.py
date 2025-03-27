from django.contrib import admin
from .models import Book, BookInstance, Language, Genre, Author

#Inline classes
class BookInline(admin.TabularInline):
    extra = 0
    model = Book

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

#Register complex configurations to the admin page
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    #The attributes to show on listing
    list_display = ('title', 'author', 'genre_display')
    
    #The inlines the page uses
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'book', 'language', 'status', 'due_back', 'borrower')
    
    #Attributes that can be filtered
    list_filter = ('status', 'due_back')
    
    #Fields for structuring the display
    fieldsets = (
        ('Info', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Avaibility', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = [ 'first_name', 'last_name', ('date_of_birth', 'date_of_death') ]
    inlines = [BookInline]

#Register simple configurations to the admin page
admin.site.register(Language)
admin.site.register(Genre)
