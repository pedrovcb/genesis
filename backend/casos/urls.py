from django.urls import path
from . import views

urlpatterns = [
    
    path('casos/', views.listar_casos, name='listar_casos'),
    path('casos/<int:id>/', views.detalhe_caso, name='detalhe_caso'),
    path('casos/<int:id>/responder/', views.responder_caso, name='responder_caso'),
    path('casos/<int:id>/raciocinio/', views.raciocinio_caso, name='raciocinio_caso'),
]