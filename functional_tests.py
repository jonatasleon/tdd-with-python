from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith ouviu falar sobre uma nova aplicação legal para to-do lists.
        # Ela vai checar sua homepage
        self.browser.get('http://localhost:8000')

        # Ela percebe que o titulo e o heeader da pagina mencionam To-do lists
        self.assertIn('To-do', self.browser.title)
        self.fail('Finish the test')

        # Ela é convidada a entrar com um to-do item imediatamente

        # Ela digita "Comprar penas de pavão" em um text box (O hobby dela é
        # amarrar iscas de peixes com mosca)

        # Quando ela digita enter, a página atualiza, agora pagina exibe
        # "1: Comprar penas de pavão" como um item em uma lista to-do

        # Ainda tem uma caixa de texto convidando-a para adicionar outro item.
        # Ela entra com "Usar penas para fazer uma mosca" (Edith é metódica)

        # A página atualiza novamente, agora exibe ambos itens na lista

        # Edith se pergunta se o site vai lembrar da sua lista. Então ela vê
        # que o site tem uma url gerada para ela -- há algum texto explicativo
        # para este efeito

        # Ela visita essa URL - a lista dela ainda está lá

        # Satisfeita ela volta a dormir


if __name__ == '__main__':
    unittest.main(warnings='ignore')
