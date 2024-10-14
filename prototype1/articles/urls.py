from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:id>/', views.article_detail, name='article_detail'),
    path('add/', views.add_article, name='add_article'),
    path('article/<int:article_id>/delete/', views.delete_article, name='delete_article'),

]


