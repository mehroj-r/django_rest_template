# Django REST Framework Template

This is a Django REST API template designed for scalable and secure backend development. It supports both production and development settings, uses JWT for authentication, and includes modular configuration and environment management.

## 🔧 Project Structure

```
config/
├── api/
│   └── v1/
│       ├── __init__.py
│       ├── apps.py
│       ├── urls.py
│       └── views.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── dev_urls.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
├── templates/
├── db.sqlite3
├── manage.py
└── requirements.txt
```

## ⚙️ Settings Overview

### `base.py`
Contains shared configuration for both development and production, including installed apps, middleware, templates, and DRF setup.

### `dev.py`
Overrides `base.py` for local development:
- PostgreSQL database setup via environment variables.
- Adds `debug_toolbar` and `django_extensions`.
- Custom logging to console.
- JWT configured for 1-day access tokens, 7-day refresh tokens.

### `prod.py`
Overrides `base.py` for production use:
- SQLite database (can be modified for production DB).
- Basic `DEBUG=True` (should be set to `False` in real deployment).
- JWT authentication via `SimpleJWT`.

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/mehroj-r/django_rest_template.git
cd django_rest_template
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (for `dev.py`)
Create a `.env` file or set manually:
```bash
export DB_NAME=your_db
export DB_USER_NM=your_user
export DB_USER_PW=your_password
export DB_IP=127.0.0.1
export DB_PORT=5432
```

### 5. Run the Server

#### Development
```bash
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py runserver
```

#### Production
```bash
DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py runserver
```

## 🔐 Authentication

This template uses JWT authentication provided by `rest_framework_simplejwt`. All requests to protected endpoints require a Bearer token.

### Obtain Token
```http
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

### Refresh Token
```http
POST /api/token/refresh/
{
    "refresh": "your_refresh_token"
}
```

## 📁 API Versioning

API endpoints are versioned under `/api/v1/`. Add additional versions (e.g., `v2`) in the `api` directory to support future upgrades.

## 🧪 Testing and Debugging

In development mode, the following tools are available:
- **Django Debug Toolbar**: Navigate to any page in development to see DB queries, cache usage, etc.
- **Django Extensions**: Additional management commands (e.g., `runserver_plus`, `shell_plus`).

## 📝 Notes

- Default database in production is SQLite — recommended only for prototyping.
- **Remember to change the `SECRET_KEY` and set `DEBUG=False` in production!**
- Use a production-ready DB (e.g., PostgreSQL) and configure `ALLOWED_HOSTS`.