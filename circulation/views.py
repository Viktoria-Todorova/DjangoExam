from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta

from catalog.models import Catalog
from circulation.models import Borrowed


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
        Borrowed.objects.create(
            magician=request.user,
            book=book,
            due_date=timezone.now() + timedelta(days=25)
        )
        book.quantity -= 1
        book.save()
        return redirect('home')


class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, borrowed_id):
        borrowed = get_object_or_404(Borrowed, id=borrowed_id, magician=request.user)
        borrowed.return_date = timezone.now()
        borrowed.save()

        borrowed.book.quantity += 1
        borrowed.book.save()

        return redirect('users:profile')