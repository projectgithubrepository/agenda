from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.

class Evento(models.Model):
	titulo = models.CharField(max_length=100) 				#vai ter no máx 100 caracteres
	descricao = models.TextField(blank=True, null=True)		#o título não pode ser em branco, mas a descrição pode. Por isso colocou blank = true
	data_evento = models.DateTimeField(verbose_name='Data do Evento')	
	#data evento não pode ser nulo, por isso fica assim
	data_criacao = models.DateTimeField(auto_now=True)		#data que o usuário inseriu esse evento no meu banco. Esse dado tem que ser automático, não pode deixar o usuário alterar. Para saber quando foi feita a inserção. auto_now = sempre que for criado um registro ele automaticamente vai inserir a data/hora atual.
	usuario = models.ForeignKey(User, on_delete=models.CASCADE) #para que seja multiusuário. Não vou criar uma tabela de usuários. Vou usar a do django. on_delete é o que fazer com os dados quando aquele usuário for deletado? models.CASCADE apaga tudo daquele usuário
	local = models.CharField(max_length=100, blank=True, null=True)

	class Meta:
		db_table = 'evento'

	def __str__(self):		#esse método trata o nome dos eventos adicionados p/ igual o título
		return self.titulo

#datetime-local não tem compatiblidade no firefox, ou seja, essa funcionalidade não funciona. Vai apenas aparecer como um input de texto
	
	def get_data_evento(self):
		return self.data_evento.strftime('%d/%m/%Y %H:%M hr')

	def get_data_input_evento(self): 
		#return self.data_evento.strftime('%Y-%m-%dT%H:%M')
		return self.data_evento.strftime('%Y-%m-%d %H:%M')
	
	def get_evento_atrasado(self):
		if self.data_evento < datetime.now():
			return True
		else:
			return False