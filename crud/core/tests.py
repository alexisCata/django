from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test import TestCase

from .forms import BankUserForm
from .models import BankUser, BankAccount
from .views import list_users, add_user, add_bank_account, update_user, delete_user, delete_bank_account


# models test
class BankUserTest(TestCase):
    def create_bankuser(self, first_name="first_name", last_name="last_name"):
        user = User.objects.create()
        return BankUser.objects.create(first_name=first_name, last_name=last_name, owner=user)

    def test_bankuser_creation(self):
        b = self.create_bankuser()
        self.assertTrue(isinstance(b, BankUser))


class BankAccountTest(TestCase):
    def create_bankaccount(self, IBAN="123456789"):
        user = User.objects.create()
        bu = BankUser.objects.create(first_name='name', last_name='last_name', owner=user)
        return BankAccount.objects.create(bank_user=bu, IBAN=IBAN)

    def test_bankaccount_creation(self):
        b = self.create_bankaccount()
        self.assertTrue(isinstance(b, BankAccount))


# forms test
class BankUserFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_bankuserform_valid(self):
        form_data = {'first_name': 'firstname',
                     'last_name': 'lastname',
                     'DNI': '12345678Z'}
        form = BankUserForm(data=form_data)
        form.owner = self.user
        self.assertTrue(form.is_valid())

    def test_bankuserform_invalid(self):
        form_data = {'first_name': '12345',
                     'last_name': '12234'}
        form = BankUserForm(data=form_data)
        form.owner = self.user
        self.assertFalse(form.is_valid())


# views test
class TestHome(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_anonymous_redirect_login(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/login/?next=/')
        response = self.client.post('/', follow=True)
        self.assertRedirects(response, '/login/?next=/')

    def test_home_loads(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')


class TestViewListUsers(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        BankUser.objects.create(first_name='test_name_bank_user', last_name='last_name', DNI='12345678Z', owner=self.user)

        self.factory = RequestFactory()

    def test_response(self):
        request = self.factory.get('/')
        request.user = self.user
        response = list_users(request)
        self.assertContains(response, 'Hello')
        self.assertContains(response, 'test_name_bank_user')


class TestViewAddUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get('user')
        request.user = self.user
        response = add_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<button class="btn btn-primary" name="save" type="submit">Save</button>', response.content)

    def test_post(self):
        request = self.factory.post('user')
        request.user = self.user
        request.POST = {'csrfmiddlewaretoken': ['PE44cEnEQ41e8UL9DXb8KTGQd5vH55AKCgVFkAozw6qRn3B0jitAwbkg15O3Kocj'],
                        # 'form-MIN_NUM_FORMS': '',
                        # 'form-MAX_NUM_FORMS': '',
                        # 'form-INITIAL_FORMS': '0',
                        # 'form-TOTAL_FORMS': '1',
                        #
                        # 'form-0-IBAN': 'ES7921000813610123456789',
                        # 'form-0-bank_user': '',
                        # 'form-0-id': '',

                        'first_name': 'firstname',
                        'last_name': 'lastname',
                        'DNI': '12345678Z',
                        'save': ''}

        response = add_user(request)

        self.assertEqual(response.status_code, 302)

        user = BankUser.objects.filter(first_name='firstname', last_name='lastname', DNI='12345678Z')
        num = len(user)
        self.assertEquals(num, 1)

        # num = BankAccount.objects.filter(bank_user=user[0]).count()
        # self.assertEquals(num, 1)


class TestViewAddBankAccount(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.bankuser = BankUser.objects.create(first_name='firstname', last_name='lastname', DNI='12345678Z', owner=self.user)
        self.bankuser.save()
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get('add_bank_account/{}'.format(self.bankuser.id))
        request.user = self.user
        response = add_bank_account(request, self.bankuser.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<button class="btn btn-primary" name="save" type="submit">Save</button>', response.content)

    def test_post(self):
        request = self.factory.post('add_bank_account/{}'.format(self.bankuser.id))
        request.user = self.user
        request.POST = {'csrfmiddlewaretoken': ['PE44cEnEQ41e8UL9DXb8KTGQd5vH55AKCgVFkAozw6qRn3B0jitAwbkg15O3Kocj'],
                        'IBAN': 'ES7921000813610123456789'}

        response = add_bank_account(request, self.bankuser.id)

        self.assertEqual(response.status_code, 302)

        num = BankAccount.objects.filter(bank_user=self.bankuser).count()
        self.assertEquals(num, 1)


class TestViewUpdateUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        bu = BankUser(first_name='firstname', last_name='lastname', DNI='12345678Z', owner=self.user)
        bu.save()
        self.bank_user = bu
        ba = BankAccount(IBAN='ES7921000813610123456789', bank_user=self.bank_user)
        ba.save()
        self.bank_account = ba
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get('update/{}'.format(self.bank_user.id))
        request.user = self.user
        response = update_user(request, self.bank_user.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<button class="btn btn-primary" name="save" type="submit">Save</button>', response.content)
        self.assertIn(b'firstname', response.content)
        self.assertIn(b'lastname', response.content)

    def test_post(self):
        request = self.factory.post('update/{}'.format(self.bank_user.id))
        request.user = self.user
        request.POST = {'csrfmiddlewaretoken': ['PE44cEnEQ41e8UL9DXb8KTGQd5vH55AKCgVFkAozw6qRn3B0jitAwbkg15O3Kocj'],
                        # 'form-MIN_NUM_FORMS': '',
                        # 'form-MAX_NUM_FORMS': '',
                        # 'form-INITIAL_FORMS': '0',
                        # 'form-TOTAL_FORMS': '1',
                        #
                        # 'form-0-IBAN': 'ES7921000813610123456789',
                        # 'form-0-bank_user': '',
                        # 'form-0-id': '',

                        'first_name': 'newfirstname',
                        'last_name': 'lastname',
                        'DNI': '12345678Z',
                        'save': ''}

        response = update_user(request, self.bank_user.id)
        self.assertEqual(response.status_code, 302)

        num = BankUser.objects.filter(first_name='newfirstname').count()
        self.assertEquals(num, 1)


class TestDeleteUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        bu = BankUser(first_name='firstname', last_name='lastname', DNI='12345678Z', owner=self.user)
        bu.save()
        self.bank_user = bu
        ba = BankAccount(IBAN='ES7921000813610123456789', bank_user=self.bank_user)
        ba.save()
        self.bank_account = ba
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get('delete/{}'.format(self.bank_user.id))
        request.user = self.user
        response = delete_user(request, self.bank_user.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Delete user', response.content)

    def test_post(self):
        request = self.factory.post('delete/{}'.format(self.bank_user.id))
        request.user = self.user
        request.POST = {'delete': 'delete'}

        response = delete_user(request, self.bank_user.id)
        self.assertEqual(response.status_code, 302)

        self.assertNotIn(b'firstname', response.content)
        self.assertNotIn(b'lastname', response.content)

        num = BankUser.objects.filter(first_name='firstname', last_name='lastname', DNI='12345678Z').count()
        self.assertEquals(num, 0)


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        bu = BankUser(first_name='firstname', last_name='lastname', DNI='12345678Z', owner=self.user)
        bu.save()
        self.bank_user = bu
        ba = BankAccount(IBAN='ES7921000813610123456789', bank_user=self.bank_user)
        ba.save()
        self.bank_account = ba
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get('user/delete_bank_account/{}'.format(self.bank_user.id))
        request.user = self.user
        response = delete_bank_account(request, self.bank_account.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Delete account', response.content)

    def test_post(self):
        request = self.factory.post('user/delete_bank_account/{}'.format(self.bank_user.id))
        request.user = self.user
        request.POST = {'delete': 'delete'}

        response = delete_user(request, self.bank_user.id)
        self.assertEqual(response.status_code, 302)

        self.assertNotIn(b'ES7921000813610123456789', response.content)

        num = BankAccount.objects.filter(IBAN="ES7921000813610123456789").count()
        self.assertEquals(num, 0)
