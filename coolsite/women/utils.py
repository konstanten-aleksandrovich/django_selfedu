from .models import *
from django.db.models import Count
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
class DataMixin:
    paginate_by = 2
    def get_user_comtext(self,**kwargs):
        context=kwargs
        cats = Category.objects.annotate(Count('women'))
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['cats'] = cats
        context['menu'] = user_menu
        if "cat_selected" not in context:
            context["cat_selected"]=0
        return context