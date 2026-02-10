
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>/', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book'),
    path('search/', views.search, name='search'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('mybooks/', views.MyBookInstanceListView.as_view(), name='mybooks'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
