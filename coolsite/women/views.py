from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseServerError

# Create your views here.



def index(request):
    return HttpResponse('Women')

def categories(requast,catid):
    if requast.GET:
        print(requast.GET)
    return  HttpResponse(f'<h1>Статьи по категориям</h1><p>{catid}</p>')
def archive(request,year):
    if int(year)>2020:
        return redirect('home',permanent=True)
    return  HttpResponse(f'<h1>Архив по годам </h1><p>{year}</p>')
def ServerError(request):
    return HttpResponseServerError('<h1>500</h1>')
def pageNotFound(request, exception):
    print('ghjghjg')
    return HttpResponseNotFound('<h1>Строница не наидена</h1>')