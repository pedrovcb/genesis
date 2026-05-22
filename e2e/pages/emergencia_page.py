from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EmergenciaPage:
    """Page Object para Modo Emergência."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_page_loaded(self):
        """Verifica se página Emergência foi carregada."""
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.protocol-list')))
            return True
        except:
            return False

    def get_protocol_cards(self):
        """Retorna lista de cards de protocolo."""
        return self.driver.find_elements(By.CSS_SELECTOR, '.protocol-card')

    def get_protocol_count(self):
        """Retorna quantidade de protocolos disponíveis."""
        cards = self.get_protocol_cards()
        return len(cards)

    def click_protocol_by_name(self, protocol_name):
        """Clica em protocolo pelo nome."""
        cards = self.get_protocol_cards()
        for card in cards:
            if protocol_name in card.text:
                card.click()
                return True
        return False

    def get_first_protocol_card(self):
        """Retorna primeiro card de protocolo."""
        cards = self.get_protocol_cards()
        if cards:
            return cards[0]
        return None

    def toggle_favorite_on_card(self, card_element):
        """Clica no ícone de favorito (estrela) de um card."""
        # Tenta múltiplos seletores
        try:
            # Tenta por classe que contenha star ou favorite
            star = card_element.find_element(By.CSS_SELECTOR, '[class*="star"], [class*="favorite"], svg[class*="icon"]')
            star.click()
            return
        except:
            pass

        try:
            # Tenta por ícone SVG genérico
            star = card_element.find_element(By.CSS_SELECTOR, 'svg, button[type="button"]')
            star.click()
            return
        except:
            raise Exception("Star/favorite button não encontrado no card")

    def get_timer_text(self):
        """Retorna texto do timer (desktop sidebar)."""
        try:
            timer = self.driver.find_element(By.CSS_SELECTOR, '[class*="timer"]')
            return timer.text
        except:
            return None

    def go_back(self):
        """Clica no botão de voltar."""
        back_btn = self.driver.find_element(By.CSS_SELECTOR, '.back-btn')
        back_btn.click()
