from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta

from catalog.models import Catalog
from circulation.forms import LoginForm
from circulation.models import Borrowed
from users.models import User


class ValidateRentABookView(LoginRequiredMixin, DetailView):
    model = Catalog
    template_name = 'circulation/rent.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'


class RentABookView(LoginRequiredMixin, FormView):
    template_name = 'circulation/log-page.html'
    form_class = LoginForm

    def get_book(self):
        return get_object_or_404(Catalog, id=self.kwargs['book_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.get_book()
        return context

    def form_valid(self, form):
        book = self.get_book()
        magician_username = form.cleaned_data['magician']
        try:
            user = User.objects.get(username=magician_username)
        except User.DoesNotExist:
            form.add_error('magician', "No user with this username exists!")
            return self.form_invalid(form)

        Borrowed.objects.create(magician=user, book=book, due_date=timezone.now() + timedelta(days=25))
        book.quantity -= 1
        book.save()
        return redirect('home')