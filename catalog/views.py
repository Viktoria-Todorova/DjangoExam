from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from catalog.forms import SearchForm
from catalog.models import Catalog


# Create your views here.
def search_books(request: HttpRequest)->HttpResponse:
    form = SearchForm(request.GET or None)
    books = Catalog.objects.none()

    searched_book =''

    if request.GET and form.is_valid():
        searched_book = form.cleaned_data['book_name']
        books = Catalog.objects.filter(title__icontains=searched_book)

    context = {
        'form': form,
        'books': books,
        'searched_book': searched_book,
    }
    return render(request, 'catalog/home.html',context)




#todo i want to filter them by genre
def all_books(request: HttpRequest) -> HttpResponse:
    books = Catalog.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'catalog/all_books.html', context)

#todo
def book_delete(request: HttpRequest,pk)->HttpResponse:
    #only if admin
    return render(request, 'catalog/books_delete.html', context)

def book_edit(request: HttpRequest,pk)->HttpResponse:
    #only if admin
    #add validations
    return render(request, 'catalog/books_edit.html', context)