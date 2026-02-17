from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest,HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView

from catalog.forms import SearchForm, GenreFilterForm, BooksForm, DeleteBookForm
from catalog.models import Catalog


class SearchBooksView(ListView):
    model = Catalog
    template_name = 'catalog/home.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Catalog]:
        form = SearchForm(self.request.GET)

        if form.is_valid():
            searched_book = form.cleaned_data.get('book_name')
            if searched_book:
                return Catalog.objects.filter(title__icontains=searched_book)

        return Catalog.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        context['searched_book'] = self.request.GET.get('book_name', '')
        return context


class AllBooksView(ListView):
    model = Catalog
    template_name = 'catalog/all_books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Catalog]:
        qs = Catalog.objects.all()
        form = GenreFilterForm(self.request.GET)

        if form.is_valid():
            genre = form.cleaned_data.get('genre')
            if genre:
                qs = qs.filter(genre=genre)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GenreFilterForm(self.request.GET)
        return context
# # Create your views here.
# def search_books(request: HttpRequest)->HttpResponse:
#     form = SearchForm(request.GET or None)
#     books = Catalog.objects.none()
#
#     searched_book =''
#
#     if request.GET and form.is_valid():
#         searched_book = form.cleaned_data['book_name']
#         books = Catalog.objects.filter(title__icontains=searched_book)
#
#     context = {
#         'form': form,
#         'books': books,
#         'searched_book': searched_book,
#     }
#     return render(request, 'catalog/home.html',context)
#
#
#
#
# #todo i want to filter them by genre
# def all_books(request: HttpRequest) -> HttpResponse:
#     form = GenreFilterForm(request.GET or None)
#     books = Catalog.objects.all()
#     if form.is_valid():
#         genre = form.cleaned_data['genre']
#         if genre:
#             books = books.filter(genre=genre)
#     context = {
#         'books': books,
#         'form': form,
#     }
#     return render(request, 'catalog/all_books.html', context)


class CatalogListView(ListView):
    paginate_by = 10

    def get_queryset(self)->QuerySet[Catalog]:
        qs = Catalog.objects.all()

        book_genre = self.request.GET.get('book_genre')
        if book_genre:
            if book_genre not in Catalog.Genre.choices.labels:
                raise HttpResponseBadRequest

        qs =qs.filter(genre=book_genre)
        return qs


class BookDetailView(DetailView):
    model = Catalog
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'




class BookEditView(UpdateView):
    model = Catalog
    form_class = BooksForm
    template_name = 'catalog/book_edit.html'

    def get_success_url(self) -> str:
        return reverse('book_detail',
                       kwargs={'pk': self.object.pk})

#todo
# def book_delete(request: HttpRequest,pk)->HttpResponse:
#     #only if admin
#     return render(request, 'catalog/books_delete.html', context)


class BookDeleteView(DeleteView):
    model = Catalog
    # form_class = DeleteBookForm
    template_name = 'catalog/book_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DeleteBookForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = DeleteBookForm(instance=self.object)

        self.object.delete()

        return render(request, "catalog/book_confirm_delete.html", {
            "form": form
        })


# def book_edit(request: HttpRequest,pk)->HttpResponse:
#     #only if admin
#     #add validations
#     return render(request, 'catalog/books_edit.html', context)