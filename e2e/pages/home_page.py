from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    """Page Object para tela Home."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_page_loaded(self):
        """Verifica se página Home foi carregada."""
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mobile-frame')))
            return True
        except:
            return False

    def get_page_title(self):
        """Retorna título/logo visível."""
        try:
            title = self.driver.find_element(By.TAG_NAME, 'h1')
            return title.text
        except:
            return None

    def search_protocol(self, query):
        """Digita na barra de busca."""
        search_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        if search_inputs:
            search_input = search_inputs[0]
            search_input.clear()
            search_input.send_keys(query)

    def get_search_results(self):
        """Retorna resultados da busca (elementos do dropdown)."""
        try:
            # Aguarda o dropdown aparecer
            results = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class*="dropdown"], [class*="result"]'))
            )
            return results
        except:
            return []

    def click_emergencia_button(self):
        """Clica no botão 'Modo Emergência'."""
        # Tenta múltiplos seletores
        try:
            # Tenta por aria-label
            btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Emergência"], button[aria-label*="emergencia"]')
            btn.click()
            return
        except:
            pass

        # Tenta por texto
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        for btn in buttons:
            text = btn.text.strip()
            if any(word in text.lower() for word in ['emergência', 'emergencia', 'emergência']):
                if 'disabled' not in btn.get_attribute('class'):
                    btn.click()
                    return

        raise Exception("Botão Modo Emergência não encontrado ou desabilitado")

    def is_emergencia_button_enabled(self):
        """Verifica se botão emergência está habilitado."""
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Emergência"], button[aria-label*="emergencia"]')
            return btn.is_enabled()
        except:
            pass

        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        for btn in buttons:
            text = btn.text.strip()
            if any(word in text.lower() for word in ['emergência', 'emergencia']):
                return 'disabled' not in btn.get_attribute('class')
        return False
