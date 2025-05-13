from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
router=routers.DefaultRouter()
router.register(r'apiauthor', views.AuthorViewSet)

urlpatterns = [
    path('csrf/', views.csrf, name='csrf'),
    path('clicked/', views.clicked, name='clicked'),
    path('token/', obtain_auth_token),
    path('', include(router.urls)),
    path('index', views.index, name='index'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('book/<str:pk>', views.BookDetailView.as_view(), name='book-detail'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('loan/', views.LoanListView.as_view(), name='loan-list'),
    path('loaned/', views.LoanedListView.as_view(), name='loaned-list'),
    path('book/<uuid:pk>/renew', views.RenewBookView.as_view(), name='renew-book'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<str:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    path('book/<str:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
]
