from django.urls import path
from . import views

urlpatterns = [

    path('', views.comics_home, name='comics_home'),

    path('', views.home, name='home'),
    path('comic_list/', views.comic_list, name='comic_list'),
    path('recent/', views.recent_comics, name='recent_comics'),
    path('random/', views.random_comic, name='random_comic'),
    path('popular/', views.popular_comics, name='popular_comics'),
    path('upload_comic/', views.upload_comic, name='upload_comic'),
    path('<int:comic_id>/upload_chapter/', views.upload_chapter, name='upload_chapter'),

    path('comic/<int:comic_id>/', views.comic_detail, name='comic_detail'),
    path('comic/<int:comic_id>/chapter/<int:chapter_number>/', views.read_chapter, name='read_chapter'),

    path('search/', views.search_comics, name='search_comics'),

    path('genres/', views.comics_by_genre, name='comics_by_genre'),
    path('format/<str:format_type>/', views.comics_by_format, name='comics_by_format'),

    path('comic/<int:comic_id>/like/', views.like_comic, name='like_comic'),

    path('comic/<int:comic_id>/delete/', views.delete_comic, name='delete_comic'),
    path('comic/<int:comic_id>/chapter/<int:chapter_id>/delete/', views.delete_chapter, name='delete_chapter'),




]





