from django.db import models
from django.conf import settings
from fluxogramas.models import Fluxograma


class CasoClinico(models.Model):
    NIVEL_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    contexto = models.TextField(blank=True, null=True)

    fluxograma = models.ForeignKey(
        Fluxograma,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='casos_clinicos'
    )

    nivel = models.CharField(
        max_length=20,
        choices=NIVEL_CHOICES,
        default='medio'
    )

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Questao(models.Model):
    TIPO_CHOICES = [
        ('aberta', 'Aberta'),
        ('multipla_escolha', 'Múltipla escolha'),
    ]

    caso_clinico = models.ForeignKey(
        CasoClinico,
        on_delete=models.CASCADE,
        related_name='questoes'
    )

    enunciado = models.TextField()

    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
        default='aberta'
    )

    ordem = models.PositiveIntegerField(default=1)
    resposta_esperada = models.TextField(blank=True, null=True)
    palavras_chave = models.JSONField(default=list, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem']
        unique_together = ('caso_clinico', 'ordem')

    def __str__(self):
        return f"{self.caso_clinico.titulo} - Questão {self.ordem}"


class PassoRaciocinio(models.Model):
    questao = models.ForeignKey(
        Questao,
        on_delete=models.CASCADE,
        related_name='passos_raciocinio'
    )

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    ordem = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['ordem']
        unique_together = ('questao', 'ordem')

    def __str__(self):
        return f"{self.questao} - Passo {self.ordem}"


class RespostaUsuario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='respostas_casos'
    )

    questao = models.ForeignKey(
        Questao,
        on_delete=models.CASCADE,
        related_name='respostas_usuarios'
    )

    resposta = models.TextField()
    correta = models.BooleanField(null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    pontuacao = models.IntegerField(default=0)

    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criada_em']

    def __str__(self):
        return f"{self.usuario} respondeu {self.questao}"