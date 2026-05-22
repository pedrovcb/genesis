"""
Testes de autenticação: login, cadastro, navegação.
"""
import pytest
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.cadastro_page import CadastroPage
from pages.home_page import HomePage

load_dotenv(dotenv_path="../.env")

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:3000")
TEST_EMAIL = os.getenv("E2E_TEST_EMAIL", "teste_e2e@genesis.com")
TEST_PASSWORD = os.getenv("E2E_TEST_PASSWORD", "senha_teste_123")


class TestAuth:
    """Testes de autenticação."""

    def test_login_valido(self, clean_driver):
        """Test: Login com credenciais válidas leva à Home."""
        driver = clean_driver
        driver.get(BASE_URL)

        login_page = LoginPage(driver)
        login_page.enter_email(TEST_EMAIL)
        login_page.enter_password(TEST_PASSWORD)
        login_page.submit()

        # Aguarda carregamento de Home
        home_page = HomePage(driver)
        assert home_page.is_page_loaded(), "Home não foi carregada após login"

        # Verifica token em localStorage
        token = driver.execute_script("return localStorage.getItem('token')")
        assert token is not None, "Token não foi salvo em localStorage"

    def test_login_invalido(self, clean_driver):
        """Test: Login com senha errada mostra erro."""
        driver = clean_driver
        driver.get(BASE_URL)

        login_page = LoginPage(driver)
        login_page.enter_email(TEST_EMAIL)
        login_page.enter_password("senha_errada_123")
        login_page.submit()

        # Aguarda mensagem de erro
        time.sleep(2)
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Mensagem de erro não exibida"

        # Verifica que ainda está em localhost:3000 (não navegou)
        assert "localhost:3000" in driver.current_url, \
            "Usuário foi autenticado com senha errada"

    def test_login_campos_vazios(self, clean_driver):
        """Test: Submeter form vazio não navega."""
        driver = clean_driver
        driver.get(BASE_URL)

        login_page = LoginPage(driver)
        # Não preenche nada, só clica submit
        login_page.submit()

        time.sleep(1)
        # Deve estar ainda em localhost:3000
        assert "localhost:3000" in driver.current_url, \
            "Form vazio deveria não permitir submit"

    def test_cadastro_sucesso(self, clean_driver):
        """Test: Cadastro com email único redireciona para login."""
        driver = clean_driver
        driver.get(BASE_URL)

        login_page = LoginPage(driver)
        login_page.click_criar_conta()

        # Aguarda tela de cadastro
        time.sleep(2)
        cadastro_page = CadastroPage(driver)

        # Usa email único (com timestamp)
        unique_email = f"teste_{int(time.time())}@genesis.com"
        cadastro_page.enter_email(unique_email)
        cadastro_page.enter_password("senha123456")
        cadastro_page.enter_confirm_password("senha123456")
        cadastro_page.submit()

        # Aguarda redirecionar para login com mensagem
        time.sleep(2)
        login_page = LoginPage(driver)
        success_msg = login_page.get_success_message()
        assert success_msg is not None or "Conta criada" in driver.page_source, \
            "Mensagem de sucesso não exibida"

    def test_cadastro_senha_diferente(self, clean_driver):
        """Test: Senhas diferentes mostram erro."""
        driver = clean_driver
        driver.get(BASE_URL)

        login_page = LoginPage(driver)
        login_page.click_criar_conta()

        time.sleep(2)
        cadastro_page = CadastroPage(driver)

        unique_email = f"teste_{int(time.time())}@genesis.com"
        cadastro_page.enter_email(unique_email)
        cadastro_page.enter_password("senha123456")
        cadastro_page.enter_confirm_password("senha_diferente")
        cadastro_page.submit()

        # Aguarda erro
        time.sleep(1)
        error_msg = cadastro_page.get_error_message()
        assert error_msg is not None or "não" in driver.page_source.lower(), \
            "Erro de senhas diferentes não mostrado"

    def test_cadastro_volta_login(self, clean_driver):
        """Test: Clicar 'Entrar' em cadastro volta para login."""
        driver = clean_driver
        driver.get(BASE_URL)

        login_page = LoginPage(driver)
        login_page.click_criar_conta()

        time.sleep(2)
        cadastro_page = CadastroPage(driver)
        cadastro_page.click_volta_login()

        time.sleep(1)
        # Verifica que voltou para login (próximo campo deve ser email login)
        login_page = LoginPage(driver)
        assert login_page.is_submit_button_enabled(), \
            "Não voltou para página de login"
