# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

#admin.site.register(Book);
#admin.site.register(Author);
admin.site.register(Genre);
#admin.site.register(BookInstance);
admin.site.register(Language);

class BookInline(admin.TabularInline):
    model = Book;
    extra = 0;

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death');
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')];
    inlines = [BookInline];

admin.site.register(Author, AuthorAdmin);

class BookInstanceInline(admin.StackedInline): #admin.TabularInline
    model = BookInstance;
    extra = 0;

# the same as admin.site.register()
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre');
    inlines = [BookInstanceInline];

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back');
    list_display = ('book', 'status', 'due_back', 'id');
    fieldsets = (
        (None, {'fields':('book','imprint','id')}),
        ('Availability', {'fields':('status', 'due_back')}),
    );
