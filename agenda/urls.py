"""agenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from django.views.generic import RedirectView #faz parte do path('', RedirectView.as_view(url='/agenda/'))

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('eventos/<titulo_evento>/', views.Eventos),
    path('agenda/', views.lista_eventos),
    #path('', views.index) #leva para uma view e a view te redireciona para uma url
    path('', RedirectView.as_view(url='/agenda/')) #essa é a outra forma de redirecionar a pag. inicial para uma url designada
]
