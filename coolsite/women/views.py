from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Women')

def categories(requast):
    return  HttpResponse('<h1>Статьи по категориям<h1>')