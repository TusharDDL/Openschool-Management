# School Management System - Deployment Guide

## Table of Contents
1. [Production Deployment](#production-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [CI/CD Setup](#cicd-setup)
5. [Monitoring Setup](#monitoring-setup)
6. [Backup Strategy](#backup-strategy)

## Production Deployment

### System Requirements

#### Minimum Requirements
```
CPU: 2 cores
RAM: 4GB
Storage: 50GB SSD
OS: Ubuntu 20.04 LTS or higher
```

#### Recommended Requirements
```
CPU: 4 cores
RAM: 8GB
Storage: 100GB SSD
OS: Ubuntu 22.04 LTS
```

### Server Setup

#### 1. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y nginx postgresql redis-server python3.11 python3.11-venv nodejs npm

# Install certbot for SSL
sudo apt install -y certbot python3-certbot-nginx
```

#### 2. Configure Nginx
```nginx
# /etc/nginx/sites-available/school-management
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Static files
    location /static {
        alias /var/www/school-management/static;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Media files
    location /media {
        alias /var/www/school-management/media;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

#### 3. SSL Configuration
```bash
# Install SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Application Deployment

#### 1. Frontend Deployment
```bash
# Build frontend
npm run build

# Install PM2
npm install -g pm2

# Start frontend
pm2 start npm --name "frontend" -- start

# Save PM2 configuration
pm2 save
```

#### 2. Backend Deployment
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn

# Start backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Docker Deployment

### 1. Production Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend.prod
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
    ports:
      - "3000:3000"
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://user:pass@db:5432/school_management
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=school_management
    restart: unless-stopped

volumes:
  postgres_data:
```

### 2. Production Dockerfile for Frontend
```dockerfile
# Dockerfile.frontend.prod
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

### 3. Production Dockerfile for Backend
```dockerfile
# Dockerfile.prod
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

## Cloud Deployment

### AWS Deployment

#### 1. EC2 Setup
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS
aws configure
```

#### 2. RDS Setup
```bash
# Create RDS instance
aws rds create-db-instance \
    --db-instance-identifier school-management \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password your_password \
    --allocated-storage 20
```

#### 3. S3 Setup for Static Files
```bash
# Create S3 bucket
aws s3 mb s3://school-management-static

# Configure bucket policy
aws s3api put-bucket-policy --bucket school-management-static --policy file://bucket-policy.json
```

### Docker Swarm Deployment

#### 1. Initialize Swarm
```bash
# Initialize swarm
docker swarm init

# Join worker nodes
docker swarm join --token <token> <manager-ip>:2377
```

#### 2. Deploy Stack
```bash
# Deploy stack
docker stack deploy -c docker-compose.prod.yml school-management

# Check services
docker service ls

# Scale services
docker service scale school-management_backend=3
```

## CI/CD Setup

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/school-management
            git pull
            npm ci
            npm run build
            pm2 restart all
```

## Monitoring Setup

### 1. Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'school-management'
    static_configs:
      - targets: ['localhost:8000']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
```

### 2. Grafana Dashboard
```json
{
  "dashboard": {
    "id": null,
    "title": "School Management Dashboard",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "http_request_duration_seconds"
          }
        ]
      }
    ]
  }
}
```

### 3. Alert Configuration
```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'email-notifications'

receivers:
- name: 'email-notifications'
  email_configs:
  - to: 'admin@yourdomain.com'
    from: 'alertmanager@yourdomain.com'
    smarthost: 'smtp.gmail.com:587'
    auth_username: 'your-email@gmail.com'
    auth_password: 'your-app-specific-password'
```

## Backup Strategy

### 1. Database Backup
```bash
#!/bin/bash
# backup.sh

# Set variables
BACKUP_DIR="/var/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="school_management"

# Create backup
pg_dump -Fc $DB_NAME > $BACKUP_DIR/backup_$DATE.dump

# Upload to S3
aws s3 cp $BACKUP_DIR/backup_$DATE.dump s3://school-management-backups/

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -type f -mtime +7 -delete
```

### 2. File Backup
```bash
#!/bin/bash
# backup-files.sh

# Set variables
BACKUP_DIR="/var/backups/files"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/var/www/school-management"

# Create backup
tar -czf $BACKUP_DIR/files_$DATE.tar.gz $APP_DIR

# Upload to S3
aws s3 cp $BACKUP_DIR/files_$DATE.tar.gz s3://school-management-backups/

# Clean old backups
find $BACKUP_DIR -type f -mtime +7 -delete
```

### 3. Automated Backup Schedule
```bash
# Add to crontab
0 1 * * * /path/to/backup.sh
0 2 * * * /path/to/backup-files.sh
```

### 4. Backup Verification
```bash
#!/bin/bash
# verify-backup.sh

# Test database restore
pg_restore -C -d postgres $BACKUP_DIR/backup_$DATE.dump

# Verify files
tar -tzf $BACKUP_DIR/files_$DATE.tar.gz

# Check S3 sync
aws s3 ls s3://school-management-backups/
```