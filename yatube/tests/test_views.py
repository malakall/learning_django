from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class ViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="denis", password="dhsj")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)


    def test_about_page_uses_correct_template(self):
        response = self.authorized_client.get(reverse("about"))
        self.assertTemplateUsed(response, "main/about.html")



    def test_home_page_correct_template(self):
        response = self.authorized_client.get(reverse("index"))

        self.assertTemplateUsed(response, "main/index.html")




from ..models import Group
# тест пагинатора
User = get_user_model()

class IndexPaginationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        # Создаём 5 групп с обязательными полями
        number_of_groups = 5
        for i in range(number_of_groups):
            Group.objects.create(
                name=f'Group {i}',
                description=f'Description for group {i}',
                user_name=f'user{i}',
                user=cls.user
            )

    def setUp(self):
        self.client = Client()

    def test_first_page_contains_two_groups(self):
        response = self.client.get(reverse('index')) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['groups']), 2)

    def test_second_page_contains_two_groups(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['groups']), 2)

    def test_third_page_contains_one_group(self):
        response = self.client.get(reverse('index') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['groups']), 1)
