from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProtocoloPage:
    """Page Object para página Protocolo/Fluxograma."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_page_loaded(self):
        """Verifica se página protocolo foi carregada."""
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="protocol"], [class*="fluxo"]')))
            return True
        except:
            return False

    def get_protocol_title(self):
        """Retorna título do protocolo."""
        try:
            # Tenta h1 primeiro
            title = self.driver.find_element(By.TAG_NAME, 'h1')
            return title.text
        except:
            pass

        try:
            # Tenta qualquer elemento com texto de protocolo
            title = self.driver.find_element(By.CSS_SELECTOR, '[class*="title"], [class*="header"]')
            return title.text
        except:
            return None

    def get_flowchart_nodes(self):
        """Retorna lista de nós do fluxograma."""
        # Procura por elementos que representam nós (cards ou buttons com classe fluxo/node/grupo)
        nodes = self.driver.find_elements(By.CSS_SELECTOR, '[class*="node"], [class*="fluxo"], [class*="grupo"]')
        return nodes

    def click_node(self, node_element):
        """Clica em um nó para expandir/expandir."""
        node_element.click()

    def get_expanded_children(self, node_element):
        """Retorna filhos de um nó já expandido."""
        try:
            children = node_element.find_elements(By.CSS_SELECTOR, '[class*="child"], [class*="filled"]')
            return children
        except:
            return []

    def get_favorite_button(self):
        """Retorna botão de favoritar (FAB com star)."""
        try:
            fav_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[class*="favorite"], button[class*="star"]')
            return fav_btn
        except:
            return None

    def toggle_favorite(self):
        """Clica no botão favoritar."""
        fav_btn = self.get_favorite_button()
        if fav_btn:
            fav_btn.click()
            return True
        return False

    def go_back(self):
        """Clica no botão de voltar."""
        back_btn = self.driver.find_element(By.CSS_SELECTOR, '.back-btn')
        # Click via JavaScript se método normal falhar
        try:
            back_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", back_btn)

    def is_favorite_active(self):
        """Verifica se protocolo é favorito (star preenchida)."""
        fav_btn = self.get_favorite_button()
        if fav_btn:
            return '★' in fav_btn.text or 'filled' in fav_btn.get_attribute('class')
        return False
