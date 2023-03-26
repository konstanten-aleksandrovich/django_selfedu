from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseServerError
from .models import *
# Create your views here.

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

def index(request):
    posts=Women.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request,'women/index.html',context=context)
def about(request):
    return render(request,'women/about.html',{'menu':menu,'title':'О саите'})
def addpage(request):
    return HttpResponse('Добовление статьи')
def contact(request):
    return HttpResponse('Обратная связь')
def login(request):
    return HttpResponse('Авторизация')
def show_post(request,post_id):
    return HttpResponse(f'отоброжение статьи  id={post_id}')



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