# 服务器部署完整指南

<div align="center">

**将亚马逊广告智能投放平台部署到服务器**

适用于：云服务器（阿里云/腾讯云/华为云）、VPS、独立服务器

</div>

---

## 📋 目录

- [服务器要求](#服务器要求)
- [部署方式选择](#部署方式选择)
- [方式一：Docker部署（推荐）](#方式一docker部署推荐)
- [方式二：手动部署](#方式二手动部署)
- [域名与HTTPS配置](#域名与https配置)
- [性能优化](#性能优化)
- [运维管理](#运维管理)

---

## 服务器要求

### 最低配置

| 配置项 | 最低要求 | 推荐配置 |
|--------|---------|---------|
| CPU | 2核 | 4核+ |
| 内存 | 4GB | 8GB+ |
| 硬盘 | 40GB SSD | 100GB SSD |
| 带宽 | 3Mbps | 10Mbps+ |
| 系统 | Ubuntu 20.04/22.04 | Ubuntu 22.04 LTS |

### 推荐云服务商

- **阿里云** ECS实例
- **腾讯云** CVM实例
- **华为云** ECS实例
- **AWS** EC2实例

---

## 部署方式选择

| 方式 | 优点 | 缺点 | 适用场景 |
|-----|------|------|---------|
| Docker部署 | 快速、一致、易维护 | 需要学习Docker | 推荐生产环境 |
| 手动部署 | 灵活、可控 | 步骤多、易出错 | 需要定制化 |

---

## 方式一：Docker部署（推荐）

### 第一步：连接服务器

```bash
# 使用SSH连接服务器（Windows用户可用PuTTY或PowerShell）
ssh root@your_server_ip

# 或使用密钥
ssh -i your_key.pem root@your_server_ip
```

### 第二步：安装Docker

#### Ubuntu/Debian系统

```bash
# 更新软件包
apt update && apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装Docker Compose
apt install docker-compose-plugin -y

# 启动Docker并设置开机自启
systemctl start docker
systemctl enable docker

# 验证安装
docker --version
docker compose version
```

#### CentOS/RHEL系统

```bash
# 安装Docker
yum install -y yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动Docker
systemctl start docker
systemctl enable docker
```

### 第三步：准备项目

```bash
# 创建项目目录
mkdir -p /opt/amazon-ads
cd /opt/amazon-ads

# 方式A：从GitHub克隆
git clone https://github.com/Nuility/amzongtest-advertisement.git .

# 方式B：上传本地项目（在本地执行）
# scp -r C:/1/挑战杯/test1/* root@your_server_ip:/opt/amazon-ads/
```

### 第四步：配置环境变量

```bash
# 进入后端目录
cd backend

# 复制环境变量模板
cp .env.example .env

# 编辑配置文件
nano .env
```

#### 关键配置项修改

```bash
# ========== 应用配置 ==========
APP_NAME=Amazon Ads Intelligent Platform
DEBUG=False                    # 生产环境设为False

# ========== 数据库配置 ==========
# 使用Docker内置MySQL，无需修改
DATABASE_URL=mysql+pymysql://root:AmazonAds2024@mysql:3306/amazon_ads

# ========== Redis配置 ==========
# 使用Docker内置Redis，无需修改
REDIS_URL=redis://redis:6379/0

# ========== 安全配置 ==========
# ⚠️ 生产环境必须修改！生成方法：
# python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET_KEY=your-very-secure-secret-key-change-this-32chars

# ========== 日志配置 ==========
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE_PATH=/var/log/amazon-ads/app.log

# ========== 其他配置保持默认 ==========
```

**生成安全的JWT密钥**：

```bash
# 在服务器上执行
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 将输出的字符串复制到 .env 的 JWT_SECRET_KEY
```

### 第五步：修改Docker Compose配置

```bash
cd /opt/amazon-ads
nano docker-compose.yml
```

#### 生产环境配置示例

```yaml
version: '3.8'

services:
  # MySQL数据库
  mysql:
    image: mysql:8.0
    container_name: amazon-ads-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: AmazonAds2024    # 修改为强密码
      MYSQL_DATABASE: amazon_ads
      MYSQL_CHARSET: utf8mb4
    volumes:
      - mysql_data:/var/lib/mysql
      - ./backend/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - amazon-ads-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis缓存
  redis:
    image: redis:7-alpine
    container_name: amazon-ads-redis
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - amazon-ads-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # 后端API服务
  backend:
    build: ./backend
    container_name: amazon-ads-backend
    restart: always
    environment:
      - DATABASE_URL=mysql+pymysql://root:AmazonAds2024@mysql:3306/amazon_ads
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=False
    volumes:
      - ./backend/.env:/app/.env
      - backend_logs:/var/log/amazon-ads
    ports:
      - "8000:8000"
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - amazon-ads-network

  # 前端Web服务
  frontend:
    build: ./frontend
    container_name: amazon-ads-frontend
    restart: always
    ports:
      - "80:80"        # HTTP端口
      - "443:443"      # HTTPS端口（如果配置）
    depends_on:
      - backend
    networks:
      - amazon-ads-network

  # Celery Worker（异步任务）
  celery-worker:
    build: ./backend
    container_name: amazon-ads-celery-worker
    restart: always
    command: celery -A app.jobs.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=mysql+pymysql://root:AmazonAds2024@mysql:3306/amazon_ads
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    networks:
      - amazon-ads-network

  # Celery Beat（定时任务调度）
  celery-beat:
    build: ./backend
    container_name: amazon-ads-celery-beat
    restart: always
    command: celery -A app.jobs.celery_app beat --loglevel=info
    environment:
      - DATABASE_URL=mysql+pymysql://root:AmazonAds2024@mysql:3306/amazon_ads
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    networks:
      - amazon-ads-network

networks:
  amazon-ads-network:
    driver: bridge

volumes:
  mysql_data:
  redis_data:
  backend_logs:
```

### 第六步：配置防火墙

#### Ubuntu UFW防火墙

```bash
# 启用防火墙
ufw enable

# 开放必要端口
ufw allow 22/tcp      # SSH
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
ufw allow 8000/tcp    # API（可选，仅开发时开放）

# 查看状态
ufw status
```

#### 阿里云/腾讯云安全组

在云平台控制台配置安全组规则：

| 方向 | 端口范围 | 协议 | 说明 |
|-----|---------|------|------|
| 入方向 | 22 | TCP | SSH访问 |
| 入方向 | 80 | TCP | HTTP访问 |
| 入方向 | 443 | TCP | HTTPS访问 |
| 入方向 | 8000 | TCP | API访问（可选） |

### 第七步：启动服务

```bash
cd /opt/amazon-ads

# 构建镜像
docker compose build

# 启动所有服务
docker compose up -d

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 第八步：验证部署

```bash
# 检查服务健康状态
curl http://localhost:8000/health

# 检查前端
curl http://localhost:80

# 查看MySQL连接
docker exec -it amazon-ads-mysql mysql -uroot -pAmazonAds2024 -e "SHOW DATABASES;"
```

### 第九步：访问应用

- **前端界面**: `http://your_server_ip` 或 `http://your_domain.com`
- **后端API**: `http://your_server_ip:8000` 或 `http://api.your_domain.com`
- **API文档**: `http://your_server_ip:8000/docs`

---

## 方式二：手动部署

### 第一步：安装依赖

#### 安装Python

```bash
# Ubuntu
apt update
apt install -y python3.11 python3-pip python3-venv

# CentOS
yum install -y python3.11 python3-pip
```

#### 安装Node.js

```bash
# 使用nvm安装
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
```

#### 安装MySQL

```bash
# Ubuntu
apt install -y mysql-server

# 启动并设置开机自启
systemctl start mysql
systemctl enable mysql

# 安全配置
mysql_secure_installation
```

#### 安装Redis

```bash
apt install -y redis-server
systemctl start redis
systemctl enable redis
```

### 第二步：部署后端

```bash
cd /opt/amazon-ads/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install cryptography

# 配置环境变量
cp .env.example .env
nano .env  # 修改配置

# 初始化数据库
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 使用Gunicorn启动（推荐）
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 或使用systemd管理（推荐）
```

#### 创建systemd服务

```bash
nano /etc/systemd/system/amazon-ads-backend.service
```

```ini
[Unit]
Description=Amazon Ads Platform Backend
After=network.target mysql.service redis.service

[Service]
Type=notify
User=root
WorkingDirectory=/opt/amazon-ads/backend
Environment="PATH=/opt/amazon-ads/backend/venv/bin"
ExecStart=/opt/amazon-ads/backend/venv/bin/gunicorn \
  app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000 \
  --access-logfile /var/log/amazon-ads/access.log \
  --error-logfile /var/log/amazon-ads/error.log
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 创建日志目录
mkdir -p /var/log/amazon-ads

# 启动服务
systemctl daemon-reload
systemctl start amazon-ads-backend
systemctl enable amazon-ads-backend
```

### 第三步：部署前端

```bash
cd /opt/amazon-ads/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 安装Nginx
apt install -y nginx
```

#### 配置Nginx

```bash
nano /etc/nginx/sites-available/amazon-ads
```

```nginx
server {
    listen 80;
    server_name your_domain.com;  # 改为您的域名或IP
    
    # 前端静态文件
    location / {
        root /opt/amazon-ads/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    # API反向代理
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # API文档
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }
    
    location /redoc {
        proxy_pass http://localhost:8000/redoc;
    }
}
```

```bash
# 启用配置
ln -s /etc/nginx/sites-available/amazon-ads /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启Nginx
systemctl restart nginx
systemctl enable nginx
```

---

## 域名与HTTPS配置

### 配置域名（可选但推荐）

#### 1. 购买域名

推荐域名注册商：
- 阿里云万网
- 腾讯云DNSPod
- GoDaddy

#### 2. 域名解析

添加A记录：
```
类型: A记录
主机记录: @
记录值: your_server_ip
```

添加www记录：
```
类型: CNAME
主机记录: www
记录值: your_domain.com
```

#### 3. 申请免费SSL证书

使用Let's Encrypt免费证书：

```bash
# 安装Certbot
apt install -y certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your_domain.com -d www.your_domain.com

# 自动续期测试
certbot renew --dry-run

# 设置自动续期
crontab -e
# 添加以下行：
0 0 1 * * /usr/bin/certbot renew --quiet
```

#### 4. 强制HTTPS

修改Nginx配置：

```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your_domain.com www.your_domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
    
    # SSL优化配置
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;
    
    # 其他配置同上...
}
```

---

## 性能优化

### 1. MySQL优化

编辑MySQL配置：

```bash
nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

```ini
[mysqld]
# 连接数
max_connections = 200

# 缓冲池大小（建议为内存的70-80%）
innodb_buffer_pool_size = 2G

# 日志配置
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2

# 查询缓存
query_cache_size = 64M
query_cache_type = 1
```

### 2. Redis优化

```bash
nano /etc/redis/redis.conf
```

```conf
# 内存限制
maxmemory 1gb
maxmemory-policy allkeys-lru

# 持久化
appendonly yes
appendfsync everysec
```

### 3. Nginx优化

```nginx
# 在http块中添加
http {
    # Gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_min_length 1000;
    
    # 缓存配置
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m;
    
    # 连接优化
    keepalive_timeout 65;
    client_max_body_size 20M;
}
```

### 4. 后端优化

使用Gunicorn配置：

```bash
# 创建配置文件
nano /opt/amazon-ads/backend/gunicorn.conf.py
```

```python
# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1  # 推荐配置
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 120
```

---

## 运维管理

### 服务管理

```bash
# Docker方式
docker compose start          # 启动
docker compose stop           # 停止
docker compose restart        # 重启
docker compose logs -f        # 查看日志

# 手动部署方式
systemctl start amazon-ads-backend
systemctl stop amazon-ads-backend
systemctl restart amazon-ads-backend
systemctl status amazon-ads-backend
```

### 日志查看

```bash
# Docker方式
docker compose logs -f backend
docker compose logs -f frontend

# 手动方式
tail -f /var/log/amazon-ads/app.log
tail -f /var/log/nginx/access.log
```

### 数据备份

```bash
# MySQL备份
docker exec amazon-ads-mysql mysqldump -uroot -pAmazonAds2024 amazon_ads > backup_$(date +%Y%m%d).sql

# 或手动方式
mysqldump -uroot -p amazon_ads > backup_$(date +%Y%m%d).sql

# 定时备份（crontab）
0 2 * * * /usr/bin/mysqldump -uroot -ppassword amazon_ads > /backup/mysql_$(date +\%Y\%m\%d).sql
```

### 监控告警

#### 使用Prometheus + Grafana（推荐）

```yaml
# 添加到docker-compose.yml
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 常见问题

### 1. 端口被占用

```bash
# 查看端口占用
lsof -i :80
lsof -i :8000

# 结束进程
kill -9 <PID>
```

### 2. 权限问题

```bash
# 修改文件所有者
chown -R root:root /opt/amazon-ads
chmod -R 755 /opt/amazon-ads
```

### 3. 连接超时

检查防火墙和安全组配置，确保端口开放。

### 4. 内存不足

```bash
# 查看内存使用
free -h

# 查看进程内存
top

# 增加交换空间
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

---

## 部署检查清单

部署前请确认：

- [ ] 服务器配置满足最低要求
- [ ] 已安装Docker和Docker Compose
- [ ] 已配置环境变量（特别是JWT密钥）
- [ ] 已配置防火墙开放端口
- [ ] 已修改数据库密码
- [ ] DEBUG模式已关闭
- [ ] 域名已解析（如使用）
- [ ] SSL证书已配置（如使用HTTPS）

部署后验证：

- [ ] 所有容器正常运行
- [ ] 健康检查通过
- [ ] 前端页面可访问
- [ ] API接口可访问
- [ ] 数据库连接正常
- [ ] Redis连接正常

---

## 技术支持

如遇问题，请：
1. 查看日志排查错误
2. 查看 [docs/USER_MANUAL.md](docs/USER_MANUAL.md)
3. 在GitHub提Issue

---

**Amazon Ads Platform Team**  
**Powered by 华为云 CodeArts**
