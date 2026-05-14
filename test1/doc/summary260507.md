# 亚马逊广告智能投放平台项目总结

**生成日期**: 2027-05-07  
**项目名称**: 亚马逊广告智能投放与团队管理平台  
**技术平台**: 华为云 CodeArts

---

## 一、项目概述

基于亚马逊广告系统的竞价机制和转化优化原理，构建智能广告投放平台，实现：

- **提升广告 ROI** - 通过智能调价策略优化投入产出比
- **降低人工成本** - 自动化关键词挖掘、调价、否定词管理
- **实现运营标准化** - 策略模板化，经验可复制
- **支持规模化增长** - 多账号、多站点、多品牌管理

---

## 二、生成的规格文档

### 2.1 文档位置
`.codeartsdoer/specs/amazon_ads/`

### 2.2 文档清单

| 文件 | 说明 | 内容 |
|------|------|------|
| `spec.md` | 需求规格说明 | 20+ 功能需求、非功能需求、验收标准 |
| `design.md` | 技术设计文档 | 微服务架构、数据库设计、API 接口、核心模块设计 |
| `tasks.md` | 任务清单 | 13 个阶段、100+ 具体任务 |
| `workflows.md` | 工作流设计 | CI/CD 工作流、数据处理工作流、CodeArts Pipeline 配置 |
| `agents.md` | 智能体设计 | 7 个核心智能体设计、编排机制、部署配置 |

---

## 三、生成的项目代码

### 3.1 后端服务（Backend - Python + FastAPI）

#### 核心目录结构
```
backend/
├── app/
│   ├── api/                  # API 接口层
│   │   ├── metrics.py        # 指标查询 API
│   │   ├── bidding.py        # 调价执行 API
│   │   └── keywords.py       # 关键词管理 API
│   │
│   ├── core/                 # 核心配置
│   │   ├── config.py         # 应用配置（数据库、Redis、API等）
│   │   └── database.py       # SQLAlchemy 数据库连接
│   │
│   ├── models/               # 数据模型层
│   │   ├── models.py         # SQLAlchemy ORM 模型
│   │   │                     # - Campaign（广告活动）
│   │   │                     # - AdGroup（广告组）
│   │   │                     # - Keyword（关键词）
│   │   │                     # - Account（账号）
│   │   │                     # - BiddingLog（调价日志）
│   │   │                     # - TeamMember（团队成员）
│   │   │                     # - KPIConfig（KPI 配置）
│   │   └── schemas.py        # Pydantic 数据验证模型
│   │
│   ├── services/             # 业务服务层
│   │   ├── metric_service.py         # 指标计算服务
│   │   │                             # - CTR 计算
│   │   │                             # - CVR 计算
│   │   │                             # - ACoS 计算
│   │   │                             # - ROAS 计算
│   │   └── bidding_service.py        # 调价引擎
│   │                                 # - ACoS 目标策略
│   │                                 # - CVR 优化策略
│   │                                 # - 风险控制
│   │                                 # - 边界检查
│   │
│   ├── agents/               # 智能体
│   │   └── base_agent.py     # 智能体基类和实现
│   │                         # - DataCollectionAgent
│   │                         # - BiddingStrategyAgent
│   │                         # - KeywordMiningAgent
│   │                         # - AnomalyDetectionAgent
│   │
│   ├── jobs/                 # 定时任务
│   │   ├── celery_app.py     # Celery 配置
│   │   └── tasks.py          # 异步任务定义
│   │                         # - sync_ad_data（数据同步）
│   │                         # - execute_bidding_strategy（调价）
│   │                         # - mine_keywords（关键词挖掘）
│   │                         # - calculate_performance（绩效计算）
│   │
│   └── main.py               # FastAPI 应用入口
│
├── tests/                    # 测试文件
│   ├── test_metric_service.py    # 指标计算测试
│   └── test_bidding_service.py   # 调价引擎测试
│
├── requirements.txt          # Python 依赖清单
├── pytest.ini                # 测试配置
├── .flake8                   # 代码质量配置
├── Dockerfile                # Docker 镜像构建
└── run.py                    # 启动脚本
```

#### 关键代码实现

**1. 指标计算服务** (`metric_service.py`)
```python
class MetricCalculator:
    - calculate_ctr()     # 点击率
    - calculate_cvr()     # 转化率
    - calculate_acos()    # 广告成本销售比
    - calculate_roas()    # 投资回报率
    - calculate_all_metrics()  # 综合计算
```

**2. 调价引擎** (`bidding_service.py`)
```python
class BiddingEngine:
    - ACoSTargetStrategy  # 基于 ACoS 目标的策略
    - CVRBasedStrategy    # 基于 CVR 优化的策略
    - execute_bidding()   # 执行调价（含风险控制）
```

**3. Celery 定时任务** (`tasks.py`)
- 每小时：数据同步
- 每 4 小时：调价策略执行
- 每天：关键词挖掘、绩效计算

### 3.2 前端应用（Frontend - React + TypeScript）

#### 核心目录结构
```
frontend/
├── src/
│   ├── pages/
│   │   └── Dashboard.tsx         # 仪表盘页面
│   │                             # - 数据概览卡片
│   │                             # - ACoS/ROAS 趋势图
│   │                             # - 花费分布图
│   │
│   ├── services/
│   │   └── api.ts                # API 客户端
│   │                             # - metricsAPI（指标查询）
│   │                             # - biddingAPI（调价执行）
│   │                             # - keywordsAPI（关键词管理）
│   │
│   ├── components/               # UI 组件
│   ├── hooks/                    # React Hooks
│   ├── store/                    # 状态管理（Zustand）
│   └── utils/                    # 工具函数
│
├── package.json          # Node.js 依赖清单
└── Dockerfile            # Docker 镜像构建
```

#### 技术栈
- **框架**: React 18 + TypeScript
- **UI 库**: Ant Design 5
- **图表**: ECharts
- **状态管理**: Zustand
- **数据请求**: TanStack Query (React Query)
- **HTTP 客户端**: Axios

### 3.3 基础设施配置

#### Docker Compose (`docker-compose.yml`)
```yaml
services:
  - backend          # FastAPI 应用
  - frontend         # React 应用
  - mysql            # MySQL 8.0
  - redis            # Redis 7
  - celery-worker    # Celery 工作进程
  - celery-beat      # Celery 调度器
```

#### Kubernetes 部署 (`infrastructure/k8s/`)
- `backend-deployment.yaml` - 后端服务部署（2 副本、健康检查、资源限制）
- `frontend-deployment.yaml` - 前端服务部署（LoadBalancer 服务类型）

---

## 四、核心功能模块

### 4.1 数据采集模块
- Amazon Ads API 集成（OAuth 2.0 认证）
- Campaign、AdGroup、Keyword 数据同步
- 性能指标数据采集
- 支持多账号、多站点

### 4.2 指标计算模块
- **流量指标**: Impressions、Clicks、CTR
- **成本指标**: CPC、Spend
- **转化指标**: Orders、CVR
- **KPI 指标**: ACoS、ROAS、TACoS
- 多维度聚合（Campaign、Keyword、SKU）

### 4.3 自动调价引擎
- **ACoS 目标策略**: 根据实际 ACoS 与目标的偏差自动调整出价
- **CVR 优化策略**: 高 CVR 提价，低 CVR 降价
- **风险控制**: 最大调整幅度 30%、冷却期 24 小时
- **批量执行**: 支持批量关键词调价
- **审计日志**: 所有调价操作可追溯

### 4.4 关键词管理模块
- **关键词挖掘**: 基于搜索词报告和 ML 模型推荐高潜力关键词
- **否定词识别**: 自动识别高点击无转化的关键词
- **相关性过滤**: 基于产品 Listing 计算相关性得分

### 4.5 BI 可视化系统
- **实时仪表盘**: 总花费、销售额、ACoS、ROAS 概览
- **趋势分析**: ACoS、ROAS 时间序列图
- **SKU 分析**: 单品盈利能力分析
- **对比分析**: 环比、同比数据对比

### 4.6 团队管理系统
- **KPI 配置**: 多维度目标设定（ACoS、ROAS、花费效率）
- **绩效计算**: 自动计算达成率和绩效分数
- **人效分析**: 运营人员工作量统计

### 4.7 智能体系统
- **DataCollectionAgent**: 数据采集智能体
- **BiddingStrategyAgent**: 调价策略智能体
- **KeywordMiningAgent**: 关键词挖掘智能体
- **AnomalyDetectionAgent**: 异常检测智能体
- **PerformanceEvaluationAgent**: 绩效计算智能体
- **BudgetOptimizationAgent**: 预算优化智能体
- **NegativeKeywordAgent**: 否定词智能体

---

## 五、技术架构

### 5.1 整体架构
```
┌─────────────────────────────────────┐
│     Frontend (React + TypeScript)    │
│         Ant Design + ECharts         │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│        API Gateway (华为云 APIG)      │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│     Backend (FastAPI + Python)       │
├──────────────────────────────────────┤
│  API Layer                           │
│  ├── metrics.py (指标查询)           │
│  ├── bidding.py (调价执行)           │
│  └── keywords.py (关键词管理)        │
│                                      │
│  Service Layer                       │
│  ├── MetricCalculator                │
│  └── BiddingEngine                   │
│                                      │
│  Agent Layer                         │
│  ├── DataCollectionAgent             │
│  ├── BiddingStrategyAgent            │
│  └── KeywordMiningAgent              │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│          Data Layer                  │
├──────────────────────────────────────┤
│  MySQL (业务数据)                    │
│  ClickHouse (分析数据)               │
│  Redis (缓存 + 任务队列)             │
└──────────────────────────────────────┘
               │
┌──────────────┴──────────────────────┐
│       External APIs                  │
├──────────────────────────────────────┤
│  Amazon Ads API                      │
│  Amazon SP-API                       │
└──────────────────────────────────────┘
```

### 5.2 数据库设计

**MySQL 表**:
- `campaigns` - 广告活动
- `ad_groups` - 广告组
- `keywords` - 关键词
- `accounts` - 账号
- `bidding_logs` - 调价日志
- `team_members` - 团队成员
- `kpi_configs` - KPI 配置

**ClickHouse 表**:
- `performance_metrics` - 性能指标（按日期分区）

### 5.3 华为云服务集成
- **CCE (Cloud Container Engine)** - Kubernetes 容器编排
- **RDS** - MySQL 托管
- **DWS (Data Warehouse Service)** - ClickHouse 数据仓库
- **DCS (Distributed Cache Service)** - Redis 缓存
- **OBS (Object Storage Service)** - 对象存储
- **APIG (API Gateway)** - API 网关
- **CTS (Cloud Trace Service)** - 审计追踪

---

## 六、DevOps 与工作流

### 6.1 CI/CD 工作流
```
代码提交 → 代码检查 → 单元测试 → 构建 → 部署
   ↓          ↓          ↓        ↓       ↓
  Git      Flake8    pytest    Docker   Kubernetes
           Black     (80%覆盖率)
```

### 6.2 数据处理工作流
```
每小时: 数据同步 → 指标计算 → 缓存更新
每 4 小时: 调价策略执行 → 效果追踪
每天: 关键词挖掘 → 否定词识别 → 绩效计算
```

### 6.3 监控告警
- **系统监控**: CPU、内存、API 响应时间、错误率
- **业务监控**: 数据同步延迟、调价成功率、ACoS 异常波动
- **告警分级**: P0（电话+短信）、P1（短信）、P2（钉钉）、P3（邮件）

---

## 七、测试覆盖

### 7.1 单元测试
- `test_metric_service.py` - 指标计算逻辑测试（CTR、CVR、ACoS、ROAS）
- `test_bidding_service.py` - 调价策略测试（ACoS 策略、CVR 策略、边界检查）

### 7.2 测试配置
```ini
[pytest]
asyncio_mode = auto
addopts = 
    --cov=app
    --cov-report=html
    --cov-fail-under=80
```

---

## 八、快速启动指南

### 8.1 使用 Docker Compose（推荐）

```bash
# 1. 启动所有服务
docker-compose up -d

# 2. 查看服务状态
docker-compose ps

# 3. 查看日志
docker-compose logs -f backend

# 4. 停止服务
docker-compose down
```

**访问地址**:
- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs
- API 文档（ReDoc）: http://localhost:8000/redoc

### 8.2 本地开发模式

**后端**:
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py

# 运行测试
pytest

# 代码格式化
black app/
isort app/
```

**前端**:
```bash
cd frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 运行测试
npm test
```

### 8.3 Kubernetes 部署

```bash
# 1. 配置 kubeconfig
kubectl config use-context your-cluster

# 2. 创建命名空间
kubectl create namespace amazon-ads

# 3. 创建密钥
kubectl create secret generic db-credentials \
  --from-literal=url='mysql+pymysql://user:pass@host:3306/db' \
  -n amazon-ads

# 4. 部署应用
kubectl apply -f infrastructure/k8s/

# 5. 查看部署状态
kubectl get pods -n amazon-ads
kubectl get services -n amazon-ads
```

---

## 九、项目文件统计

### 9.1 文件数量
- **规格文档**: 5 个（spec.md、design.md、tasks.md、workflows.md、agents.md）
- **后端代码**: 15+ 个 Python 文件
- **前端代码**: 5+ 个 TypeScript 文件
- **配置文件**: 10+ 个（Docker、K8s、pytest 等）
- **总计**: 35+ 个文件

### 9.2 代码行数（估算）
- **后端**: ~2000 行 Python
- **前端**: ~500 行 TypeScript
- **配置**: ~500 行 YAML/JSON
- **文档**: ~3000 行 Markdown

---

## 十、后续开发建议

### 10.1 短期任务（1-2 周）
1. ✅ 完善 Amazon Ads API 集成（实际调用）
2. ✅ 实现数据采集服务（完整流程）
3. ✅ 完善前端仪表盘（添加图表）
4. ✅ 编写更多单元测试和集成测试

### 10.2 中期任务（1-2 月）
1. 实现 ML 关键词评分模型训练
2. 开发异常检测算法
3. 完善团队管理和权限系统
4. 性能优化（数据库查询、缓存策略）

### 10.3 长期任务（3-6 月）
1. 多平台扩展（TikTok、Shopify）
2. 预算优化算法
3. 预测模型（销量预测、花费预测）
4. 高级可视化（自定义报表、实时大屏）

---

## 十一、关键配置说明

### 11.1 环境变量（后端）
```bash
# 数据库
DATABASE_URL=mysql+pymysql://user:pass@host:3306/amazon_ads
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Amazon API
AMAZON_ADS_API_BASE=https://advertising-api.amazon.com
AMAZON_SP_API_BASE=https://sellingpartnerapi-na.amazon.com

# 安全
JWT_SECRET_KEY=your-secret-key
```

### 11.2 Celery 定时任务配置
```python
beat_schedule = {
    "data-sync-hourly": {
        "task": "app.jobs.tasks.sync_ad_data",
        "schedule": 3600.0,  # 每小时
    },
    "bidding-strategy": {
        "task": "app.jobs.tasks.execute_bidding_strategy",
        "schedule": 14400.0,  # 每 4 小时
    },
    "keyword-mining": {
        "task": "app.jobs.tasks.mine_keywords",
        "schedule": 86400.0,  # 每天
    },
}
```

---

## 十二、技术债务与优化点

### 12.1 当前限制
- ⚠️ Amazon API 实际调用未实现（需要申请开发者权限）
- ⚠️ ML 模型仅定义接口，未实际训练
- ⚠️ 前端图表组件待完善
- ⚠️ 缺少端到端测试

### 12.2 优化建议
- 💡 使用连接池优化数据库性能
- 💡 实现批量数据写入（减少数据库压力）
- 💡 添加请求缓存（减少 API 调用）
- 💡 实现 API 限流和熔断机制
- 💡 完善日志和追踪系统

---

## 十三、文档索引

### 13.1 项目文档
- **README.md** - 项目快速入门
- **KNOWLEDGE_BASE.md** - 项目知识库（待填充）
- **doc/summary260507.md** - 本总结文档

### 13.2 规格文档
- `.codeartsdoer/specs/amazon_ads/spec.md` - 需求规格
- `.codeartsdoer/specs/amazon_ads/design.md` - 技术设计
- `.codeartsdoer/specs/amazon_ads/tasks.md` - 任务清单
- `.codeartsdoer/specs/amazon_ads/workflows.md` - 工作流设计
- `.codeartsdoer/specs/amazon_ads/agents.md` - 智能体设计

### 13.3 API 文档
- 启动后端后访问: http://localhost:8000/docs
- ReDoc 格式: http://localhost:8000/redoc

---

## 十四、联系方式与支持

**项目维护者**: Amazon Ads Platform Team  
**技术栈**: Python 3.10+ | Node.js 18+ | MySQL 8.0 | Redis 7 | Kubernetes  
**云平台**: 华为云 CodeArts  

**问题反馈**: 请在项目仓库创建 Issue  
**贡献代码**: 欢迎 Pull Request

---

**文档版本**: v1.0  
**最后更新**: 2027-05-07
