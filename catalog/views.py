from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Book, BookInstance, Genre, Language, Author
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RenewBookForm
import datetime
from django.urls import reverse_lazy
from django.forms import DateInput
from django.http import HttpResponseRedirect
#Index mapping function
def index(request):

    #Get the counts of the tables
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_avaible = BookInstance.objects.filter(status__exact='a').count() 
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_martian = Book.objects.filter(title__icontains='martian').count()
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    #Set the values to the context
    context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_avaible': num_avaible,
        'num_authors': num_authors,
        'num_martian': num_martian,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    #Return the HTML
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by=10

class AuthorListView(generic.ListView):
    model = Author
    paginate_by=10

class AuthorDetailView(generic.DetailView):
    model = Author

class BookDetailView(generic.DetailView):
    model = Book

class LoanListView(LoginRequiredMixin, generic.ListView):
    model=BookInstance
    context_object_name='loan_list'
    login_url = '/catalog/accounts/login'
    paginate_by = 10
    template_name='loan_list.html'
    def get_queryset(self):
        return(
            BookInstance.objects.filter(borrower__exact=self.request.user).filter(status__exact='o').order_by('due_back')
        )

class LoanedListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.is_librarian'
    login_url = '/catalog/accounts/login'
    paginate_by=10
    template_name='loaned_list.html'
    context_object_name='loan_list'
    model=BookInstance
    queryset=BookInstance.objects.filter(status__exact='o').order_by('due_back')

class RenewBookView(LoginRequiredMixin, generic.edit.FormView):
    login_url='/catalog/accounts/login'
    template_name='renew_book.html'
    success_url='/catalog/loan'
    form_class=RenewBookForm
    def get_initial(self):
        book_instance = get_object_or_404(BookInstance, pk=self.kwargs['pk'])
        initial = super().get_initial()
        initial['due_back'] = book_instance.due_back or datetime.date.today() + datetime.timedelta(weeks=3)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_instance = get_object_or_404(BookInstance, pk=self.kwargs['pk'])
        context['book'] = book_instance
        return context

    def form_valid(self, form):
        book_instance = get_object_or_404(BookInstance, pk=self.kwargs['pk'])
        book_instance.due_back = form.cleaned_data['due_back']
        book_instance.save()
        return super().form_valid(form)

class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.CreateView):
    permission_required='catalog.add_author'
    login_url='/catalog/accounts/login'
    fields=['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name='add.html'
    model=Author
    initial={'date_of_birth': datetime.date.today()}
    def get_form(self, form_class=None):
        form=super().get_form(form_class)
        form.fields['date_of_death'].widget=DateInput(attrs={'type': 'date'})
        form.fields['date_of_birth'].widget=DateInput(attrs={'type': 'date'})
        return form

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):
    login_url='/catalog/accounts/login'
    permission_required='catalog.change_author'
    template_name='add.html'
    fields=['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    model=Author
    def get_form(self, form_class=None):
        form=super().get_form(form_class)
        form.fields['date_of_death'].widget=DateInput(attrs={'type': 'date'})
        form.fields['date_of_birth'].widget=DateInput(attrs={'type': 'date'})
        return form


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):
    model=Author
    login_url='/catalog/accounts/login'
    permission_required='catalog.delete_author'
    template_name='author_confirm_delete.html'
    success_url=reverse_lazy('author-list')
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )

class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.CreateView):
    permission_required='catalog.add_book'
    login_url='/catalog/accounts/login'
    fields=['title', 'author', 'summary', 'genre', 'isbn']
    template_name='add.html'
    model=Book

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required='catalog.change_book'
    login_url='/catalog/accounts/login'
    template_name='add.html'
    fields=['title', 'author', 'summary', 'genre', 'isbn']
    model=Book

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required='catalog.delete_book'
    login_url='/catalog/accounts/login'
    template_name='book_confirm_delete.html'
    model=Book
    success_url=reverse_lazy('book-list')
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("book-delete", kwargs={"pk": self.object.pk})
            )

