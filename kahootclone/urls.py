from django.contrib import admin
from django.urls import path, include
from services import views



urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('models.urls')),
    path('services/', include('services.urls')),
    path('api/', include('restServer.urls')),
]