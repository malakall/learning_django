from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class StaticURLTests(TestCase):
        # сохздаем экземляр клиента , который каждый раз буде запускаться при запуске теста (тут надо писать все что может повторяться и следоват концепции Dry)
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='artem', password='Qwert555')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        # Делаем запрос к главной странице и проверяем статус
        response = self.client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

    def test_StaticURLTests(self):
        response1 = self.client.get('/about/')
        response2 = self.client.get('/orders/')

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    # тут проверка что при нашем гет запросе нам возвращается нужный нам template
    def test_about_url_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'main/index.html', "вася, ты что-то поломал" )


    def test_for_authorizated_user(self):
        response = self.authorized_client.get("/forms/")
        self.assertEqual(response.status_code, 200, "ты баран")

        response2 = self.client.get("/forms/")
        self.assertEqual(response2.status_code, 302, "только для авторизовынных !")

