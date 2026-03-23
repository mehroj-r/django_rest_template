# {{ cookiecutter.project_name }}

A production-ready, scalable Django REST API template for rapid backend development. This template features modular app structure, JWT authentication, Docker support, environment-based settings, and best practices for both development and deployment.

---

## 📦 Project Structure

```
{{ cookiecutter.project_slug }}/
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
- **Utility Scripts**: Backup, entrypoint, and other scripts for automation.
- **Logging**: Centralized log directory for error and access logs.

---

## ⚙️ Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
cd {{ cookiecutter.project_slug }}
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
- App: http://localhost:8000
- Admin: http://localhost:8000/admin/

### 4. Production Deployment
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
- Logging: `LOGGING_TELEGRAM_BOT_TOKEN`, `LOGGING_TELEGRAM_CHAT_ID`

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
