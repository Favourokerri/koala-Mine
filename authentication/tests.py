from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from userProfile.models import Profile

# Create your tests here.
class SignUpViewTest(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.signUp_url = reverse('signUp')
    
    def test_register_view_success(self):
        """ test for successful signUp"""
        response = self.client.post(self.signUp_url, {
            "username": "favourokerri767@gmail.com",
            "email": "favourokerri767@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "super12345",
            "confirm_password": "super12345"
        })

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='favourokerri767@gmail.com').exists())
        user = User.objects.get(username='favourokerri767@gmail.com')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_register_view_for_duplicate_email(self):
        User.objects.create(username='favourokerri767@gmail.com', password='favour21')
        response = self.client.post(self.signUp_url, {
            "username": "favourokerri767@gmail.com",
            "email": "favourokerri767@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "super12345",
            "confirm_password": "super12345"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('user with this username already exits', response.content.decode())