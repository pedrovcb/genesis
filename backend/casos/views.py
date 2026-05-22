from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CasoClinico, Questao, PassoRaciocinio
from .serializers import (
    CasoClinicoListSerializer,
    CasoClinicoDetailSerializer,
    PassoRaciocnioSerializer,
    ResponderSerializer
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_casos(request):
    fluxograma_id = request.GET.get('fluxograma')
    casos = CasoClinico.objects.filter(ativo=True)
    if fluxograma_id:
        casos = casos.filter(fluxograma_id=fluxograma_id)
        
    serializer = CasoClinicoListSerializer(casos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalhe_caso(request, id):
    caso = get_object_or_404(CasoClinico, id=id, ativo=True)
    serializer = CasoClinicoDetailSerializer(caso)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def responder_caso(request, id):
    caso = get_object_or_404(CasoClinico, id=id)
    serializer = ResponderSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    questao_id = serializer.validated_data['questao_id']
    resposta_usuario = str(serializer.validated_data['resposta']).strip().lower()

    questao = get_object_or_404(Questao, id=questao_id, caso_clinico=caso)
    resposta_correta_texto = str(questao.resposta_esperada).strip().lower()

    correto = resposta_usuario == resposta_correta_texto

    return Response({
        'correto': correto,
        'resposta_correta': questao.resposta_esperada,
        'mensagem': 'Resposta correta!' if correto else 'Resposta incorreta, tente novamente.'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def raciocinio_caso(request, id):
    passos = PassoRaciocinio.objects.filter(questao__caso_clinico_id=id).order_by('ordem')
    serializer = PassoRaciocnioSerializer(passos, many=True)
    return Response(serializer.data)
# Create your views here.
