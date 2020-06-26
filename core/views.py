from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

#def Eventos(request, titulo_evento):
#	Evento.objects.get(titulo = titulo_evento)
#	return HttpResponse('<h1>O local do evento é: {} </h1>'.format(Evento.local))


#def index(request):			
#esse método é para que o caminho especificado seja a página inicial
#	return redirect('/agenda/')

def login_user(request):
	return render(request, 'login.html')

def logout_user(request):
	logout(request)
	return redirect('/')

def submit_login(request):
	if request.POST:
		username = request.POST.get('username') #post é o método e o .get é para recuperar um parâmetro. Nesse caso o parâmetro é username
		password = request.POST.get('password')
		usuario = authenticate(username=username, password=password)
		if usuario is not None: #se o usuário não for vazio, vai fazer o login  passando o request e o usuário. Após logar vai retornar ele para o índice/index. Quando retornar para o índice vai passar pela validação do decorador login_required, ele vai estar com a sessão aberta e vai conseguir acessar a página normalmente
			login(request, usuario)
			return redirect('/')
		else:
			messages.error(request, 'Usuário ou senha inválido.')
	return redirect('/')

@login_required(login_url='/login/') #o @ é para identificar que é um decorador. Login_url='login/' significa que quando não estiver autenticado irá direcionar para essa url
def lista_eventos(request):
	usuario = request.user
	usuario = request.user
	evento = Evento.objects.filter(usuario=usuario)		#aqui vai buscar um objeto na classe Evento lá no arquivo models. Ao substituir o .get(id=1) por .all() vai buscar tudo. O .filter vai filtar nesse caso os eventos daquele usuário
	dados = {'eventos':evento}			#vai passar um dicionário
	return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
	return render(request, 'evento.html')

@login_required(login_url='/login/')
def submit_evento(request):
	if request.POST:
		titulo = request.POST.get('titulo')
		data_evento = request.POST.get('data_evento')
		descricao = request.POST.get('descricao')
		usuario = request.user
		Evento.objects.create(titulo=titulo,		#lá na def data_eventos passou um filter
							data_evento=data_evento,#aqui usou create
							descricao=descricao,
							usuario=usuario)
	return redirect('/')