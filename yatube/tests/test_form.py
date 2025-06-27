from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Group  # или нужная модель, например Post

User = get_user_model()

class PostCreateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)  # авторизуем пользователя

    def test_create_post(self):
        posts_count = Group.objects.count()  # считаем записи до создания новой

        form_data = {
            'name': 'New Group',
            'description': 'Description for new group',
            'user_name': 'username123',
            # если есть другие обязательные поля, добавьте их сюда
        }

        response = self.client.post(
            reverse('index'),  # URL создания поста
            data=form_data,
            follow=True
        )

        # Проверяем, что произошёл редирект (код 200 после follow)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что количество записей увеличилось на 1
        self.assertEqual(Group.objects.count(), posts_count + 1)

        # Проверяем, что новая запись с нужными данными существует
        self.assertTrue(Group.objects.filter(name='New Group', user_name='username123').exists())


    def test_changeies_in_form(self):
        post_count = Group.objects.count()

        group = Group.objects.create(
            name='Old Group',
            description='Old description',
            user_name='olduser',
            user=self.user
        )

        form_data = {
            'name': 'New Group',
            'description': 'Description for new group',
            'user_name': 'username123',

        }

        response = self.client.post(
        reverse('edit_group', args=[group.id]),
        data=form_data,
        follow=True
        )

        self.assertEqual(response.status_code, 200)
        group.refresh_from_db()
        self.assertEqual(group.name, "New Group")
        self.assertEqual(group.description, "Description for new group")


from ..models import Comment, Group

class CommetsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.authorized_client = Client()
        self.user = User.objects.create_user(username="kdljf", password="323232")
        self.authorized_client.force_login(self.user)

        self.group = Group.objects.create(
            name="Test Group",
            description="Test description",
            user_name="artem",
            user=self.user         
        )

        self.comment_count = Comment.objects.count()

    def test_comment_created(self):
        response = self.authorized_client.post(
            reverse('group_detail', kwargs={'group_id': self.group.pk}), 
            data={'text': 'Новый комментарий'}
        )

        self.assertEqual(Comment.objects.count(), self.comment_count + 1)
        self.assertRedirects(response, reverse('group_detail', kwargs={'group_id': self.group.pk}))

