from django.db.models import Count

from .models import *

menu = [{'title': "О нас", 'url_name': 'about'},
        {'title': "Лента тропов", 'url_name': 'feed_of_trops'},
        {'title': "Добавить троп", 'url_name': 'add_page'},
        {'title': "Поиск", 'url_name': 'see_q'},
]


class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('trops'))

        # user_menu = menu.copy()
        # if not self.request.user.is_authenticated:
        #     user_menu.pop(3) #в словаре menu удаляется вкладка добавления статьи

        context['menu'] = menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
