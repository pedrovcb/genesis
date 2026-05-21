from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient
from fluxogramas.models import Fluxograma
from fluxogramas.validacao_respostas import (
    normalizar_numero,
    validar_resposta_numerica,
)

class FluxogramaListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fluxo1 = Fluxograma.objects.create(
            titulo='Protocol A',
            descricao='Description for Protocol A',
            conteudo={'steps': [{'titulo': 'Step 1'}]}
        )
        self.fluxo2 = Fluxograma.objects.create(
            titulo='Protocol B',
            descricao='Description for Protocol B',
            conteudo={'steps': [{'titulo': 'Step 2'}]}
        )
        self.fluxo3 = Fluxograma.objects.create(
            titulo='Dengue Treatment',
            descricao='Dengue fever treatment protocol',
            conteudo={'steps': []}
        )

    def test_list_all_fluxogramas(self):
        response = self.client.get('/api/fluxogramas/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['resultados']), 3)

    def test_search_by_titulo(self):
        response = self.client.get('/api/fluxogramas/?busca=Protocol%20A')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['resultados']), 1)
        self.assertEqual(data['resultados'][0]['titulo'], 'Protocol A')

    def test_search_by_descricao(self):
        response = self.client.get('/api/fluxogramas/?busca=Dengue')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['resultados']), 1)
        self.assertEqual(data['resultados'][0]['titulo'], 'Dengue Treatment')

    def test_search_case_insensitive(self):
        response = self.client.get('/api/fluxogramas/?busca=protocol%20a')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['resultados']), 1)

    def test_search_no_results(self):
        response = self.client.get('/api/fluxogramas/?busca=Nonexistent')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['resultados']), 0)

class FluxogramaDetailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fluxo = Fluxograma.objects.create(
            titulo='Protocol A',
            descricao='Description A',
            conteudo={'steps': [{'titulo': 'Step 1', 'descricao': 'Do this'}]}
        )

    def test_get_fluxograma_detail(self):
        response = self.client.get(f'/api/fluxogramas/{self.fluxo.id}/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['titulo'], 'Protocol A')
        self.assertEqual(data['id'], self.fluxo.id)
        self.assertIn('conteudo', data)
        self.assertEqual(data['conteudo']['steps'][0]['titulo'], 'Step 1')

    def test_get_nonexistent_fluxograma(self):
        response = self.client.get('/api/fluxogramas/99999/')

        self.assertEqual(response.status_code, 404)

class ValidacaoRespostaNumericaTests(SimpleTestCase):

    def test_normaliza_numero_inteiro_em_texto(self):
        resultado = normalizar_numero("10")
        self.assertEqual(str(resultado), "10")

    def test_normaliza_numero_com_ponto(self):
        resultado = normalizar_numero("10.5")
        self.assertEqual(str(resultado), "10.5")

    def test_normaliza_numero_com_virgula(self):
        resultado = normalizar_numero("10,5")
        self.assertEqual(str(resultado), "10.5")

    def test_resposta_exata_deve_ser_aceita(self):
        resultado = validar_resposta_numerica("24.2", "24.2")
        self.assertTrue(resultado["correta"])

    def test_resposta_dentro_da_tolerancia_para_cima_deve_ser_aceita(self):
        resultado = validar_resposta_numerica("10.1", "10")
        self.assertTrue(resultado["correta"])

    def test_resposta_dentro_da_tolerancia_para_baixo_deve_ser_aceita(self):
        resultado = validar_resposta_numerica("9.9", "10")
        self.assertTrue(resultado["correta"])

    def test_resposta_fora_da_tolerancia_deve_ser_rejeitada(self):
        resultado = validar_resposta_numerica("10.2", "10")
        self.assertFalse(resultado["correta"])

    def test_resposta_nao_numerica_deve_ser_rejeitada(self):
        resultado = validar_resposta_numerica("abc", "24.2")
        self.assertFalse(resultado["correta"])
        self.assertEqual(
            resultado["mensagem"],
            "A resposta precisa ser um número válido."
        )

    def test_mensagem_quando_resposta_for_menor(self):
        resultado = validar_resposta_numerica("20", "24.2")
        self.assertFalse(resultado["correta"])
        self.assertIn("abaixo", resultado["mensagem"])

    def test_mensagem_quando_resposta_for_maior(self):
        resultado = validar_resposta_numerica("30", "24.2")
        self.assertFalse(resultado["correta"])
        self.assertIn("acima", resultado["mensagem"])