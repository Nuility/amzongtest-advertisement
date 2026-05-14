# 亚马逊广告智能投放平台

<div align="center">

**基于华为云 CodeArts 的智能广告投放与团队管理平台**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 项目简介

亚马逊广告智能投放平台是一个企业级的广告自动化管理系统，旨在帮助跨境电商卖家、广告代理公司和品牌出海团队实现：

- **提升广告ROI** - 通过智能调价策略优化投入产出比
- **降低人工成本** - 自动化关键词挖掘、调价、否定词管理
- **实现运营标准化** - 策略模板化，经验可复制
- **支持规模化增长** - 多账号、多站点、多品牌管理

### 核心价值

本平台通过以下方式提升广告投放效率：

1. **智能竞价调整** - 基于ACoS、CVR等指标自动调整关键词出价
2. **关键词智能推荐** - 基于历史数据和算法推荐高潜力关键词
3. **实时数据分析** - 全面的指标计算和可视化展示
4. **自动化运营** - 减少人工干预，提升运营效率

---

## 🎯 核心功能

### 1. 指标计算与分析

自动计算和分析关键广告指标：

- **流量指标**: Impressions（展示量）、Clicks（点击量）、CTR（点击率）
- **成本指标**: CPC（平均点击成本）、Spend（总花费）
- **转化指标**: Orders（订单量）、CVR（转化率）
- **KPI指标**: ACoS（广告销售成本比）、ROAS（投资回报率）、TACoS（总广告销售成本比）

**API端点**:
- `GET /metrics/campaigns` - 查询广告活动指标
- `GET /metrics/keywords` - 查询关键词指标
- `GET /metrics/dashboard/overview` - 获取看板概览数据

### 2. 自动调价引擎

基于多种策略自动调整关键词出价：

- **ACoS目标策略** - 根据实际ACoS与目标值的偏差调整出价
  - ACoS > 目标×1.2 → 降低出价10%
  - ACoS < 目标×0.8 → 提高出价10%
  
- **CVR优化策略** - 基于转化率优化出价
  - CVR > 平均×1.5 → 提高出价15%
  - CVR < 平均×0.5 → 降低出价22.5%

- **风险控制机制**
  - 最大调整幅度限制（±30%）
  - 冷却期限制（24小时）
  - 数据量阈值验证

**API端点**:
- `POST /bidding/execute` - 执行竞价策略
- `GET /bidding/logs` - 查询竞价历史日志
- `GET /bidding/strategies` - 获取可用策略列表

### 3. 关键词智能管理

智能关键词推荐和否定词管理：

- **关键词推荐**
  - 基于ASIN分析推荐相关关键词
  - 计算推荐得分（0-1分）
  - 提供建议出价
  
- **否定词管理**
  - 自动识别低效关键词
  - 批量添加否定词
  - 否定词效果追踪

**API端点**:
- `GET /keywords/recommend` - 获取关键词推荐
- `POST /keywords/negative` - 添加否定关键词
- `GET /keywords/negative` - 查询否定关键词列表
- `DELETE /keywords/negative` - 移除否定关键词

### 4. BI数据可视化

实时数据看板和多维度分析：

- **实时看板** - 总花费、销售额、ACoS、ROAS概览
- **趋势分析** - 时间序列趋势图、同比/环比对比
- **SKU分析** - 单品盈利能力分析、投放建议

### 5. 团队管理与绩效

多团队协作和绩效追踪：

- **KPI配置** - 多维度目标设定
- **绩效计算** - 自动计算达成率和绩效分数
- **人效分析** - 运营人员工作量统计

---

## 🏗️ 技术架构

### 系统架构

```
┌─────────────────────────────────────┐
│     Frontend (React + TypeScript)    │
│         Ant Design + ECharts         │
└──────────────┬──────────────────────┘
               │ HTTP/REST
┌──────────────┴──────────────────────┐
│     Backend (FastAPI + Python)       │
├──────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐     │
│  │ API Layer  │  │ Middleware │     │
│  └────────────┘  └────────────┘     │
│  ┌────────────┐  ┌────────────┐     │
│  │  Service   │  │    Agent    │     │
│  └────────────┘  └────────────┘     │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│          Data Layer                  │
├──────────────────────────────────────┤
│  MySQL  │  Redis  │  ClickHouse      │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│       External APIs                  │
├──────────────────────────────────────┤
│  Amazon Ads API  │  SP-API           │
└──────────────────────────────────────┘
```

### 技术栈

**后端**:
- **FastAPI** - 现代高性能Web框架
- **SQLAlchemy** - ORM框架
- **Pydantic** - 数据验证
- **Celery** - 异步任务队列
- **Redis** - 缓存和消息队列
- **MySQL** - 业务数据存储
- **ClickHouse** - 分析数据存储

**前端**:
- **React 18** - UI框架
- **TypeScript** - 类型安全
- **Ant Design 5** - UI组件库
- **ECharts** - 数据可视化
- **Zustand** - 状态管理
- **TanStack Query** - 数据请求

**基础设施**:
- **Docker** - 容器化
- **Kubernetes** - 容器编排
- **华为云 CCE** - 云容器引擎

---

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 7+
- Docker & Docker Compose（可选）

### 方式一：Docker Compose（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd amazon-ads-platform
```

2. **配置环境变量**
```bash
cp backend/.env.example backend/.env
# 编辑 .env 文件，配置数据库、Redis等连接信息
```

3. **启动所有服务**
```bash
docker-compose up -d
```

4. **查看服务状态**
```bash
docker-compose ps
```

5. **访问应用**
- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- API文档(Swagger): http://localhost:8000/docs
- API文档(ReDoc): http://localhost:8000/redoc

### 方式二：本地开发

#### 后端开发

1. **创建虚拟环境**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件
```

4. **启动开发服务器**
```bash
python run.py
```

后端服务将在 http://localhost:8000 启动

#### 前端开发

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```

前端应用将在 http://localhost:3000 启动

---

## ⚙️ 配置说明

### 环境变量配置

创建 `backend/.env` 文件，配置以下环境变量：

```bash
# ========== 应用配置 ==========
APP_NAME=Amazon Ads Intelligent Platform
DEBUG=False

# ========== 数据库配置 ==========
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/amazon_ads
DATABASE_POOL_SIZE=50
DATABASE_MAX_OVERFLOW=100
DATABASE_POOL_TIMEOUT=30
DATABASE_POOL_RECYCLE=3600

# ========== Redis配置 ==========
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=100
REDIS_SOCKET_TIMEOUT=5

# ========== ClickHouse配置 ==========
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_DB=amazon_ads

# ========== Amazon API配置 ==========
AMAZON_ADS_API_BASE=https://advertising-api.amazon.com
AMAZON_SP_API_BASE=https://sellingpartnerapi-na.amazon.com
AMAZON_API_TIMEOUT=30
AMAZON_API_MAX_RETRIES=3

# ========== 安全配置 ==========
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# ========== Celery配置 ==========
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ========== 日志配置 ==========
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE_PATH=/var/log/amazon-ads/app.log

# ========== 缓存配置 ==========
CACHE_DEFAULT_TTL=300
CACHE_MAX_TTL=3600
CACHE_SLOW_QUERY_THRESHOLD=1.0

# ========== 性能配置 ==========
PERFORMANCE_SLOW_REQUEST_THRESHOLD=1.0
```

### 重要配置说明

1. **JWT_SECRET_KEY**: 生产环境必须修改为强密码
2. **DATABASE_URL**: 数据库连接字符串，包含用户名和密码
3. **REDIS_URL**: Redis连接字符串
4. **LOG_FORMAT**: 日志格式，可选 `json` 或 `text`
5. **CACHE_DEFAULT_TTL**: 缓存默认过期时间（秒）

---

## 📚 API文档

### Swagger UI

启动后端服务后，访问 http://localhost:8000/docs 查看交互式API文档

### 主要API端点

#### 指标查询

```bash
# 查询广告活动指标
GET /metrics/campaigns?account_id=acc_123&start_date=2024-01-01&end_date=2024-01-31

# 查询关键词指标
GET /metrics/keywords?campaign_id=camp_123&start_date=2024-01-01&end_date=2024-01-31

# 获取看板概览
GET /metrics/dashboard/overview?account_id=acc_123&start_date=2024-01-01&end_date=2024-01-31
```

#### 竞价策略

```bash
# 执行ACoS目标策略
POST /bidding/execute
Content-Type: application/json

{
  "strategy_name": "acos_target",
  "keyword_ids": ["kw_1", "kw_2", "kw_3"],
  "target_acos": 0.25
}

# 查询竞价历史
GET /bidding/logs?account_id=acc_123&limit=100
```

#### 关键词管理

```bash
# 获取关键词推荐
GET /keywords/recommend?asin=B08N5WRWNW&limit=20

# 添加否定关键词
POST /keywords/negative
Content-Type: application/json

["kw_1", "kw_2"]
```

### 错误响应格式

所有API错误返回统一格式：

```json
{
  "error_code": "DATABASE_ERROR",
  "message": "Database operation failed",
  "details": null,
  "request_id": "uuid-1234-5678",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 错误码说明

| 错误码 | HTTP状态码 | 说明 |
|--------|-----------|------|
| `DATABASE_ERROR` | 503 | 数据库操作失败 |
| `VALIDATION_ERROR` | 422 | 参数校验失败 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `EXTERNAL_API_ERROR` | 502 | 外部API调用失败 |
| `BUSINESS_ERROR` | 400 | 业务规则校验失败 |
| `BID_OUT_OF_RANGE` | 400 | 竞价超出允许范围 |

---

## 🧪 测试

### 运行测试

```bash
cd backend

# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 运行特定测试文件
pytest tests/test_metric_service.py
```

### 测试覆盖率目标

- 单元测试覆盖率: ≥80%
- API端点测试覆盖率: ≥80%
- 总体覆盖率: ≥80%

---

## 📁 项目结构

```
.
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API接口层
│   │   │   ├── metrics.py     # 指标查询API
│   │   │   ├── bidding.py     # 竞价策略API
│   │   │   └── keywords.py    # 关键词管理API
│   │   │
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # 应用配置
│   │   │   ├── database.py    # 数据库连接
│   │   │   ├── cache.py       # Redis缓存服务
│   │   │   ├── logger.py      # 日志系统
│   │   │   ├── exceptions.py  # 异常定义
│   │   │   └── context.py     # 请求上下文
│   │   │
│   │   ├── middleware/        # 中间件
│   │   │   ├── request_logger.py    # 请求日志
│   │   │   ├── performance.py       # 性能监控
│   │   │   └── error_handler.py     # 异常处理
│   │   │
│   │   ├── models/            # 数据模型
│   │   │   ├── models.py      # SQLAlchemy模型
│   │   │   └── schemas.py     # Pydantic模型
│   │   │
│   │   ├── services/          # 业务服务层
│   │   │   ├── metric_service.py      # 指标计算
│   │   │   └── bidding_service.py     # 竞价引擎
│   │   │
│   │   ├── agents/            # 智能体
│   │   │   └── base_agent.py
│   │   │
│   │   ├── jobs/              # 定时任务
│   │   │   ├── celery_app.py
│   │   │   └── tasks.py
│   │   │
│   │   └── main.py            # 应用入口
│   │
│   ├── tests/                 # 测试文件
│   ├── requirements.txt       # Python依赖
│   ├── pytest.ini             # 测试配置
│   └── .env.example           # 环境变量示例
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/       # UI组件
│   │   ├── pages/            # 页面
│   │   ├── services/         # API服务
│   │   ├── hooks/            # React Hooks
│   │   └── store/            # 状态管理
│   └── package.json
│
├── infrastructure/            # 基础设施配置
│   ├── docker/               # Docker配置
│   ├── k8s/                  # Kubernetes配置
│   └── terraform/            # Terraform配置
│
├── doc/                       # 文档
│   └── summary260508.md      # 代码完善总结
│
├── docker-compose.yml         # Docker Compose配置
└── README.md                  # 项目说明
```

---

## 🔧 开发指南

### 添加新的API端点

1. 在 `backend/app/api/` 创建新的路由文件
2. 定义Pydantic模型在 `backend/app/models/schemas.py`
3. 实现业务逻辑在 `backend/app/services/`
4. 在 `backend/app/main.py` 注册路由

### 代码规范

- 使用 `black` 格式化代码
- 使用 `flake8` 检查代码风格
- 使用 `mypy` 进行类型检查
- 所有函数添加类型注解
- 所有API端点添加文档字符串

### 提交代码

```bash
# 格式化代码
black app/
isort app/

# 检查代码风格
flake8 app/

# 类型检查
mypy app/

# 运行测试
pytest
```

---

## 📊 性能优化

### 已实现的优化

1. **数据库连接池**
   - 连接池大小: 50
   - 最大溢出连接: 100
   - 连接健康检查: 启用

2. **Redis缓存**
   - 默认TTL: 300秒
   - TTL随机化: 防止缓存雪崩
   - 缓存键模式管理

3. **查询优化**
   - 使用索引
   - 避免N+1查询
   - 限制返回字段

4. **性能监控**
   - 请求耗时追踪
   - 慢请求告警（>1秒）
   - 缓存命中率统计

---

## 🔐 安全特性

- **敏感信息外部化** - 所有密码、密钥从环境变量读取
- **JWT认证** - 基于JWT的用户认证
- **错误信息脱敏** - 不暴露内部实现细节
- **SQL注入防护** - 使用ORM和参数化查询
- **请求追踪** - 每个请求唯一ID，便于审计

---

## 📖 文档

### 规格文档

详细文档位于 `.codeartsdoer/specs/amazon_ads/`:

- `spec.md` - 需求规格说明
- `design.md` - 技术设计文档
- `tasks.md` - 任务清单
- `workflows.md` - 工作流设计
- `agents.md` - 智能体设计

### 代码完善文档

- `doc/summary260508.md` - 2026-05-08代码完善总结

---

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📝 License

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📞 支持

如有问题或建议，请：

- 提交 Issue
- 发送邮件至: support@example.com
- 查看文档: http://localhost:8000/docs

---

<div align="center">

**Built with ❤️ by Amazon Ads Platform Team**

**Powered by 华为云 CodeArts**

</div>
