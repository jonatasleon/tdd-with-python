from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_table_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith ouviu falar sobre uma nova aplicação legal para to-do lists.
        # Ela vai checar sua homepage
        self.browser.get(self.live_server_url)

        # Ela percebe que o titulo e o header da pagina mencionam To-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ela é convidada a entrar com um to-do item imediatamente
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # Ela digita "Comprar penas de pavão" em um text box (O hobby dela é
        # amarrar iscas de peixes com mosca)
        inputbox.send_keys('Buy peacock feathers')

        # Quando ela digita enter, a página atualiza, agora pagina exibe
        # "1: Comprar penas de pavão" como um item em uma lista to-do
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Ainda tem uma caixa de texto convidando-a para adicionar outro item.
        # Ela entra com "Usar penas para fazer uma mosca" (Edith é metódica)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacocks to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # A página atualiza novamente, agora exibe ambos itens na lista
        self.check_for_row_in_list_table('2: Use peacocks to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Agora um novo usuário, Francis, vem para o site

        # Nós usamos um novo sessão no navegador para ter certeza que nenhuma #
        # informação de Edith está vindo através de cookies etc #
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visita a home page. Não há nenhum sinal da lista da Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis começa uma nova lista entrando com um novo item. Ele é menos
        # interessante do que Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis recebe sua própria URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # De novo, não há nem rastro da list de Edith
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfeitos eles voltam a dormir

    def test_layout_and_styling(self):
        # Ela vai checar sua homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Ela nota que a caixa de texto está muito bem centralizada
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
