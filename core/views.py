from django.shortcuts import render, HttpResponse#, redirect
from core.models import Evento

# Create your views here.

#def Eventos(request, titulo_evento):
#	Evento.objects.get(titulo = titulo_evento)
#	return HttpResponse('<h1>O local do evento é: {} </h1>'.format(Evento.local))


#def index(request):			
#esse método é para que o caminho especificado seja a página inicial
#	return redirect('/agenda/')

def lista_eventos(request):
	usuario = request.user
	evento = Evento.objects.all()		#aqui vai buscar um objeto na classe Evento lá no arquivo models. Ao substituir o .get(id=1) por .all() vai buscar tudo. O .filter vai filtar nesse caso os eventos daquele usuário
	dados = {'eventos':evento}			#vai passar um dicionário
	return render(request, 'agenda.html', dados)