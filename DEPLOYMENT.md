# 🚀 Guía de Deployment - Multicont Flask API

## Tabla de Contenidos
- [Requisitos de Producción](#requisitos-de-producción)
- [Docker Setup](#docker-setup)
- [Configuración de Producción](#configuración-de-producción)
- [Deployment con Docker Compose](#deployment-con-docker-compose)
- [CI/CD con GitHub Actions](#cicd-con-github-actions)
- [Monitoring y Logging](#monitoring-y-logging)
- [Backup y Recuperación](#backup-y-recuperación)
- [Troubleshooting](#troubleshooting)

---

## Requisitos de Producción

### Hardware Mínimo Recomendado
- **CPU**: 2 cores (4 cores recomendado)
- **RAM**: 4GB (8GB recomendado)
- **Storage**: 20GB SSD
- **Network**: 100 Mbps

### Software Requerido
- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **PostgreSQL**: 15+ (via Docker)
- **Nginx**: 1.25+ (via Docker)
- **Git**: Para CI/CD

### Variables de Entorno de Producción

```bash
# .env.production
DATABASE_URL=postgresql+psycopg2://multicont_user:STRONG_PASSWORD@postgres:5432/multicont_prod
SECRET_KEY=GENERATE_WITH_python_-c_"import_secrets;_print(secrets.token_hex(32))"
JWT_SECRET_KEY=GENERATE_WITH_python_-c_"import_secrets;_print(secrets.token_hex(32))"

FLASK_ENV=production
FLASK_DEBUG=False

# Redis para caching en producción
CACHE_TYPE=RedisCache
CACHE_REDIS_HOST=redis
CACHE_REDIS_PORT=6379
CACHE_REDIS_PASSWORD=STRONG_REDIS_PASSWORD
CACHE_DEFAULT_TIMEOUT=300

# Email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-app-password
```

**⚠️ IMPORTANTE**: Nunca commitear `.env.production` al repositorio.

---

## Docker Setup

### 1. Dockerfile Multi-stage

**Archivo**: `Dockerfile`

```dockerfile
# Stage 1: Builder
FROM python:3.13-slim as builder

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-slim

WORKDIR /app

# Instalar solo dependencias de runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias instaladas desde builder
COPY --from=builder /root/.local /root/.local

# Copiar código de la aplicación
COPY . .

# Hacer scripts ejecutables
RUN chmod +x docker-entrypoint.sh

# Variables de entorno
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py

# Exponer puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]
```

### 2. Docker Entrypoint Script

**Archivo**: `docker-entrypoint.sh`

```bash
#!/bin/bash
set -e

echo "🚀 Iniciando Multicont Flask API..."

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando PostgreSQL..."
while ! nc -z postgres 5432; do
    sleep 1
done
echo "✅ PostgreSQL está listo"

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones de base de datos..."
flask db upgrade

# Verificar salud de la base de datos
echo "🔍 Verificando conexión a base de datos..."
python -c "from app import db, create_app; app = create_app(); app.app_context().push(); db.session.execute('SELECT 1')"

echo "✅ Aplicación lista para recibir tráfico"

# Ejecutar comando principal (gunicorn)
exec "$@"
```

### 3. Docker Compose (Producción)

**Archivo**: `docker-compose.prod.yml`

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: multicont_postgres
    restart: always
    environment:
      POSTGRES_DB: multicont_prod
      POSTGRES_USER: multicont_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U multicont_user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - multicont_network

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: multicont_redis
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD} --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - multicont_network

  # Flask Application
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: multicont_app
    restart: always
    env_file:
      - .env.production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    expose:
      - "5000"
    networks:
      - multicont_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Nginx Reverse Proxy
  nginx:
    image: nginx:1.25-alpine
    container_name: multicont_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - app
    networks:
      - multicont_network
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  multicont_network:
    driver: bridge
```

### 4. Nginx Configuration

**Archivo**: `nginx/nginx.conf`

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss 
               application/rss+xml font/truetype font/opentype 
               application/vnd.ms-fontobject image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_status 429;

    # Upstream Flask app
    upstream flask_app {
        least_conn;
        server app:5000 max_fails=3 fail_timeout=30s;
    }

    # HTTP Server (redirect to HTTPS)
    server {
        listen 80;
        server_name api.multicont.com;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name api.multicont.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # Security Headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Client body size limit
        client_max_body_size 10M;

        # API endpoints
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            
            proxy_pass http://flask_app;
            proxy_http_version 1.1;
            
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
            
            proxy_buffering off;
            proxy_request_buffering off;
        }

        # Health check (sin rate limit)
        location /health {
            proxy_pass http://flask_app/health;
            access_log off;
        }

        # Swagger UI
        location /api/docs {
            proxy_pass http://flask_app/api/docs;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files (si aplica)
        location /static/ {
            alias /app/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # Logs
        access_log /var/log/nginx/access.log main;
        error_log /var/log/nginx/error.log warn;
    }
}
```

---

## Configuración de Producción

### 1. Production Config Class

**Archivo**: `app/config.py` (añadir)

```python
class ProductionConfig(Config):
    """Configuración para ambiente de producción."""
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20
    }
    
    # Cache
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST', 'redis')
    CACHE_REDIS_PORT = int(os.environ.get('CACHE_REDIS_PORT', 6379))
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Logging
    LOG_LEVEL = 'INFO'
```

### 2. Health Check Endpoint

**Archivo**: `app/api/health_api.py`

```python
from flask import Blueprint, jsonify
from app import db

health_api = Blueprint('health_api', __name__)

@health_api.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint para load balancers y monitoring.
    
    Verifica:
    - Aplicación respondiendo
    - Conexión a base de datos
    - Redis (si está configurado)
    """
    try:
        # Verificar DB
        db.session.execute('SELECT 1')
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'cache': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503
```

### 3. Logging Configuration

**Archivo**: `app/__init__.py` (añadir)

```python
def configure_logging(app):
    """Configurar logging para producción."""
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Crear directorio de logs
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # File handler
        file_handler = RotatingFileHandler(
            'logs/multicont.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Multicont Flask API startup')
```

---

## Deployment con Docker Compose

### Paso a Paso

#### 1. Preparar Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version
```

#### 2. Clonar Repositorio

```bash
git clone https://github.com/wilk-17/app-multicont.git
cd app-multicont
```

#### 3. Configurar Variables de Entorno

```bash
# Copiar template
cp .env.example .env.production

# Editar con valores reales
nano .env.production

# Generar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 4. Build y Deploy

```bash
# Build de imágenes
docker-compose -f docker-compose.prod.yml build

# Iniciar servicios
docker-compose -f docker-compose.prod.yml up -d

# Verificar estado
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f app
```

#### 5. Verificar Deployment

```bash
# Health check
curl http://localhost/health

# API endpoint
curl http://localhost/api/quotes/

# Verificar containers
docker ps

# Ver logs de nginx
docker-compose -f docker-compose.prod.yml logs nginx
```

---

## CI/CD con GitHub Actions

### GitHub Actions Workflow

**Archivo**: `.github/workflows/deploy.yml`

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
        run: |
          pytest --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            your-dockerhub-user/multicont-api:latest
            your-dockerhub-user/multicont-api:${{ github.sha }}
          cache-from: type=registry,ref=your-dockerhub-user/multicont-api:buildcache
          cache-to: type=registry,ref=your-dockerhub-user/multicont-api:buildcache,mode=max
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            cd /var/www/app-multicont
            git pull origin main
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
            docker-compose -f docker-compose.prod.yml exec -T app flask db upgrade
```

### Secrets Requeridos en GitHub

```
DOCKER_USERNAME
DOCKER_PASSWORD
DEPLOY_HOST
DEPLOY_USER
DEPLOY_SSH_KEY
```

---

## Monitoring y Logging

### 1. Prometheus + Grafana (Opcional)

**Añadir a `docker-compose.prod.yml`**:

```yaml
  prometheus:
    image: prom/prometheus:latest
    container_name: multicont_prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - multicont_network

  grafana:
    image: grafana/grafana:latest
    container_name: multicont_grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - multicont_network
```

### 2. Application Metrics

**Instalar flask-prometheus-metrics**:

```bash
pip install prometheus-flask-exporter
```

**En `app/__init__.py`**:

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Métricas por endpoint
metrics.info('app_info', 'Application info', version='2.0.0')
```

### 3. Logs Centralizados

**Usar ELK Stack o servicio cloud**:
- **Elasticsearch**: Storage de logs
- **Logstash**: Procesamiento
- **Kibana**: Visualización

---

## Backup y Recuperación

### Script de Backup Automático

**Archivo**: `scripts/backup.sh`

```bash
#!/bin/bash
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="multicont_backup_$TIMESTAMP.sql"

# Backup de PostgreSQL
docker exec multicont_postgres pg_dump -U multicont_user multicont_prod > "$BACKUP_DIR/$BACKUP_FILE"

# Comprimir
gzip "$BACKUP_DIR/$BACKUP_FILE"

# Retener solo últimos 7 días
find $BACKUP_DIR -name "multicont_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

**Cron job (diario a las 2 AM)**:

```bash
0 2 * * * /var/www/app-multicont/scripts/backup.sh >> /var/log/multicont_backup.log 2>&1
```

### Restaurar Backup

```bash
# Descomprimir
gunzip multicont_backup_20250124_020000.sql.gz

# Restaurar
docker exec -i multicont_postgres psql -U multicont_user multicont_prod < multicont_backup_20250124_020000.sql
```

---

## Troubleshooting

### Problemas Comunes

#### 1. Contenedor app no inicia

```bash
# Ver logs
docker-compose -f docker-compose.prod.yml logs app

# Verificar variables de entorno
docker-compose -f docker-compose.prod.yml exec app env

# Entrar al contenedor
docker-compose -f docker-compose.prod.yml exec app /bin/bash
```

#### 2. Error de conexión a PostgreSQL

```bash
# Verificar que postgres esté healthy
docker-compose -f docker-compose.prod.yml ps

# Verificar conectividad
docker-compose -f docker-compose.prod.yml exec app nc -zv postgres 5432

# Ver logs de postgres
docker-compose -f docker-compose.prod.yml logs postgres
```

#### 3. Nginx 502 Bad Gateway

```bash
# Verificar que app esté respondiendo
docker-compose -f docker-compose.prod.yml exec app curl localhost:5000/health

# Ver logs de nginx
docker-compose -f docker-compose.prod.yml logs nginx

# Verificar configuración de nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

#### 4. Performance degradado

```bash
# Ver uso de recursos
docker stats

# Ver queries lentas en PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U multicont_user -d multicont_prod -c "SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Verificar cache hit rate
docker-compose -f docker-compose.prod.yml exec redis redis-cli INFO stats
```

### Comandos Útiles

```bash
# Reiniciar servicios
docker-compose -f docker-compose.prod.yml restart

# Ver logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f --tail=100

# Ejecutar migración manualmente
docker-compose -f docker-compose.prod.yml exec app flask db upgrade

# Shell de Python en contexto de app
docker-compose -f docker-compose.prod.yml exec app flask shell

# Limpiar containers y volúmenes huérfanos
docker system prune -a --volumes
```

---

## Checklist de Pre-deployment

- [ ] Variables de entorno configuradas en `.env.production`
- [ ] SECRET_KEY y JWT_SECRET_KEY generados aleatoriamente
- [ ] Contraseñas fuertes para PostgreSQL y Redis
- [ ] Certificados SSL configurados (Let's Encrypt recomendado)
- [ ] Backups automáticos configurados
- [ ] Monitoring setup (Prometheus + Grafana)
- [ ] Rate limiting configurado en Nginx
- [ ] CORS configurado apropiadamente
- [ ] Logs centralizados funcionando
- [ ] Health check respondiendo
- [ ] Migraciones de DB ejecutadas
- [ ] Tests pasando en CI/CD
- [ ] Documentación API actualizada
- [ ] Plan de rollback definido

---

**Fecha**: 2025-01-24
**Versión**: 2.0.0
**Autor**: Multicont Development Team
