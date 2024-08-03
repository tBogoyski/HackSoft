from django.test import TestCase

from users.models import CustomUser


class TestCustomUserManager(TestCase):
    def setUp(self):
        self.user_manager = CustomUser.objects

    def test_create_user(self):
        email = 'test_user@example.com'
        password = '123456'
        self.user_manager.create_user(email=email, password=password)

        # Ensure the user was created
        user_qs = CustomUser.objects.filter(email=email)
        self.assertTrue(user_qs.exists())
        user = user_qs.first()
        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_valid)

    def test_create_superuser(self):
        email = 'test_superuser@example.com'
        password = '123456'
        self.user_manager.create_superuser(email=email, password=password)

        # Ensure the superuser was created
        user_qs = CustomUser.objects.filter(email=email)
        self.assertTrue(user_qs.exists())
        superuser = user_qs.first()
        self.assertEqual(email, superuser.email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_valid)

    def test_create_user_with_no_email(self):
        with self.assertRaises(ValueError):
            self.user_manager.create_user(email='', password='123456')

    def test_create_user_with_extra_fields(self):
        email = 'test_user@example.com'
        password = '123456'
        name = 'Custom User'
        user = self.user_manager.create_user(
            email=email,
            password=password,
            name=name,
            is_valid=True
        )

        # Ensure custom fields are set correctly
        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(name, user.name)
        self.assertTrue(user.is_valid)
