from rest_framework import serializers
from .models import CasoClinico, Questao, PassoRaciocinio

class QuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questao
        fields = ['id', 'enunciado', 'tipo', 'ordem']

class CasoClinicoDetailSerializer(serializers.ModelSerializer):
    questoes = QuestaoSerializer(many=True, read_only=True)

    class Meta:
        model = CasoClinico
        fields = ['id', 'titulo', 'descricao', 'contexto', 'nivel', 'questoes']

class CasoClinicoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CasoClinico
        fields = ['id', 'titulo', 'descricao', 'nivel']

class PassoRaciocnioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassoRaciocinio
        fields = ['id', 'titulo', 'descricao', 'ordem']

class ResponderSerializer(serializers.Serializer):
    questao_id = serializers.IntegerField()
    resposta = serializers.CharField()