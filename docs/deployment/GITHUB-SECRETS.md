# GitHub Secrets Configuration

This document outlines all the secrets that need to be configured in your GitHub repository for deployment workflows to function properly.

## How to Add Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter the secret name and value
5. Click **Add secret**

---

## Development Deployment Secrets (`deploy-dev.yml`)

Required secrets for the development deployment workflow:

| Secret Name | Description                                         | Example                            |
|---|-----------------------------------------------------|------------------------------------|
| `LOCATION` | Project directory on the server                     | `/opt/projects/django_boilerplate` |
| `SSH_HOST` | Hostname or IP address of the server                | `example.com` or `192.168.1.100`   |
| `SSH_USERNAME` | SSH username for authentication on the dev server   | `deploy` or `devops`               |
| `SSH_PRIVATE_KEY` | SSH private key for passwordless authentication     | ED25519/RSA private key            |
| `DEPLOY_BRANCH` | Git branch to deploy from. (default: `development`) | `development`, `production`        |

---

## Production Deployment Secrets (`deploy-prod.yml`)

Required secrets for the production deployment workflow:

| Secret Name | Description | Example                                    |
|---|---|--------------------------------------------|
| `CONTAINER_NAME` | Docker container name/image name | `django-boilerplate`                       |
| `SSH_USER` | SSH username for authentication on the prod server | `deploy` or `devops`                       |
| `SSH_HOST` | Hostname or IP address of the production server | `example.com` or `prod.example.com`    |
| `LOCATION` | Project directory on the server | `/home/deploy/projects/django_boilerplate` |
| `SSH_PRIVATE_KEY` | SSH private key for passwordless authentication | (ED25519 or RSA private key content)       |

---

### Steps to Setup SSH Key for server authentication:

1. **Generate SSH Key Pair**
   ```bash
   ssh-keygen -t rsa -b 4096 -C "github-deploy" -f ~/.ssh/github_deploy
   ```

2. **Add public key to the server**:
   ```bash
   cat ~/.ssh/github_deploy.pub | ssh deploy@server.com "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
   ```
3. **Verify SSH access using the new key**:
    ```bash
    ssh -i ~/.ssh/github_deploy
    ```
4. **Get the private key content** and add as `SSH_PRIVATE_KEY` secret:
   ```bash
   cat ~/.ssh/github_deploy
   ```

