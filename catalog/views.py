# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count();
    num_instances = BookInstance.objects.all().count();
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count();
    num_authors = Author.objects.count(); # The 'all()' is implied by default.
    num_genres = Genre.objects.count();
    num_book_test = Book.objects.filter(title__contains='test').count();

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0);
    request.session['num_visits'] = num_visits + 1;

    CONTEXT = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'num_book_test':num_book_test,
        'num_visits':num_visits,
    };
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context=CONTEXT
    );

class BookListView(generic.ListView):
    model = Book;
    paginate_by = 10;

class BookDetailView(generic.DetailView):
    model = Book;

class AuthorListView(generic.ListView):
    model = Author;
    paginate_by = 10;

class AuthorDetailView(generic.DetailView):
    model = Author;

# implementation by function
'''
def book_detail_view(request,pk):
    try:
        book_id=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    #book_id=get_object_or_404(Book, pk=pk)
    
    return render(
        request,
        'catalog/book_detail.html',
        context={'book':book_id,}
    )
'''

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance;
    template_name = 'catalog/bookinstance_list_borrowed_user.html';
    paginate_by = 10;

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back');

class LoanedBooksByLabrarianListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance;
    permission_required = 'catalog.can_mark_returned';
    template_name = 'catalog/bookinstance_list_loaned_librarian.html';
    paginate_by = 20;

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back');

