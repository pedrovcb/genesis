import os
import pytest
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage

load_dotenv(dotenv_path="../.env")

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:3000")
API_BASE_URL = os.getenv("E2E_API_URL", "http://localhost:8000/api")
TEST_EMAIL = os.getenv("E2E_TEST_EMAIL", "teste_e2e@genesis.com")
TEST_PASSWORD = os.getenv("E2E_TEST_PASSWORD", "senha_teste_123")


@pytest.fixture(scope="session", autouse=True)
def setup_test_user():
    """Cria user de teste se não existir."""
    try:
        # Tenta cadastrar user de teste
        response = requests.post(
            f"{API_BASE_URL}/auth/cadastro/",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD,
                "confirmPassword": TEST_PASSWORD
            },
            timeout=5
        )
        if response.status_code == 201:
            print(f"\nUser teste criado: {TEST_EMAIL}")
        elif response.status_code == 400:
            # User já existe
            print(f"\nUser teste já existe: {TEST_EMAIL}")
        else:
            print(f"\nAviso ao criar user: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"\nNao conseguiu criar user teste: {e}")
        print("Verifique se backend esta rodando em " + API_BASE_URL)


@pytest.fixture(scope="session")
def driver():
    """Cria driver Firefox headless para toda a sessão."""
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--width=1280")
    options.add_argument("--height=1024")

    drv = webdriver.Firefox(
        service=Service("/usr/local/bin/geckodriver"),
        options=options
    )

    drv.implicitly_wait(10)
    yield drv
    drv.quit()


@pytest.fixture
def logged_in(driver):
    """Fixa driver já autenticado na página Home."""
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    login_page.enter_email(TEST_EMAIL)
    login_page.enter_password(TEST_PASSWORD)
    login_page.submit()

    # Espera Home carregar
    WebDriverWait(driver, 10).until(
        lambda d: "http://localhost:3000" in d.current_url
    )

    yield driver

    # Limpa estado
    driver.execute_script("localStorage.clear()")


@pytest.fixture
def clean_driver(driver):
    """Limpa localStorage antes de cada teste."""
    try:
        driver.execute_script("localStorage.clear()")
    except Exception:
        pass  # Ignora erro de localStorage em página em branco
    driver.delete_all_cookies()
    yield driver
