from django.urls import path,include
from .import views

urlpatterns = [
    path('registration/', views.UserRagistrationView.as_view(),name='user_registration'),
    path('login/', views.UserLoginView.as_view(),name='user_login'),
    path('profile/', views.ProfileView.as_view(),name='profile'),
    path('profile_update/', views.UserAccountUpdateView.as_view(),name='profile_update'),
    path('logout/', views.UserLogoutView.as_view(),name='user_logout'),
    path('deposit/', views.DepositMoneyView.as_view(),name='deposit_money'),
    path('password_change/', views.UserPasswordChange.as_view(),name='password_change'),
]
