# Django REST Template + AIOGRAM

A production-ready, scalable Django REST API template for rapid backend development. This template includes modular DRF architecture and full async Telegram bot support with aiogram (polling for local development, webhook for production).

---

## 📦 Project Structure

```
django_rest_template/
├── docker-compose.yml / docker-compose.prod.yml   # Docker orchestration (dev/prod)
├── Dockerfile                                     # App Dockerfile
├── scripts/                                       # Utility scripts
│   ├── backup.sh
│   └── entrypoint.sh
├── src/
│   ├── manage.py
│   ├── apps/                                      # Modular Django apps
│   │   ├── account/                               # User/account management
│   │   │   ├── admin/ api/ migrations/ ...
│   │   ├── core/                                  # Core business logic
│   │   │   ├── admin/ api/ migrations/ ...
│   │   ├── url_router.py                          # App URL router
│   ├── config/                                    # Django project config
│   │   ├── server/                                # ASGI/WGI entrypoints
│   │   ├── settings/                              # base.py, dev.py, prod.py
│   │   ├── urls/                                  # URL configs
│   │   └── ...
├── pyproject.toml / uv.lock                       # Python dependencies
├── logs/                                          # Log files
└── README.md
```

---

## 🚀 Features

- **Modular App Structure**: Easily extend with new Django apps under `src/apps/`.
- **JWT Authentication**: Secure endpoints using `rest_framework_simplejwt`.
- **Environment-based Settings**: Separate configs for development and production.
- **Dockerized**: Ready-to-use Docker and Nginx setup for local and cloud deployment.
- **Admin Panel**: Django admin enabled for all registered models.
- **API Versioning**: Organize endpoints under `/api/v1/` and beyond.
- **Async Telegram Bot (aiogram)**: Full bot module with middlewares, dependency injection, i18n tooling, polling, and webhook support.
- **Utility Scripts**: Backup, entrypoint, and other scripts for automation.
- **Logging**: Centralized log directory for error and access logs.

---

## ⚙️ Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/mehroj-r/django_rest_template
cd django_rest_template
```

### 2. Local Development (with uv)
```bash
uv sync
cd src
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

### 3. Dockerized Development
```bash
docker-compose up --build
```
- App: http://localhost:8005
- Admin: http://localhost:8005/admin/

### 4. Run Telegram Bot (Polling for dev)
```bash
cd src
python manage.py runserver
```

In a second terminal:

```bash
cd src
python manage.py runbot
```

### 5. Configure Telegram Bot Webhook (prod)
```bash
cd src
python manage.py botwebhook set
```
Remove webhook:
```bash
python manage.py botwebhook delete
```

Webhook endpoint: `/bot/webhook/`

### 6. Production Deployment
- Edit environment variables and secrets as needed.
- Use `docker-compose.prod.yml` and production settings:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

---

## 🔐 Authentication

- Uses JWT (JSON Web Token) via `rest_framework_simplejwt`.
- Obtain token:
```http
POST /api/v1/token/
{
  "username": "<user>",
  "password": "<pass>"
}
```
- Refresh token:
```http
POST /api/v1/token/refresh/
{
  "refresh": "<refresh_token>"
}
```
- Use `Authorization: Bearer <access_token>` for protected endpoints.

---

## 📚 API Structure & Versioning

- All API endpoints are grouped under `/api/v1/`.
- Add new versions (e.g., `/api/v2/`) by extending the `apps` and `config/urls` modules.
- Example endpoints:
  - `/api/v1/account/` (user management)
  - `/api/v1/core/` (core business logic)

---

## 🛠️ Development Tools

- **Django Debug Toolbar** (dev only)
- **Django Extensions** (dev only)
- **Custom Logging**: All logs in `/logs/`
- **Scripts**: Use `scripts/backup.sh` for DB backups, `scripts/entrypoint.sh` for Docker entrypoint

---

## 📝 Environment Variables

Set these for development/production as needed:
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- Database: `DB_NAME`, `DB_USER_NM`, `DB_USER_PW`, `DB_IP`, `DB_PORT`
- Bot: `BOT_TOKEN`, `BOT_MODE`, `BOT_WEBHOOK_BASE_URL`, `BOT_WEBHOOK_PATH`, `BOT_WEBHOOK_SECRET`, `BOT_PARSE_MODE`, `BOT_DEFAULT_LOCALE`, `BOT_FALLBACK_LOCALE`

---

## 🤖 aiogram Bot Support

- Bot package: `src/bot/`
- Polling worker command: `python manage.py runbot`
- Webhook endpoint: `/bot/webhook/`
- Webhook management command: `python manage.py botwebhook set|delete`
- Local mode is polling (`src/config/settings/dev.py`)
- Production mode is webhook (`src/config/settings/prod.py`)
- Docker entrypoint configures webhook before starting ASGI server

---

## 🌍 Bot Translations

Bot locales live in `src/bot/etc/locales` and use GNU gettext (`.po`/`.mo`).

```bash
cd src
python manage.py boti18n extract
python manage.py boti18n update
python manage.py boti18n compile
```

Create a new locale:

```bash
python manage.py boti18n init --locale uz
```

---

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

---

## 🤝 Contributing

1. Fork the repo & create your branch
2. Make changes with clear commit messages
3. Ensure all tests pass
4. Submit a pull request

---

## 📬 Contact

For questions or support, open an issue or contact the maintainer.
