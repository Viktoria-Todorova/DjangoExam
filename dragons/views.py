from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def chose_a_dragon(request: HttpRequest,dragon_id) -> HttpResponse:
    return render(request, 'users/register-page.html', )
