from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse #tratamento de erros

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
	data_atual = datetime.now() - timedelta(hours=1) #aparece os eventos até 1 hora depois (em que já esteja atrasado) 
	evento = Evento.objects.filter(usuario=usuario,
									data_evento__gt=data_atual)		
									#aqui vai buscar um objeto na classe Evento lá no arquivo models. 
									#Ao substituir o .get(id=1) por .all() vai buscar tudo. O .filter vai filtar nesse caso os eventos daquele usuário.
									# __gt significa = se o campo, nesse caso data_evento, for maior que o data_atual, você retorna. __lt para quando o campo for menor que o data_atual. Ou seja, filtra os eventos antes ou depois da data atual. Pq esse comando? pq o python nesse caso não aceita usar sinal > ou <.
	dados = {'eventos':evento}			#vai passar um dicionário
	return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
	id_evento = request.GET.get('id')
	dados = {}
	if id_evento:
		dados['evento'] = Evento.objects.get(id=id_evento)
	return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
	if request.POST:
		titulo = request.POST.get('titulo')
		data_evento = request.POST.get('data_evento')
		descricao = request.POST.get('descricao')
		usuario = request.user
		local = request.POST.get('local')
		id_evento = request.POST.get('id_evento')
		if id_evento: 				#para atualizar o evento e não apenas criar outro
			evento = Evento.objects.get(id=id_evento)
			if evento.usuario == usuario:		
				evento.titulo = titulo
				evento.descricao = descricao
				evento.data_evento = data_evento
				evento.local = local
				evento.save()

#outro forma de atualizar o evento
		#if id_evento:
		#Evento.objects.filter(id=id_evento).update(titulo=titulo,		
			#										data_evento=data_evento,#aqui usou create
			#										descricao=descricao,
			#										local=local) #não precisa mexer no usuário, pois ele se mantém igual
		else:
			Evento.objects.create(titulo=titulo,		#lá na def data_eventos passou um filter
							data_evento=data_evento,#aqui usou create
							descricao=descricao,
							usuario=usuario, local=local)
	return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
	#Evento.objects.filter(id=id_evento).delete()	#nessa linha fica possível outra pessoa ver o código e até apagar os dados de um outro usuário. 
	usuario = request.user
	try:		#tratamento de erro para quando acessa alguma coisa que não existe (exemplo um url digitada errado)				
		evento = Evento.objects.get(id=id_evento)
	except Exception:
		raise Http404()
	if usuario == evento.usuario:
		evento.delete()				#pronto. Agora não é mais possível esse acesso não desejado
	else:
		raise Http404()
	return redirect('/') #redirect para a página principal, index/índice

@login_required(login_url='/login/')
def json_lista_evento(request):
	usuario = request.user
	evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')		
	#dados = {'eventos':evento}			#não precisa dos dados, vai retornar direto um eventodata
	return JsonResponse(list(evento), safe=False)

#vamos supor que vc queira passar para uma aplicação externa. Uma API mesmo. Para que alguém acesse a sua agenda numa outra aplicação, uma outra pessoa.
#formas de integração entre aplicações 
# 1) tira o @login_required do json_lista_evento
# 2) vai mudar o path para path('agenda/lista/<int:id_usuario>/', views.json_lista_evento),
# 3) incluir o id_usuario no json_lista_evento(request, id_usuario):
# 4) incluir nos imports o 'from django.contrib.auth.models import user'
# 5) usuario = User.object.get(id=id_usuario)
#ou seja, ao invés de pegar da requisição e requerer o login eu posso simplesmente disponibilizar uma API pública ou não, ou procurar outras formas
#pode, por exemplo, criar uma função que não requer login e retorne esse Json aqui
#para trabalhar com JavaScript o JsonResponse é muito bom