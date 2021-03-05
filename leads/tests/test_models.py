from django.test import TestCase

from leads.models import User, UserProfile


class TestUserModel(TestCase):

    # maybe this test isn't quite necessary becaue we don't need to test django core methods
    def test_user_creation_signal(self):

        test_user = User.objects.create(
            username='testuser', email='testemail@gmail.com', password='1234@14RsF')

        user_profile = UserProfile.objects.filter(user=test_user)
        self.assertEqual(user_profile[0].pk, test_user.pk)
