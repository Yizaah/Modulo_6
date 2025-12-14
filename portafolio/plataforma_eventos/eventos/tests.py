from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail


class AuthTests(TestCase):
	def test_register_creates_user_and_shows_activation_message(self):
		url = reverse('register')
		data = {
			'username': 'testuser',
			'email': 'test@example.com',
			'password1': 'complexpassword123',
			'password2': 'complexpassword123',
		}
		response = self.client.post(url, data, follow=True)
		self.assertTrue(User.objects.filter(username='testuser').exists())
		user = User.objects.get(username='testuser')
		# user should be inactive until activation
		self.assertFalse(user.is_active)
		# should redirect to register done
		self.assertRedirects(response, reverse('register_done'), fetch_redirect_response=False, status_code=302)

	def test_register_duplicate_email_fails(self):
		User.objects.create_user(username='exists', email='dup@example.com', password='x')
		url = reverse('register')
		data = {
			'username': 'newuser',
			'email': 'dup@example.com',
			'password1': 'anotherpass123',
			'password2': 'anotherpass123',
		}
		response = self.client.post(url, data)
		# Should re-render form with errors
		self.assertContains(response, 'Ya existe un usuario con ese correo electrónico.')

	def test_password_reset_sends_email(self):
		User.objects.create_user(username='pwuser', email='pw@example.com', password='pw')
		url = reverse('password_reset')
		response = self.client.post(url, {'email': 'pw@example.com'}, follow=True)
		# One email should be sent using Django's email backend
		self.assertEqual(len(mail.outbox), 1)
		self.assertIn('pw@example.com', mail.outbox[0].to)

	def test_registration_sends_activation_email_and_activation_works(self):
		url = reverse('register')
		data = {
			'username': 'inactive',
			'email': 'inactive@example.com',
			'password1': 'complexpassword123',
			'password2': 'complexpassword123',
		}
		response = self.client.post(url, data, follow=True)
		# user created but inactive
		user = User.objects.get(username='inactive')
		self.assertFalse(user.is_active)
		# activation email sent
		self.assertEqual(len(mail.outbox), 1)

		# Build activation URL and confirm activation
		from django.utils.http import urlsafe_base64_encode
		from django.utils.encoding import force_bytes
		from django.contrib.auth.tokens import default_token_generator

		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		act_url = reverse('activate', args=[uid, token])
		resp = self.client.get(act_url, follow=True)
		user.refresh_from_db()
		self.assertTrue(user.is_active)
		# After activation, user should be logged in
		self.assertTrue(resp.context.get('user').is_authenticated)


class PermissionTests(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', password='p')
		self.user2 = User.objects.create_user(username='user2', password='p')
		self.super = User.objects.create_superuser(username='su', password='p', email='su@example.com')

	def test_private_event_access_denied(self):
		from .models import Evento
		evento = Evento.objects.create(
			titulo='Privado', descripcion='x', tipo='conferencia', fecha='2030-01-01T10:00:00Z', es_privado=True, organizador=self.user1
		)
		self.client.login(username='user2', password='p')
		url = reverse('evento_detail', args=[evento.pk])
		response = self.client.get(url, follow=True)
		# Should redirect to acceso_denegado
		self.assertRedirects(response, reverse('acceso_denegado'), fetch_redirect_response=False, status_code=302)

	def test_create_event_requires_permission(self):
		url = reverse('evento_create')
		self.client.login(username='user2', password='p')
		data = {
			'titulo': 'Test', 'descripcion': 'desc', 'tipo': 'conferencia', 'fecha': '2030-01-01T12:00:00Z', 'es_privado': False
		}
		response = self.client.post(url, data, follow=True)
		# user2 has no add_evento permission; no Evento should be created
		from .models import Evento
		self.assertFalse(Evento.objects.filter(titulo='Test').exists())

	def test_superuser_sees_all_events(self):
		from .models import Evento
		Evento.objects.create(titulo='A', descripcion='', tipo='conferencia', fecha='2030-01-01T10:00:00Z', organizador=self.user1)
		Evento.objects.create(titulo='B', descripcion='', tipo='concierto', fecha='2030-02-01T10:00:00Z', organizador=self.user2)
		self.client.login(username='su', password='p')
		url = reverse('evento_list')
		response = self.client.get(url)
		self.assertContains(response, 'A')
		self.assertContains(response, 'B')

# Create your tests here.
