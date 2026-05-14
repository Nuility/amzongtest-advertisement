
# 亚马逊广告智能投放平台 - 使用手册

<div align="center">

**完整的使用指南与操作说明**

版本：v1.0.0  
更新日期：2026-05-12

</div>

---

## 📑 目录

- [1. 系统概述](#1-系统概述)
  - [1.1 平台简介](#11-平台简介)
  - [1.2 技术架构](#12-技术架构)
  - [1.3 核心组件](#13-核心组件)
- [2. 运行前提](#2-运行前提)
  - [2.1 硬件要求](#21-硬件要求)
  - [2.2 软件要求](#22-软件要求)
  - [2.3 网络要求](#23-网络要求)
  - [2.4 权限要求](#24-权限要求)
- [3. 安装部署](#3-安装部署)
  - [3.1 环境准备](#31-环境准备)
  - [3.2 快速部署（推荐）](#32-快速部署推荐)
  - [3.3 验证部署](#33-验证部署)
  - [3.4 数据库初始化](#34-数据库初始化)
- [4. 配置说明](#4-配置说明)
  - [4.1 环境变量配置](#41-环境变量配置)
  - [4.2 关键配置说明](#42-关键配置说明)
  - [4.3 Docker配置](#43-docker配置)
- [5. 使用方法](#5-使用方法)
  - [5.1 启动服务](#51-启动服务)
  - [5.2 停止服务](#52-停止服务)
  - [5.3 重启服务](#53-重启服务)
  - [5.4 访问应用](#54-访问应用)
  - [5.5 查看日志](#55-查看日志)
  - [5.6 数据备份](#56-数据备份)
- [6. 功能说明](#6-功能说明)
  - [6.1 主要功能模块](#61-主要功能模块)
  - [6.2 用户操作流程](#62-用户操作流程)
- [7. API使用指南](#7-api使用指南)
  - [7.1 API认证](#71-api认证)
  - [7.2 主要API端点](#72-主要api端点)
  - [7.3 错误处理](#73-错误处理)
- [8. 常见问题](#8-常见问题)
  - [8.1 安装部署问题](#81-安装部署问题)
  - [8.2 运行使用问题](#82-运行使用问题)
- [9. 故障排查](#9-故障排查)
  - [9.1 服务状态检查](#91-服务状态检查)
  - [9.2 日志查看](#92-日志查看)
  - [9.3 性能监控](#93-性能监控)
  - [9.4 常见故障处理流程](#94-常见故障处理流程)
- [附录](#附录)

---

## 1. 系统概述

### 1.1 平台简介

亚马逊广告智能投放平台是一个企业级的广告自动化管理系统，基于华为云 CodeArts 开发，帮助跨境电商卖家实现：

- **智能竞价管理** - 自动调整关键词出价，优化ACoS
- **关键词智能推荐** - 基于算法推荐高潜力关键词
- **实时数据分析** - 全面的指标计算和可视化展示
- **团队协作管理** - 多账号、多团队管理支持

### 1.2 技术架构

```
┌─────────────────────────────────────┐
│     前端 (React + TypeScript)        │
│         Ant Design + ECharts         │
└──────────────┬──────────────────────┘
               │ HTTP/REST
┌──────────────┴──────────────────────┐
│     后端 (FastAPI + Python 3.13)     │
│         SQLAlchemy + Celery          │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│     数据层 (MySQL + Redis)            │
└─────────────────────────────────────┘
```

### 1.3 核心组件

| 组件 | 技术 | 版本 | 说明 |
|-----|------|------|------|
| 后端框架 | FastAPI | 0.136+ | 高性能异步Web框架 |
| 数据库 | MySQL | 8.0 | 业务数据存储 |
| 缓存 | Redis | 7.0 | 缓存和消息队列 |
| 任务队列 | Celery | 5.6+ | 异步任务处理 |
| 前端框架 | React | 18+ | UI组件库 |
| 容器化 | Docker | 最新 | 应用容器化 |

---

## 2. 运行前提

### 2.1 硬件要求

| 资源 | 最低配置 | 推荐配置 |
|-----|---------|---------|
| CPU | 2核 | 4核+ |
| 内存 | 4GB | 8GB+ |
| 硬盘 | 20GB | 50GB+ |
| 网络 | 10Mbps | 100Mbps+ |

### 2.2 软件要求

#### 必需软件

| 软件 | 版本要求 | 说明 |
|-----|---------|------|
| Python | 3.13+ | 后端运行环境 |
| Docker Desktop | 最新版 | 容器运行环境 |
| Docker Compose | v5.0+ | 多容器编排工具 |

#### 可选软件

| 软件 | 版本 | 用途 |
|-----|------|------|
| Node.js | 18+ | 前端本地开发 |
| Git | 最新 | 版本控制 |
| MySQL Workbench | 8.0 | 数据库管理 |

### 2.3 网络要求

- **端口占用检查**
  - 3000: 前端应用
  - 8000: 后端API
  - 3306: MySQL数据库
  - 6379: Redis缓存

- **防火墙配置**
  ```bash
  # Windows防火墙开放端口
  netsh advfirewall firewall add rule name="Amazon Ads Platform" dir=in action=allow protocol=tcp localport=3000,8000,3306,6379
  ```

### 2.4 权限要求

- **Windows**: 管理员权限（安装Docker）
- **数据库**: root用户或具有CREATE、INSERT、UPDATE、DELETE权限的用户
- **文件系统**: 项目目录读写权限

---

## 3. 安装部署

### 3.1 环境准备

#### 步骤1：安装Docker Desktop

1. 下载Docker Desktop: https://www.docker.com/products/docker-desktop
2. 安装并启动Docker Desktop
3. 验证安装
   ```bash
   docker --version
   docker-compose --version
   ```

#### 步骤2：安装Python

1. 下载Python 3.13: https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"
3. 验证安装
   ```bash
   python --version
   pip --version
   ```

#### 步骤3：获取项目代码

```bash
# 克隆项目（如果使用Git）
git clone <repository-url>
cd amazon-ads-platform

# 或直接解压项目压缩包
```

### 3.2 快速部署（推荐）

#### 方式A：Docker部署（完整服务）

```bash
# 1. 进入项目目录
cd amazon-ads-platform

# 2. 启动基础服务（MySQL + Redis）
docker-compose up -d mysql redis

# 3. 等待服务启动（约30秒）
docker-compose ps

# 4. 安装后端依赖
cd backend
pip install -r requirements.txt
pip install cryptography

# 5. 配置环境变量
cp .env.example .env
# 编辑.env文件，设置DEBUG=True

# 6. 启动后端
python run.py

# 7. 构建并启动前端（新终端）
cd ..
docker build -t amazon-ads-frontend ./frontend
docker run -d --name frontend -p 3000:4173 amazon-ads-frontend
```

#### 方式B：本地开发部署

```bash
# 1. 启动基础服务
docker-compose up -d mysql redis

# 2. 后端部署
cd backend
pip install -r requirements.txt
pip install cryptography
cp .env.example .env
python run.py

# 3. 前端部署（新终端，需安装Node.js）
cd frontend
npm install
npm run dev
```

### 3.3 验证部署

#### 检查服务状态

```bash
# 查看Docker容器
docker ps

# 预期输出：
# test1-mysql-1    Up      0.0.0.0:3306->3306/tcp
# test1-redis-1    Up      0.0.0.0:6379->6379/tcp
```

#### 测试服务连接

```bash
# 测试后端API
curl http://localhost:8000/health
# 预期输出：{"status":"healthy"}

# 测试前端访问
curl http://localhost:3000
# 预期输出：HTML页面内容
```

#### 运行测试套件

```bash
cd backend
pytest
# 预期输出：37 passed
```

### 3.4 数据库初始化

```bash
# 连接MySQL创建数据库
docker exec -it test1-mysql-1 mysql -u root -ppassword

# 在MySQL中执行
CREATE DATABASE IF NOT EXISTS amazon_ads;
USE amazon_ads;

# 执行迁移（如果配置了Alembic）
cd backend
alembic upgrade head
```

---

## 4. 配置说明

### 4.1 环境变量配置

配置文件位置：`backend/.env`

#### 完整配置示例

```bash
# ========== 应用配置 ==========
APP_NAME=Amazon Ads Intelligent Platform
APP_VERSION=1.0.0
DEBUG=True                          # 开发环境设为True，生产环境设为False

# ========== 数据库配置 ==========
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/amazon_ads
DATABASE_POOL_SIZE=50               # 连接池大小
DATABASE_MAX_OVERFLOW=100           # 最大溢出连接数
DATABASE_POOL_TIMEOUT=30            # 连接超时时间(秒)
DATABASE_POOL_RECYCLE=3600          # 连接回收时间(秒)

# ========== Redis配置 ==========
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=100           # 最大连接数
REDIS_SOCKET_TIMEOUT=5              # Socket超时(秒)

# ========== ClickHouse配置（可选） ==========
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_DB=amazon_ads

# ========== Amazon API配置 ==========
AMAZON_ADS_API_BASE=https://advertising-api.amazon.com
AMAZON_SP_API_BASE=https://sellingpartnerapi-na.amazon.com
AMAZON_API_TIMEOUT=30               # API超时时间(秒)
AMAZON_API_MAX_RETRIES=3            # 最大重试次数

# ========== 安全配置 ==========
JWT_SECRET_KEY=your-secret-key-change-in-production  # 生产环境必须修改
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30               # Token过期时间(分钟)

# ========== Celery配置 ==========
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json

# ========== 日志配置 ==========
LOG_LEVEL=INFO                      # 日志级别：DEBUG/INFO/WARNING/ERROR
LOG_FORMAT=json                     # 日志格式：json/text
LOG_FILE_PATH=                      # 日志文件路径，留空则不写文件

# ========== 缓存配置 ==========
CACHE_DEFAULT_TTL=300               # 默认缓存时间(秒)
CACHE_MAX_TTL=3600                  # 最大缓存时间(秒)
CACHE_SLOW_QUERY_THRESHOLD=1.0      # 慢查询阈值(秒)

# ========== 性能配置 ==========
PERFORMANCE_SLOW_REQUEST_THRESHOLD=1.0  # 慢请求阈值(秒)
```

### 4.2 关键配置说明

#### DEBUG模式
- **开发环境**: `DEBUG=True` - 跳过JWT密钥验证，显示详细错误信息
- **生产环境**: `DEBUG=False` - 强制要求修改JWT密钥

#### JWT密钥生成

```bash
# 生成安全的JWT密钥
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 将生成的密钥设置到.env文件
JWT_SECRET_KEY=<生成的密钥>
```

#### 数据库连接配置

```bash
# 格式
DATABASE_URL=mysql+pymysql://用户名:密码@主机:端口/数据库名

# 示例
DATABASE_URL=mysql+pymysql://root:mypassword@localhost:3306/amazon_ads
```

### 4.3 Docker配置

#### docker-compose.yml配置

主要服务配置：

```yaml
services:
  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=amazon_ads

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

#### 自定义配置

修改MySQL密码：
```yaml
environment:
  - MYSQL_ROOT_PASSWORD=your_new_password
```

修改端口映射：
```yaml
ports:
  - "13306:3306"  # 外部端口13306映射到内部3306
```

---

## 5. 使用方法

### 5.1 启动服务

#### 完整启动流程

```bash
# 1. 启动基础服务
docker-compose up -d mysql redis

# 2. 启动后端（后台运行）
cd backend
python run.py

# 3. 启动前端（新终端）
# 方式A：Docker方式
docker start frontend

# 方式B：本地方式
cd frontend
npm run dev
```

#### 使用systemd管理（Linux）

创建服务文件 `/etc/systemd/system/amazon-ads-backend.service`:

```ini
[Unit]
Description=Amazon Ads Platform Backend
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/amazon-ads-platform/backend
ExecStart=/usr/bin/python3 run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start amazon-ads-backend
sudo systemctl enable amazon-ads-backend
```

### 5.2 停止服务

```bash
# 停止后端
# 在运行python run.py的终端按 Ctrl+C

# 停止前端容器
docker stop frontend

# 停止基础服务
docker-compose stop mysql redis

# 停止并删除所有容器
docker-compose down
```

### 5.3 重启服务

```bash
# 重启后端
# Ctrl+C 停止后重新运行
python run.py

# 重启前端
docker restart frontend

# 重启基础服务
docker-compose restart mysql redis
```

### 5.4 访问应用

启动成功后，通过浏览器访问：

| 服务 | 地址 | 说明 |
|-----|------|------|
| 前端界面 | http://localhost:3000 | 用户操作界面 |
| 后端API | http://localhost:8000 | API服务 |
| API文档 | http://localhost:8000/docs | Swagger交互文档 |
| API文档 | http://localhost:8000/redoc | ReDoc文档 |
| 健康检查 | http://localhost:8000/health | 服务健康状态 |

### 5.5 查看日志

#### 后端日志

```bash
# 实时查看日志（如果配置了日志文件）
tail -f /var/log/amazon-ads/app.log

# 查看Docker日志
docker logs test1-mysql-1
docker logs test1-redis-1
```

#### 前端日志

```bash
# Docker方式
docker logs frontend

# 本地方式
# 在运行npm run dev的终端查看
```

### 5.6 数据备份

#### MySQL备份

```bash
# 备份数据库
docker exec test1-mysql-1 mysqldump -u root -ppassword amazon_ads > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker exec -i test1-mysql-1 mysql -u root -ppassword amazon_ads < backup_20260512.sql
```

#### Redis备份

```bash
# 触发RDB快照
docker exec test1-redis-1 redis-cli BGSAVE

# 复制备份文件
docker cp test1-redis-1:/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb
```

---

## 6. 功能说明

### 6.1 主要功能模块

#### 1. 指标计算与分析

**功能描述**: 自动计算和分析广告关键指标

**支持指标**:
- 流量指标: Impressions（展示量）、Clicks（点击量）、CTR（点击率）
- 成本指标: CPC（平均点击成本）、Spend（总花费）
- 转化指标: Orders（订单量）、CVR（转化率）
- KPI指标: ACoS（广告销售成本比）、ROAS（投资回报率）

**使用场景**:
- 查看广告活动整体表现
- 分析关键词效果
- 生成数据报表

#### 2. 智能竞价引擎

**功能描述**: 基于策略自动调整关键词出价

**支持策略**:

**ACoS目标策略**
- 原理: 根据实际ACoS与目标值的偏差调整出价
- 规则:
  - ACoS > 目标×1.2 → 降低出价10%
  - ACoS < 目标×0.8 → 提高出价10%
  - ACoS在目标范围内 → 保持不变

**CVR优化策略**
- 原理: 基于转化率优化出价
- 规则:
  - CVR > 平均×1.5 → 提高出价15%
  - CVR < 平均×0.5 → 降低出价22.5%

**风险控制**:
- 最大调整幅度: ±30%
- 冷却期: 24小时
- 最小点击量要求: 10次（ACoS策略）、20次（CVR策略）

#### 3. 关键词管理

**功能描述**: 智能关键词推荐和否定词管理

**关键词推荐**:
- 基于ASIN分析推荐相关关键词
- 计算推荐得分（0-1分）
- 提供建议出价

**否定词管理**:
- 自动识别低效关键词
- 批量添加否定词
- 否定词效果追踪

#### 4. 数据可视化

**功能描述**: 实时数据看板和多维度分析

**看板内容**:
- 总花费、销售额统计
- ACoS、ROAS概览
- 趋势分析图表
- 同比/环比对比
- SKU单品分析

### 6.2 用户操作流程

#### 广告活动分析流程

```
1. 登录系统
   ↓
2. 选择广告账号
   ↓
3. 设置查询时间范围
   ↓
4. 查看广告活动指标
   ↓
5. 分析关键词表现
   ↓
6. 导出数据报表
```

#### 竞价优化流程

```
1. 选择关键词
   ↓
2. 选择竞价策略
   - ACoS目标策略
   - CVR优化策略
   ↓
3. 设置目标参数
   - 目标ACoS值
   - 或平均CVR值
   ↓
4. 执行竞价调整
   ↓
5. 查看调整结果
   ↓
6. 监控效果变化
```

---

## 7. API使用指南

### 7.1 API认证

当前版本API认证已配置JWT，但在DEBUG模式下可以跳过认证。

#### 获取Token（生产环境）

```bash
# 登录获取token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

#### 使用Token

```bash
# 在请求头中添加token
curl http://localhost:8000/metrics/campaigns \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 7.2 主要API端点

#### 指标查询API

**查询广告活动指标**
```bash
GET /metrics/campaigns?account_id=acc_123&start_date=2024-01-01&end_date=2024-01-31

# 响应示例
[
  {
    "entity_id": "camp_001",
    "entity_name": "夏季促销活动",
    "entity_type": "campaign",
    "impressions": 10000,
    "clicks": 500,
    "ctr": 0.05,
    "cpc": 0.8,
    "spend": 400.0,
    "orders": 50,
    "sales": 2500.0,
    "cvr": 0.1,
    "acos": 0.16,
    "roas": 6.25
  }
]
```

**查询关键词指标**
```bash
GET /metrics/keywords?campaign_id=camp_123&start_date=2024-01-01&end_date=2024-01-31
```

**获取看板概览**
```bash
GET /metrics/dashboard/overview?account_id=acc_123&start_date=2024-01-01&end_date=2024-01-31
```

#### 竞价策略API

**执行竞价策略**
```bash
POST /bidding/execute
Content-Type: application/json

{
  "strategy_name": "acos_target",
  "keyword_ids": ["kw_1", "kw_2", "kw_3"],
  "target_acos": 0.25
}

# 响应示例
[
  {
    "keyword_id": "kw_1",
    "old_bid": 1.0,
    "new_bid": 1.1,
    "reason": "ACoS adjustment",
    "timestamp": "2024-01-15T10:30:00"
  }
]
```

**查询竞价历史**
```bash
GET /bidding/logs?account_id=acc_123&limit=100
```

#### 关键词管理API

**获取关键词推荐**
```bash
GET /keywords/recommend?asin=B08N5WRWNW&limit=20
```

**添加否定关键词**
```bash
POST /keywords/negative
Content-Type: application/json

["kw_1", "kw_2"]
```

**查询否定关键词**
```bash
GET /keywords/negative?campaign_id=camp_123
```

**移除否定关键词**
```bash
DELETE /keywords/negative?keyword_id=kw_1
```

### 7.3 错误处理

#### 错误响应格式

```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Invalid parameter value",
  "details": {"field": "start_date", "reason": "Invalid date format"},
  "request_id": "uuid-1234-5678",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### 常见错误码

| 错误码 | HTTP状态码 | 说明 | 解决方法 |
|--------|-----------|------|---------|
| `DATABASE_ERROR` | 503 | 数据库操作失败 | 检查数据库连接和状态 |
| `VALIDATION_ERROR` | 422 | 参数校验失败 | 检查请求参数格式 |
| `NOT_FOUND` | 404 | 资源不存在 | 检查资源ID是否正确 |
| `EXTERNAL_API_ERROR` | 502 | 外部API调用失败 | 检查网络连接和API配置 |
| `BUSINESS_ERROR` | 400 | 业务规则校验失败 | 检查业务逻辑条件 |
| `BID_OUT_OF_RANGE` | 400 | 竞价超出允许范围 | 调整竞价到合理范围 |

---

## 8. 常见问题

### 8.1 安装部署问题

#### Q1: Docker启动失败

**现象**: 执行`docker-compose up -d`失败

**原因**: Docker Desktop未启动或端口被占用

**解决**:
```bash
# 1. 确保Docker Desktop已启动
# Windows: 检查右下角Docker图标

# 2. 检查端口占用
netstat -ano | findstr :3306
netstat -ano | findstr :6379

# 3. 结束占用端口的进程
taskkill /PID <进程ID> /F
```

#### Q2: pip安装依赖失败

**现象**: 安装requirements.txt时报错

**原因**: Python版本不兼容或网络问题

**解决**:
```bash
# 1. 确认Python版本
python --version  # 需要3.13+

# 2. 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 逐个安装问题包
pip install <package_name>
```

#### Q3: MySQL连接失败

**现象**: 连接数据库报错

**原因**: 容器未启动或密码错误

**解决**:
```bash
# 1. 检查容器状态
docker ps | grep mysql

# 2. 重启容器
docker-compose restart mysql

# 3. 检查密码
# 默认密码在docker-compose.yml中设置
```

#### Q4: 前端访问空白

**现象**: 访问localhost:3000显示空白

**原因**: 前端构建失败或端口映射错误

**解决**:
```bash
# 1. 检查容器日志
docker logs frontend

# 2. 重新构建前端
docker build -t amazon-ads-frontend ./frontend
docker run -d --name frontend -p 3000:4173 amazon-ads-frontend

# 3. 确认端口映射正确
docker ps
```

### 8.2 运行使用问题

#### Q5: API返回500错误

**现象**: 请求API返回500状态码

**原因**: 后端服务异常或数据库错误

**解决**:
```bash
# 1. 查看后端日志
# 在运行python run.py的终端查看错误信息

# 2. 检查数据库连接
curl http://localhost:8000/health

# 3. 重启后端服务
# Ctrl+C 停止后重新运行
python run.py
```

#### Q6: 测试失败

**现象**: pytest运行失败

**原因**: 环境配置不正确

**解决**:
```bash
# 1. 确认环境变量
cat backend/.env

# 2. 确认依赖完整
pip list | grep pytest

# 3. 运行详细输出
pytest -v --tb=long
```

#### Q7: Redis连接超时

**现象**: 提示Redis连接超时

**原因**: Redis服务未运行

**解决**:
```bash
# 1. 检查Redis容器
docker ps | grep redis

# 2. 启动Redis
docker-compose up -d redis

# 3. 测试连接
docker exec -it test1-redis-1 redis-cli ping
```

---

## 9. 故障排查

### 9.1 服务状态检查

#### 完整检查脚本

```bash
#!/bin/bash

echo "=== 服务状态检查 ==="

# 检查Docker
echo -e "\n[Docker状态]"
docker --version
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 检查Python
echo -e "\n[Python版本]"
python --version

# 检查端口
echo -e "\n[端口占用]"
netstat -ano | findstr ":3000 :8000 :3306 :6379"

# 检查API
echo -e "\n[API健康检查]"
curl -s http://localhost:8000/health || echo "后端API未响应"

# 检查前端
echo -e "\n[前端检查]"
curl -s http://localhost:3000 > /dev/null && echo "前端正常" || echo "前端未响应"

# 检查数据库
echo -e "\n[数据库连接]"
docker exec test1-mysql-1 mysqladmin ping -u root -ppassword 2>/dev/null || echo "数据库未响应"

# 检查Redis
echo -e "\n[Redis连接]"
docker exec test1-redis-1 redis-cli ping || echo "Redis未响应"
```

### 9.2 日志查看

#### 后端日志

```bash
# 实时日志
# 在运行python run.py的终端查看

# 如果配置了日志文件
tail -f /var/log/amazon-ads/app.log

# 查看最近100行
tail -n 100 /var/log/amazon-ads/app.log
```

#### Docker日志

```bash
# MySQL日志
docker logs test1-mysql-1 --tail 100

# Redis日志
docker logs test1-redis-1 --tail 100

# 前端日志
docker logs frontend --tail 100
```

### 9.3 性能监控

#### 系统资源监控

```bash
# 查看容器资源使用
docker stats

# 查看进程资源
# Windows: 任务管理器
# Linux: top 或 htop
```

#### 数据库性能

```bash
# 连接MySQL
docker exec -it test1-mysql-1 mysql -u root -ppassword

# 查看连接数
SHOW STATUS LIKE 'Threads_connected';

# 查看慢查询
SHOW VARIABLES LIKE 'slow_query%';
```

#### Redis性能

```bash
# 连接Redis
docker exec -it test1-redis-1 redis-cli

# 查看信息
INFO

# 查看内存使用
INFO memory
```

### 9.4 常见故障处理流程

#### 后端无法启动

```
1. 检查Python版本
   ↓
2. 检查依赖是否完整
   pip install -r requirements.txt
   ↓
3. 检查环境变量配置
   cat .env
   ↓
4. 检查数据库连接
   curl localhost:8000/health
   ↓
5. 查看错误日志
   python run.py
```

#### 数据库连接失败

```
1. 检查MySQL容器状态
   docker ps | grep mysql
   ↓
2. 重启MySQL容器
   docker-compose restart mysql
   ↓
3. 检查连接配置
   DATABASE_URL in .env
   ↓
4. 测试连接
   docker exec -it test1-mysql-1 mysql -u root -ppassword
```

#### API响应缓慢

```
1. 检查系统资源
   docker stats
   ↓
2. 检查数据库性能
   - 连接数
   - 慢查询
   ↓
3. 检查缓存命中率
   docker exec -it test1-redis-1 redis-cli INFO stats
   ↓
4. 优化配置
   - 增加连接池大小
   - 启用缓存
   - 添加索引
```

---

## 附录

### A. 快速命令参考

```bash
# 完整启动
docker-compose up -d mysql redis
cd backend && pip install -r requirements.txt && pip install cryptography
python run.py

# 完整停止
docker-compose down
# Ctrl+C 停止后端

# 查看状态
docker ps
curl localhost:8000/health

# 查看日志
docker logs <container_name>
tail -f /var/log/amazon-ads/app.log

# 运行测试
cd backend && pytest

# 备份数据
docker exec test1-mysql-1 mysqldump -u root -ppassword amazon_ads > backup.sql
```

### B. 目录结构

```
amazon-ads-platform/
├── backend/              # 后端服务
│   ├── app/             # 应用代码
│   ├── tests/           # 测试文件
│   ├── requirements.txt # 依赖列表
│   ├── .env            # 环境配置
│   └── run.py          # 启动脚本
├── frontend/            # 前端应用
│   ├── src/            # 源代码
│   ├── package.json    # 依赖配置
│   └── Dockerfile      # 容器配置
├── docs/               # 文档目录
│   └── USER_MANUAL.md  # 本手册
├── docker-compose.yml  # Docker编排
└── README.md          # 项目说明
```

### C. 技术支持

- **项目文档**: 查看README.md和docs目录
- **API文档**: http://localhost:8000/docs
- **问题反馈**: 提交Issue到项目仓库
- **代码质量报告**: 查看`doc/summary260512.md`

---

**文档版本**: v1.0.0  
**最后更新**: 2026-05-12  
**维护团队**: 亚马逊广告平台团队  
**技术支持**: 华为云 CodeArts
