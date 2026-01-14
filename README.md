# 🚀 Backend Transport - Architecture Modulaire

Backend Django avec architecture modulaire pour application de gestion de transport de passagers et colis.

## 📂 Structure du Projet

```
backend/
├── config/                 # Configuration Django
│   └── settings/          # Settings modulaires (base, dev, prod)
├── apps/                  # Applications modulaires
│   └── authentication/    # ✅ Gestion utilisateurs & JWT
├── core/                  # Utilitaires communs
├── docs/                  # Documentation
├── logs/                  # Logs
├── media/                 # Fichiers uploadés
└── requirements/          # Dépendances
```

## ✅ Apps Implémentées

### 1. **Authentication** (Complète)
- ✅ Modèles: `User`, `Role`, `AffectationGare`
- ✅ JWT Authentication
- ✅ Endpoints: register, login, logout, change_password
- ✅ Permissions personnalisées
- ✅ Tests unitaires
- ✅ Admin Django

## 🚀 Installation

### Prérequis
- Python 3.10+
- pip
- virtualenv

### 1. Cloner et Setup

```bash
# Aller dans le dossier
cd backend_modular

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements/development.txt
```

### 2. Configuration

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env avec vos paramètres
nano .env  # ou votre éditeur préféré
```

### 3. Base de données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Initialiser les données (rôles)
python manage.py shell < scripts/init_data.py

# Créer un superutilisateur
python manage.py createsuperuser
```

### 4. Lancer le serveur

```bash
# Mode développement
python manage.py runserver

# Avec un port personnalisé
python manage.py runserver 8080
```

## 🌐 Endpoints API

### Base URL
```
http://localhost:8000/api/
```

### Authentication (`/api/auth/`)

| Endpoint | Méthode | Auth | Description |
|----------|---------|------|-------------|
| `/register/` | POST | Non | Inscription |
| `/login/` | POST | Non | Connexion |
| `/logout/` | POST | Oui | Déconnexion |
| `/change-password/` | POST | Oui | Changer mot de passe |
| `/token/refresh/` | POST | Non | Rafraîchir token |
| `/users/` | GET | Oui | Liste utilisateurs |
| `/users/me/` | GET | Oui | Utilisateur connecté |
| `/users/{id}/` | GET/PUT/PATCH | Oui | Détail utilisateur |
| `/users/{id}/activate/` | POST | Admin | Activer utilisateur |
| `/users/{id}/deactivate/` | POST | Admin | Désactiver utilisateur |
| `/roles/` | GET | Oui | Liste rôles |

## 📝 Exemples d'Utilisation

### 1. Inscription

```bash
POST /api/auth/register/
Content-Type: application/json

{
  "nom": "Doe",
  "prenom": "John",
  "telephone": "+22670000000",
  "email": "john@example.com",
  "password": "securepass123",
  "confirm_password": "securepass123",
  "role": "uuid-du-role-client"
}
```

**Réponse:**
```json
{
  "user": {
    "id": "uuid",
    "nom": "Doe",
    "prenom": "John",
    "telephone": "+22670000000",
    "email": "john@example.com",
    "role": "uuid-du-role",
    "nom_complet": "John Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Inscription réussie"
}
```

### 2. Connexion

```bash
POST /api/auth/login/
Content-Type: application/json

{
  "telephone": "+22670000000",
  "password": "securepass123"
}
```

**Réponse:**
```json
{
  "user": {
    "id": "uuid",
    "nom_complet": "John Doe",
    "telephone": "+22670000000",
    "role_code": "client"
  },
  "tokens": {
    "refresh": "...",
    "access": "..."
  },
  "message": "Connexion réussie"
}
```

### 3. Utiliser le Token

```bash
GET /api/auth/users/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### 4. Rafraîchir le Token

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "votre-refresh-token"
}
```

## 🔒 Authentification JWT

### Tokens
- **Access Token**: Durée de vie **1 jour**
- **Refresh Token**: Durée de vie **7 jours**
- Rotation automatique des tokens
- Blacklist après déconnexion

### Headers
```
Authorization: Bearer <access_token>
```

## 👥 Rôles Disponibles

| Code | Nom | Description |
|------|-----|-------------|
| `admin` | Administrateur | Tous les droits |
| `gerant` | Gérant de gare | Gestion d'une gare |
| `guichetier` | Guichetier | Vente de tickets |
| `colissier` | Colissier | Gestion colis |
| `livreur` | Livreur | Livraisons |
| `client` | Client | Réservations |
| `expediteur` | Expéditeur | Envoi colis |
| `recepteur` | Récepteur | Réception colis |

## 🧪 Tests

```bash
# Lancer tous les tests
python manage.py test

# Tests pour authentication
python manage.py test apps.authentication

# Tests avec pytest
pytest

# Tests avec couverture
pytest --cov=apps
```

## 📚 Documentation API

### Swagger UI
```
http://localhost:8000/swagger/
```

### ReDoc
```
http://localhost:8000/redoc/
```

### Swagger JSON
```
http://localhost:8000/swagger.json
```

## 🛠️ Commandes Utiles

```bash
# Créer une nouvelle app
python manage.py startapp nom_app apps/nom_app

# Créer migrations
python manage.py makemigrations

# Appliquer migrations
python manage.py migrate

# Shell interactif
python manage.py shell

# Créer superuser
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer les tests
python manage.py test
```

## 🌍 Environnements

### Développement
```bash
export DJANGO_ENV=development
python manage.py runserver
```

### Production
```bash
export DJANGO_ENV=production
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Tests
```bash
export DJANGO_ENV=test
python manage.py test
```

## 📦 Prochaines Apps à Implémenter

- [ ] **Geography** - Pays, Villes, Gares
- [ ] **Transport** - Trajets, Bus, Réservations
- [ ] **Delivery** - Colis, Livraisons
- [ ] **Payment** - Paiements, Rapports
- [ ] **Shop** - Articles, Promotions
- [ ] **Notifications** - Notifications push

## 🐛 Debugging

### Logs
```bash
# Voir les logs
tail -f logs/django.log
```

### Django Debug Toolbar
Installé en mode développement, accessible à:
```
http://localhost:8000/__debug__/
```

## 📄 License

MIT License

## 👨‍💻 Auteur

Développé avec ❤️ pour le projet Transport
