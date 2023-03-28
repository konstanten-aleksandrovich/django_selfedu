from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseServerError
from django.views.generic import ListView,DetailView,CreateView
from django.urls import  reverse_lazy

from .models import *
from .forms import *
# Create your views here.

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
class WomenHome(ListView):
    model = Women
    template_name='women/index.html'
    context_object_name='posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        context['menu'] = menu
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True)

# def index(request):
#     posts=Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request,'women/index.html',context=context)


def about(request):
    return render(request,'women/about.html',{'menu':menu,'title':'О саите'})
# def addpage(request):
#     if request.method=='POST':
#         form = AddPostForm(request.POST,request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form=AddPostForm()
#     return  render(request,'women/addpage.html',{'form':form,'menu':menu,'title':'Добовление статьи'})
class AddPage(CreateView):
    form_class=AddPostForm
    template_name='women/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self,*,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']="Добовление статьи"
        context['menu']=menu
        return context

def contact(request):
    return HttpResponse('Обратная связь')
def login(request):
    return HttpResponse('Авторизация')

class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

# def show_post(request,post_slug):
#     post=get_object_or_404(Women,slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_slug
#     }
#
#     return render(request,'women/post.html',context=context)


class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    allow_empty = False
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context

# def show_category(request,cat_slug):
#     posts =Women.objects.filter(cat__slug=cat_slug)
#     print(posts)
#     if not len(posts):
#         raise Http404
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отоброжение по рубрикам',
#         'cat_selected': cat_slug,
#     }
#     return render(request, 'women/index.html', context=context)



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