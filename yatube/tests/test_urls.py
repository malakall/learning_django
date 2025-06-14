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
    
    # тест страницы которая не существует
    def test_non_exists_page(self):
        response = self.client.get("/edjf")

        self.assertEqual(response.status_code, 404, "страница должна быть не найден")

        # это список всех шаблонов, фактически использованных при рендеринге.
        template_names = [t.name for t in response.templates]
        self.assertIn('core/404.html', template_names)



from ..models import Comment, Group

class CommentsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.authorized_client = Client()
        self.user = User.objects.create_user(username="ksnjd", password="121212")
        self.authorized_client.force_login(self.user)

        self.group = Group.objects.create(
            name="Test Group",
            description="Test description",
            user_name="ksnjd",
            user=self.user
        )

    def test_comments_post_auth(self):
        url = f"/group/{self.group.id}/"
        response = self.authorized_client.get(url) 
        self.assertEqual(response.status_code, 200)

    
    def test_comments_post_non_auth(self):
        url = f"/group/{self.group.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)