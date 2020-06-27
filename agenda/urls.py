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
    path('agenda/lista', views.json_lista_evento),
    path('agenda/evento/', views.evento),
    path('agenda/evento/submit', views.submit_evento),
    #path('', views.index) #leva para uma view e a view te redireciona para uma url
    path('agenda/evento/delete/<int:id_evento>/', views.delete_evento),
    path('', RedirectView.as_view(url='/agenda/')), #essa é a outra forma de redirecionar a pag. inicial para uma url designada
    path('login/', views.login_user), #não pode usar apenas views.login pq já existe uma função chamada login empacotada no contrib.auth do django
    path('login/submit', views.submit_login), #para que aconteça autenticação do usuário ao tentar logar na url login.html dos templates
    path('logout/', views.logout_user) 
]
