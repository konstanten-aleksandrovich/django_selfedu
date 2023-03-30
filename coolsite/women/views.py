from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseServerError
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import  reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name='women/index.html'
    context_object_name='posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_comtext(title = 'Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

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
class AddPage(LoginRequiredMixin,DataMixin,CreateView):
    form_class=AddPostForm
    template_name='women/addpage.html'
    success_url = reverse_lazy('home')
    login_url=reverse_lazy('home')

    def get_context_data(self,*,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']="Добовление статьи"
        c_def=self.get_user_comtext(title="Добовление статьи")
        return dict(list(context.items()) + list(c_def.items()))

class ContactFormView(DataMixin,FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self,*,object_list=None, **kwargs):
        contexst=super().get_context_data(**kwargs)
        c_def=self.get_user_comtext(title='Обратная связь')
        return dict(list(contexst.items())+list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def contact(request):
#     return HttpResponse('Обратная связь')
# def login(request):
#     return HttpResponse('Авторизация')

class ShowPost(DataMixin,DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        c_def=self.get_user_comtext(title = context['post'])
        return  dict(list(context.items()) + list(c_def.items()))

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


class WomenCategory(DataMixin,ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    allow_empty = False
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c=Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def=self.get_user_comtext(title = 'Категория - ' + str(c.name),cat_selected = c.pk)

        return dict(list(context.items()) + list(c_def.items()))

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

class RegisterUser(DataMixin,CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self,*,object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_comtext(title="Регистрация")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin,LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self,*,object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_dif=self.get_user_comtext(title='Авторизация')
        return dict(list(context.items())+list(c_dif.items()))
    def get_success_url(self):
        return reverse_lazy('home')
def logout_user(requst):
    logout(requst)
    return redirect('login')
