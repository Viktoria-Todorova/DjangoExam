from django.db.models import QuerySet
from django.http import HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView

from catalog.forms import SearchForm, GenreFilterForm, BooksForm, DeleteBookForm
from catalog.mixins import AdminRequiredMixin
from catalog.models import Catalog

class HomePageView(ListView):
    model = Catalog
    template_name = 'home.html'

class SearchBooksView(ListView):
    model = Catalog
    template_name = 'catalog/search_book.html'
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




class BookEditView(AdminRequiredMixin,UpdateView):
    model = Catalog
    form_class = BooksForm
    template_name = 'catalog/book_edit.html'


    def get_success_url(self) -> str:
        return reverse('book_detail',
                       kwargs={'pk': self.object.pk})



class BookDeleteView(AdminRequiredMixin,DeleteView):
    model = Catalog
    template_name = 'catalog/book_delete.html'
    success_url = reverse_lazy('home')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DeleteBookForm(instance=self.object)
        return context

