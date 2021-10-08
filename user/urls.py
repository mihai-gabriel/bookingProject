from django.urls import path, include

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.ProfileView.as_view(), name="profile"),
    path('accounts/signup/', views.RegisterView.as_view(), name="register"),
]
