import factory

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .signing import create_email_change_token
from .views import EmailChangeConfirmView


User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name', 'ja_JP')
    email = factory.Faker('email')


class EmailCheckTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.another_user = UserFactory.create()
        self.new_email = factory.Faker("email").generate({})

    def test_chenge_email(self):
        token = create_email_change_token(self.user, self.new_email)
        rf = APIRequestFactory()
        request = rf.post("")
        request.user = self.user
        res = EmailChangeConfirmView.as_view()(request, token=token)
        assert res.status_code == 200
        u = User.objects.get(id=self.user.pk)
        assert u.email != self.user.email
        assert u.email == self.new_email

    def test_no_login(self):
        token = create_email_change_token(self.user, self.new_email)
        rf = APIRequestFactory()
        request = rf.post("")
        res = EmailChangeConfirmView.as_view()(request, token=token)
        assert res.status_code == 401

    def test_another_user_login(self):
        token = create_email_change_token(self.user, self.new_email)
        rf = APIRequestFactory()
        request = rf.post("")
        request.user = self.another_user
        res = EmailChangeConfirmView.as_view()(request, token=token)
        assert res.status_code == 409
