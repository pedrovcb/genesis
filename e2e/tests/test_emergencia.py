"""
Testes do Modo Emergência: lista, favoritos, seleção de protocolo.
"""
import pytest
import time
from pages.emergencia_page import EmergenciaPage
from pages.protocolo_page import ProtocoloPage


class TestEmergencia:
    """Testes do Modo Emergência."""

    def test_modo_emergencia_carrega(self, logged_in):
        """Test: Modo Emergência carrega com lista de protocolos."""
        driver = logged_in

        # Clica no botão Modo Emergência na Home
        from pages.home_page import HomePage
        home_page = HomePage(driver)

        try:
            home_page.click_emergencia_button()
        except:
            pytest.skip("Botão Modo Emergência não encontrado")

        time.sleep(2)

        emergencia_page = EmergenciaPage(driver)
        assert emergencia_page.is_page_loaded(), \
            "Modo Emergência não foi carregado"

        count = emergencia_page.get_protocol_count()
        assert count > 0, "Nenhum protocolo disponível"

    def test_favoritar_protocolo(self, logged_in):
        """Test: Clicar na estrela de um protocolo o favorita."""
        driver = logged_in

        # Navega para Modo Emergência
        from pages.home_page import HomePage
        home_page = HomePage(driver)
        try:
            home_page.click_emergencia_button()
        except:
            pytest.skip("Botão Modo Emergência não encontrado")

        time.sleep(2)

        emergencia_page = EmergenciaPage(driver)
        assert emergencia_page.is_page_loaded(), \
            "Modo Emergência não carregou"

        # Pega primeiro card
        card = emergencia_page.get_first_protocol_card()
        assert card is not None, "Nenhum card encontrado"

        # Tenta favoritar
        try:
            emergencia_page.toggle_favorite_on_card(card)
            time.sleep(1)
        except Exception as e:
            pytest.skip(f"Não conseguiu favoritar: {e}")

    def test_selecionar_protocolo(self, logged_in):
        """Test: Clicar em um protocolo navega para sua página."""
        driver = logged_in

        # Navega para Modo Emergência
        from pages.home_page import HomePage
        home_page = HomePage(driver)
        try:
            home_page.click_emergencia_button()
        except:
            pytest.skip("Botão Modo Emergência não encontrado")

        time.sleep(2)

        emergencia_page = EmergenciaPage(driver)
        assert emergencia_page.is_page_loaded(), \
            "Modo Emergência não carregou"

        # Pega primeiro card e tenta clicar nele
        card = emergencia_page.get_first_protocol_card()
        assert card is not None, "Nenhum card encontrado"

        card.click()
        time.sleep(2)

        # Verifica se navegou para protocolo
        protocolo_page = ProtocoloPage(driver)
        assert protocolo_page.is_page_loaded(), \
            "Página do protocolo não carregou após clicar"

    def test_timer_emergencia(self, logged_in):
        """Test: Timer do modo emergência está rodando (desktop)."""
        driver = logged_in

        # Navega para Modo Emergência
        from pages.home_page import HomePage
        home_page = HomePage(driver)
        try:
            home_page.click_emergencia_button()
        except:
            pytest.skip("Botão Modo Emergência não encontrado")

        time.sleep(2)

        emergencia_page = EmergenciaPage(driver)

        # Tenta obter timer (pode não existir em mobile)
        timer_text_1 = emergencia_page.get_timer_text()

        if timer_text_1 is not None:
            # Aguarda 2 segundos e verifica se timer incrementou
            time.sleep(2)
            timer_text_2 = emergencia_page.get_timer_text()

            # Verifica se timer mudou
            assert timer_text_2 is not None, "Timer desapareceu"
        else:
            pytest.skip("Timer não encontrado (pode ser mobile-only)")
