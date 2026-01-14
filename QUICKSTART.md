# ⚡ Guide de Démarrage Rapide

## 🎯 Installation en 5 Minutes

### 1️⃣ Installation

```bash
# Cloner et entrer dans le dossier
cd backend_modular

# Créer environnement virtuel
python -m venv venv

# Activer
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements/development.txt
```

### 2️⃣ Configuration

```bash
# Copier .env
cp .env.example .env

# Laisser les valeurs par défaut pour commencer
```

### 3️⃣ Base de données

```bash
# Créer et appliquer migrations
python manage.py makemigrations
python manage.py migrate

# Initialiser les rôles
python manage.py shell < scripts/init_data.py

# Créer admin
python manage.py createsuperuser
# Téléphone: +22670000000
# Nom: Admin
# Prénom: Super
# Password: admin123
```

### 4️⃣ Lancer

```bash
python manage.py runserver
```

## 🎉 C'est Prêt!

### Accès
- 🌐 **API**: http://localhost:8000/api/
- 📚 **Swagger**: http://localhost:8000/swagger/
- 👨‍💼 **Admin**: http://localhost:8000/admin/

### Premier Test

#### 1. Obtenir les rôles
```bash
curl http://localhost:8000/api/auth/roles/
```

#### 2. S'inscrire
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Test",
    "prenom": "User",
    "telephone": "+22671111111",
    "password": "test123",
    "confirm_password": "test123",
    "role": "COLLER_UUID_DU_ROLE_CLIENT_ICI"
  }'
```

#### 3. Se connecter
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "telephone": "+22671111111",
    "password": "test123"
  }'
```

#### 4. Utiliser le token
```bash
# Copier le access token de la réponse précédente
curl http://localhost:8000/api/auth/users/me/ \
  -H "Authorization: Bearer VOTRE_ACCESS_TOKEN"
```

## 🧪 Tester avec Swagger

1. Aller sur http://localhost:8000/swagger/
2. Cliquer sur **"Authorize"** 🔓
3. Entrer: `Bearer VOTRE_ACCESS_TOKEN`
4. Cliquer sur **"Authorize"**
5. Tester tous les endpoints! ✅

## 🐛 Problèmes Courants

### Erreur: "No module named 'apps'"
```bash
# S'assurer d'être dans le bon dossier
cd backend_modular
```

### Erreur: "Invalid HTTP_HOST header"
```bash
# Ajouter à .env:
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Erreur migrations
```bash
# Supprimer db et recommencer
rm db.sqlite3
python manage.py migrate
python manage.py shell < scripts/init_data.py
```

## 📱 Intégration Flutter

### BASE_URL
```dart
// lib/config/api_constants.dart
class ApiConstants {
  // Android Emulator
  static const String BASE_URL = 'http://10.0.2.2:8000/api';
  
  // iOS Simulator
  // static const String BASE_URL = 'http://localhost:8000/api';
  
  // Device physique
  // static const String BASE_URL = 'http://VOTRE_IP:8000/api';
}
```

## 🎯 Prochaines Étapes

1. ✅ **Authentication** - Implémenté!
2. 🔜 **Geography** - Prochaine app
3. 🔜 **Transport** - Après Geography
4. 🔜 **Delivery** - Après Transport
5. 🔜 **Payment** - Après Delivery
6. 🔜 **Shop** - Après Payment
7. 🔜 **Notifications** - Dernière app

Chaque app sera créée **pas à pas** avec la même structure!

## 💡 Aide

Pour plus de détails, voir:
- 📖 **README.md** - Documentation complète
- 🏗️ **ARCHITECTURE.md** - Architecture détaillée
- 🧪 **tests/** - Exemples de tests
