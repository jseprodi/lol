from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
] 