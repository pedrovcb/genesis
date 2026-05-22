from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object para tela de login."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_email(self, email):
        """Entra com email no input."""
        email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]')
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        """Entra com senha no input."""
        pwd_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        pwd_input.clear()
        pwd_input.send_keys(password)

    def submit(self):
        """Clica no botão de login."""
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, '.login-btn-entrar')
        submit_btn.click()

    def click_criar_conta(self):
        """Clica no botão 'Criar Conta'."""
        btn = self.driver.find_element(By.CSS_SELECTOR, '.login-link-button')
        btn.click()

    def get_error_message(self):
        """Retorna mensagem de erro, se existir."""
        try:
            error = self.driver.find_element(By.CSS_SELECTOR, '.login-error, .error')
            return error.text
        except:
            return None

    def get_success_message(self):
        """Retorna mensagem de sucesso, se existir."""
        try:
            success = self.driver.find_element(By.CSS_SELECTOR, '.login-success')
            return success.text
        except:
            return None

    def is_submit_button_enabled(self):
        """Retorna se botão de submit está habilitado."""
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, '.login-btn-entrar')
        return submit_btn.is_enabled()
