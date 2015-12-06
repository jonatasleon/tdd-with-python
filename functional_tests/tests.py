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

        # Ela percebe que o titulo e o heeader da pagina mencionam To-do lists
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
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Ainda tem uma caixa de texto convidando-a para adicionar outro item.
        # Ela entra com "Usar penas para fazer uma mosca" (Edith é metódica)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacocks to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # A página atualiza novamente, agora exibe ambos itens na lista
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacocks to make a fly')

        # Edith se pergunta se o site vai lembrar da sua lista. Então ela vê
        # que o site tem uma url gerada para ela -- há algum texto explicativo
        # para este efeito
        self.fail('Finish the test')

        # Ela visita essa URL - a lista dela ainda está lá

        # Satisfeita ela volta a dormir
