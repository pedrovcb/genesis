from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CadastroPage:
    """Page Object para tela de cadastro/registro."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_email(self, email):
        """Entra com email no input."""
        inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="email"]')
        if inputs:
            inputs[0].clear()
            inputs[0].send_keys(email)

    def enter_password(self, password):
        """Entra com senha no input."""
        pwd_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="password"]')
        if pwd_inputs:
            pwd_inputs[0].clear()
            pwd_inputs[0].send_keys(password)

    def enter_confirm_password(self, password):
        """Entra com confirmação de senha."""
        pwd_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="password"]')
        if len(pwd_inputs) > 1:
            pwd_inputs[1].clear()
            pwd_inputs[1].send_keys(password)

    def submit(self):
        """Clica botão 'Cadastrar'."""
        # Encontra botão que contém texto 'Cadastrar'
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        for btn in buttons:
            if 'Cadastrar' in btn.text or 'Cadastrando' in btn.text:
                btn.click()
                return

    def click_volta_login(self):
        """Clica no botão 'Entrar' para voltar ao login."""
        # Procura por link/button com texto 'Entrar'
        elements = self.driver.find_elements(By.TAG_NAME, 'button')
        for elem in elements:
            if 'Entrar' in elem.text:
                elem.click()
                return

    def get_error_message(self):
        """Retorna mensagem de erro, se existir."""
        try:
            error = self.driver.find_element(By.CSS_SELECTOR, '.error')
            return error.text
        except:
            return None
