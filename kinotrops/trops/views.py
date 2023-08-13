from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import *
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from kinopoisk_dev import KinopoiskDev
import requests

from trops.forms import AddPostForm, RegisterUserForm, LoginUserForm
from trops.models import *
from .utils import *

menu = [{'title': "О нас", 'url_name': 'about'},
        {'title': "Лента тропов", 'url_name': 'feed_of_trops'},
        {'title': "Добавить троп", 'url_name': 'add_page'},
        {'title': "Поиск", 'url_name': 'see_q'}
]


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Что-то пошло не так! Спокуха, решаемо</h1>')

def index(request):
    trops = Trops.objects.all()
    cats = Category.objects.all()

    context = {
        'trops': trops,
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'trops/index.html', context=context)


def about(request):
    return render(request, 'trops/about.html', {'menu': menu, 'title': 'О сайте'})


def search(request):
    return render(request, 'trops/search.html', {'menu': menu, 'title': 'Поиск'})


class TropsFeedOfTrops(DataMixin, ListView):
    model = Trops
    template_name = 'trops/feed_of_trops.html'
    context_object_name = 'trops'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Лента тропов")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Trops.objects.filter(is_published=True)


class ShowTrops(DataMixin, DetailView):
    model = Trops
    template_name = 'trops/trop.html'
    slug_url_kwarg = 'trops_slug'
    context_object_name = 'trop'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['trop'])
        return dict(list(context.items()) + list(c_def.items()))


class TropsCategory(DataMixin, ListView):
    model = Trops
    template_name = 'trops/feed_of_trops.html'
    context_object_name = 'trops'
    allow_empty = False

    def get_queryset(self):
        return Trops.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['trops'][0].cat),
                                      cat_selected=context['trops'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'trops/addpage.html'
    success_url = reverse_lazy('feed_of_trops')
    login_url = reverse_lazy('index')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    return HttpResponse("Обратная связь")


#def login(request):
#   return HttpResponse("Авторизация")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'trops/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')



class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'trops/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')


# def feed_of_trops(request):
#     trops = Trops.objects.all()
#     cats = Category.objects.all()
#
#     context = {
#         'trops': trops,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Лента тропов',
#         'cat_selected': 0,
#     }
#     return render(request, 'trops/feed_of_trops.html', context=context)


# class SearchFilms(DataMixin, ListView):
#     model = Trops
#     template_name = 'trops/search.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         kinopoisk = KinopoiskDev(token='3E4DCV8-CR14QD2-KWKQGGS-6H8AFN5')
#         params = {"name": "Человек паук"}
#         response = kinopoisk.find_many_movie(params)
#         # response = kinopoisk.random()
#         # """ search_query = request.Get.get('search_film', '')
#         # response = kinopoisk.find_many_movie(search_query)"""
#         # return render(request, 'trops/films.html', {'response': response})
#         context = super().get_context_data(**kwargs)
#         return dict(list(context.items()) + list(response))
#
#
#
#     def get_queryset(self):
#         return Trops.objects.filter(is_published=True)


# class SearchFilms(DataMixin, ListView):
#     template_name = 'trops/search.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Поиск")
#         return dict(list(context.items()) + list(c_def.items()))
#
#

# def search(request):
#     q = request.GET.get('q')
#     error_msg = ''
#
#     if not q:
#         error_msg = '«Пожалуйста, введите ключевое слово»'
#         return render(request, 'trops/search.html', {'error_msg': error_msg})
#
#     kinopoisk = KinopoiskDev(token='3E4DCV8-CR14QD2-KWKQGGS-6H8AFN5')
#     params = {"name": "Человек паук"}
#     response = kinopoisk.find_many_movie(list(q))
#     return render(request, 'trops/search.html', {'error_msg': error_msg,
#                                                  'post_list': response})

class TropsFeedOfFilms(DataMixin, ListView):
    model = Trops
    template_name = 'trops/search.html'
    context_object_name = 'trops'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Поиск")
        return dict(list(context.items()) + list(c_def.items()))

    def search(self, request):
        page = 1
        limit = 3
        query = "Человек паук"
        headers = {"X-API-KEY": "3E4DCV8-CR14QD2-KWKQGGS-6H8AFN5"}
        q = request.GET.get('q')
        response = requests.get(
            'https://api.kinopoisk.dev/v1.2/movie/search',
            params={
                "query": query,
                "limit": limit,
                "page": page,
            },
            headers=headers
        )

        movies = response.json()
        return movies["docs"]


def see_q(request):
    q = request.GET.get('q')
    page = 1
    limit = 7
    query = q
    headers = {"X-API-KEY": "3E4DCV8-CR14QD2-KWKQGGS-6H8AFN5"}
    response = requests.get(
        'https://api.kinopoisk.dev/v1.2/movie/search',
        params={
            "query": query,
            "limit": limit,
            "page": page,
        },
        headers=headers
    )
    movies = response.json()
    return render(request, 'trops/see_q.html', {'movies': movies["docs"]})
