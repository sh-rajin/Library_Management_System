from django.urls import path,include
from .import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='home'),
    path('book_detail/<int:id>', views.BookDetailView.as_view(), name='book_detail'),
    path('borrow/<int:id>/', views.BorrowBookView.as_view(), name='borrow_book'),
    path('return/<int:id>/', views.ReturnBookView.as_view(), name='return_book'),
    path('category/<slug:category_slug>/', views.BookListView.as_view(), name = 'category_wise_book'),
]
