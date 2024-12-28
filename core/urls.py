from django.urls import path,include

urlpatterns = [
    path('', include('library.urls')),
    path('accounts/', include('accounts.urls')),
]