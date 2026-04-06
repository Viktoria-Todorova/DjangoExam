from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect

from catalog.models import Catalog
from circulation.models import Borrowed
from circulation.tasks import process_book_rental, process_book_return


class RulesView(LoginRequiredMixin, DetailView):
    model = Catalog
    template_name = 'circulation/log-page.html'  # rules page
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'


class ValidateRentABookView(LoginRequiredMixin, DetailView):
    model = Catalog
    template_name = 'circulation/rent.html'  # confirmation page
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'


class RentABookView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Catalog, id=book_id)
        
        # Queue rental processing asynchronously
        process_book_rental.delay(request.user.id, book_id)
        
        return redirect('home')


class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, borrowed_id):
        borrowed = get_object_or_404(Borrowed, id=borrowed_id, magician=request.user)
        
        # Queue return processing asynchronously
        process_book_return.delay(borrowed_id)
        
        return redirect('users:profile')