from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class IndexViewTest(TestCase):

    """
    This class is for testing the Index view
    """
    
    def setUp(self):
        """
        A user test is created in a test database
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_index_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Hello testuser')

    def test_index_view_not_authenticated(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)


class UserLoginViewTest(TestCase):

    """
    This class is for testing the Login view
    """

    def setUp(self):
        """
        A user test is created in a test database
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_login_valid_credentials(self):    
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'incorrect_password'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class UserLogoutViewTest(TestCase):

    """
    This class is for testing the Logout view
    """

    def setUp(self):
        """
        A user test is created in a test database
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_logout_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

class UpdateUserViewTest(TestCase):

    """
    This class is for testing the Update view
    """

    def setUp(self):
        """
        A user test is created in a test database
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            last_name='salas'
        )

    def test_update_user_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        data = {'first_name': 'orlando', 'last_name': 'salas'}
        response = self.client.post(reverse('update'), data)
        self.assertEqual(response.status_code, 200)

        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.first_name, 'orlando')
        self.assertEqual(updated_user.last_name, 'salas')

    def test_update_user_not_authenticated(self):
        data = {'first_name': 'orlando', 'last_name': 'salas'}
        response = self.client.post(reverse('update'), data)
        self.assertEqual(response.status_code, 302)


class RegistrationUserViewTest(TestCase):

    """
    This class is for testing the Registration view
    """

    def setUp(self):
        self.client = Client()

    def test_registration_user_valid_data(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('register'), data)
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)

    def test_registration_user_invalid_data(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'different_password',
        }
        response = self.client.post(reverse('register'), data)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='testuser')

    def test_registration_user_existing_user(self):
        User.objects.create_user(username='existinguser', password='testpassword123')
        data = {
            'username': 'existinguser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(User.objects.filter(username='existinguser').count(), 1)

