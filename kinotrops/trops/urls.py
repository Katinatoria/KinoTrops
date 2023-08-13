from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('feed_of_trops/', TropsFeedOfTrops.as_view(), name='feed_of_trops'),
    path('feed_of_trops/<slug:trops_slug>/', ShowTrops.as_view(), name='trops'),
    path('category/<slug:cat_slug>/', TropsCategory.as_view(), name='category'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('search/', TropsFeedOfFilms.as_view(), name='search'),
    path('see_q/', see_q, name='see_q'),
]