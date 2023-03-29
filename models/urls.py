from django.urls import path
from . import views

from django.contrib.auth import get_user_model
User = get_user_model()

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]