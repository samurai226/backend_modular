"""
Tests pour l'app Authentication
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Role

User = get_user_model()


class RoleModelTest(TestCase):
    """Tests pour le modèle Role"""
    
    def setUp(self):
        self.role = Role.objects.create(
            nom=Role.CLIENT,
            description='Client du système'
        )
    
    def test_role_creation(self):
        """Tester la création d'un rôle"""
        self.assertEqual(self.role.nom, Role.CLIENT)
        self.assertTrue(self.role.is_client)
        self.assertFalse(self.role.is_admin)
    
    def test_role_str(self):
        """Tester la représentation string"""
        self.assertEqual(str(self.role), 'Client')


class UserModelTest(TestCase):
    """Tests pour le modèle User"""
    
    def setUp(self):
        self.role = Role.objects.create(
            nom=Role.CLIENT,
            description='Client'
        )
        self.user = User.objects.create_user(
            telephone='+22670000000',
            password='testpass123',
            nom='Doe',
            prenom='John',
            role=self.role
        )
    
    def test_user_creation(self):
        """Tester la création d'un utilisateur"""
        self.assertEqual(self.user.telephone, '+22670000000')
        self.assertEqual(self.user.nom_complet, 'John Doe')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_roles(self):
        """Tester les propriétés de rôles"""
        self.assertTrue(self.user.is_client)
        self.assertFalse(self.user.is_admin)
    
    def test_superuser_creation(self):
        """Tester la création d'un superuser"""
        admin = User.objects.create_superuser(
            telephone='+22671111111',
            password='admin123',
            nom='Admin',
            prenom='Super'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class AuthAPITest(TestCase):
    """Tests pour les endpoints d'authentification"""
    
    def setUp(self):
        self.client = APIClient()
        self.role = Role.objects.create(
            nom=Role.CLIENT,
            description='Client'
        )
    
    def test_register(self):
        """Tester l'inscription"""
        data = {
            'nom': 'Test',
            'prenom': 'User',
            'telephone': '+22672222222',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'role': str(self.role.id)
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)
    
    def test_login(self):
        """Tester la connexion"""
        # Créer un utilisateur
        user = User.objects.create_user(
            telephone='+22673333333',
            password='testpass123',
            nom='Test',
            prenom='Login',
            role=self.role
        )
        
        # Tenter de se connecter
        data = {
            'telephone': '+22673333333',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
    
    def test_login_invalid(self):
        """Tester la connexion avec des identifiants invalides"""
        data = {
            'telephone': '+22674444444',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
