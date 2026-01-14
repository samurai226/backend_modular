"""
Serializers pour l'app Authentication
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Role, User, AffectationGare


class RoleSerializer(serializers.ModelSerializer):
    """Serializer pour les rôles"""
    
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer principal pour les utilisateurs"""
    role_detail = RoleSerializer(source='role', read_only=True)
    role_code = serializers.CharField(source='role.nom', read_only=True)
    role_nom = serializers.CharField(source='role.description', read_only=True)
    nom_complet = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'nom', 'prenom', 'email', 'telephone',
            'role', 'role_detail', 'role_code', 'role_nom',
            'nom_complet', 'is_active', 'last_login',
            'latitude', 'longitude', 'photo_url', 'adresse', 'cnib',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }
    
    def create(self, validated_data):
        """Créer un utilisateur"""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """Mettre à jour un utilisateur"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription"""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=6,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'nom', 'prenom', 'telephone', 'email', 
            'password', 'confirm_password', 'role'
        ]
    
    def validate(self, data):
        """Valider les données"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'password': 'Les mots de passe ne correspondent pas'
            })
        
        # Vérifier si le téléphone existe déjà
        if User.objects.filter(telephone=data['telephone']).exists():
            raise serializers.ValidationError({
                'telephone': 'Ce numéro de téléphone est déjà utilisé'
            })
        
        # Vérifier l'email si fourni
        if data.get('email') and User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'Cet email est déjà utilisé'
            })
        
        return data
    
    def create(self, validated_data):
        """Créer un nouvel utilisateur"""
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer pour la connexion"""
    telephone = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """Valider les identifiants"""
        telephone = data.get('telephone')
        password = data.get('password')
        
        if telephone and password:
            user = authenticate(telephone=telephone, password=password)
            
            if not user:
                raise serializers.ValidationError({
                    'detail': 'Identifiants invalides'
                })
            
            if not user.is_active:
                raise serializers.ValidationError({
                    'detail': 'Compte désactivé'
                })
            
            data['user'] = user
        else:
            raise serializers.ValidationError({
                'detail': 'Téléphone et mot de passe requis'
            })
        
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour changer le mot de passe"""
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True, 
        min_length=6,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """Valider les données"""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Les mots de passe ne correspondent pas'
            })
        return data


class AffectationGareSerializer(serializers.ModelSerializer):
    """Serializer pour les affectations de gares"""
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = AffectationGare
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
