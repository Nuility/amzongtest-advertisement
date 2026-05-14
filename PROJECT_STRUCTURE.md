# 项目结构说明

本文档详细说明项目中每个文件和目录的作用。

---

## 📂 根目录文件

| 文件 | 类型 | 说明 |
|-----|------|------|
| `README.md` | 文档 | 项目主文档，包含简介、快速开始、API说明等 |
| `UPGRADE.md` | 文档 | v1.0.2升级计划，列出未完成和需改进的功能 |
| `CHANGELOG.md` | 文档 | 版本更新日志，记录所有重要变更 |
| `CONTRIBUTING.md` | 文档 | 贡献指南，说明如何参与项目开发 |
| `CODE_OF_CONDUCT.md` | 文档 | 行为准则，社区行为规范 |
| `LICENSE` | 许可证 | MIT开源许可证 |
| `.gitignore` | 配置 | Git忽略文件配置 |
| `docker-compose.yml` | 配置 | Docker Compose编排配置，定义所有服务 |
| `BUGFIX_REPORT.md` | 报告 | Bug修复详细报告 |
| `ERROR_FIX_REPORT.md` | 报告 | 错误修复详细报告 |
| `RECOVERY_REPORT.md` | 报告 | 项目恢复报告 |

---

## 📂 backend/ - 后端服务

### 核心文件

| 文件 | 说明 |
|-----|------|
| `requirements.txt` | Python依赖包列表（59个包） |
| `pytest.ini` | pytest测试配置 |
| `pyproject.toml` | Python项目配置 |
| `.env` | 环境变量配置（生产） |
| `.env.example` | 环境变量配置模板 |
| `Dockerfile` | 后端Docker镜像构建文件 |
| `run.py` | 应用启动入口 |

### backend/app/ - 应用主目录

#### backend/app/api/ - API接口层

| 文件 | API端点 | 说明 |
|-----|---------|------|
| `metrics.py` | `/metrics/*` | 指标查询API<br>- 活动指标查询<br>- 关键词指标查询<br>- Dashboard概览数据 |
| `bidding.py` | `/bidding/*` | 竞价策略API<br>- 执行竞价策略<br>- 查询竞价历史<br>- 获取策略列表 |
| `keywords.py` | `/keywords/*` | 关键词管理API<br>- 关键词推荐<br>- 否定词管理 |
| `auth.py` | `/auth/*` | 认证授权API<br>- 用户登录<br>- Token验证 |

#### backend/app/core/ - 核心配置

| 文件 | 说明 |
|-----|------|
| `config.py` | 应用配置管理<br>- 环境变量加载<br>- 配置验证<br>- 安全检查 |
| `database.py` | 数据库连接管理<br>- 连接池配置<br>- 会话管理<br>- 事务处理 |
| `cache.py` | Redis缓存服务<br>- 缓存读写<br>- TTL管理<br>- 键模式管理 |
| `logger.py` | 日志系统<br>- 结构化日志<br>- JSON格式输出<br>- 请求追踪 |
| `exceptions.py` | 自定义异常<br>- 业务异常<br>- API异常<br>- 错误码定义 |
| `context.py` | 请求上下文<br>- 请求ID生成<br>- 上下文传递 |

#### backend/app/middleware/ - 中间件

| 文件 | 说明 |
|-----|------|
| `request_logger.py` | 请求日志中间件<br>- 请求开始/结束记录<br>- 响应时间统计 |
| `performance.py` | 性能监控中间件<br>- 慢请求检测<br>- 性能指标收集 |
| `error_handler.py` | 错误处理中间件<br>- 异常捕获<br>- 错误响应格式化 |

#### backend/app/models/ - 数据模型

| 文件 | 说明 |
|-----|------|
| `models.py` | SQLAlchemy数据库模型<br>- Account: 广告账户<br>- Campaign: 广告活动<br>- Keyword: 关键词<br>- BiddingLog: 竞价日志<br>- Team: 团队<br>- User: 用户 |
| `schemas.py` | Pydantic数据模型<br>- 请求验证模型<br>- 响应序列化模型<br>- 数据传输对象 |

#### backend/app/services/ - 业务服务层

| 文件 | 说明 |
|-----|------|
| `metric_service.py` | 指标计算服务<br>- MetricCalculator类<br>- ACoS/ROAS/CVR计算<br>- 指标聚合 |
| `bidding_service.py` | 竞价引擎服务<br>- ACoS目标策略<br>- CVR优化策略<br>- 风险控制 |
| `auth_service.py` | 认证服务<br>- JWT生成/验证<br>- 密码加密<br>- 权限检查 |

#### backend/app/agents/ - 智能体

| 文件 | 说明 |
|-----|------|
| `base_agent.py` | 智能体基类<br>- 通用Agent接口<br>- 决策引擎基础 |

#### backend/app/jobs/ - 定时任务

| 文件 | 说明 |
|-----|------|
| `celery_app.py` | Celery应用配置<br>- 任务队列配置<br>- Worker配置 |
| `tasks.py` | 定时任务定义<br>- sync_ad_data: 同步广告数据<br>- execute_bidding_strategy: 执行竞价<br>- mine_keywords: 挖掘关键词<br>- calculate_performance: 计算性能指标 |

#### backend/app/main.py

FastAPI应用入口：
- 应用创建
- 路由注册
- 中间件挂载
- 生命周期管理

### backend/tests/ - 测试套件

| 文件 | 说明 |
|-----|------|
| `conftest.py` | pytest配置<br>- 测试夹具<br>- 测试客户端<br>- 数据库会话 |
| `test_bidding_service.py` | 竞价服务测试<br>- ACoS策略测试<br>- CVR策略测试<br>- 风险控制测试 |
| `test_metric_service.py` | 指标服务测试<br>- ACoS计算测试<br>- ROAS计算测试<br>- CVR计算测试 |
| `unit/` | 单元测试目录<br>- 各模块单元测试 |

---

## 📂 frontend/ - 前端应用

### 核心文件

| 文件 | 说明 |
|-----|------|
| `package.json` | NPM依赖配置 |
| `tsconfig.json` | TypeScript编译配置 |
| `vite.config.ts` | Vite构建配置 |
| `index.html` | HTML入口模板 |
| `nginx.conf` | Nginx配置（生产） |
| `Dockerfile` | 前端Docker镜像构建文件 |

### frontend/src/ - 源代码

#### frontend/src/components/ - UI组件

| 目录/文件 | 说明 |
|----------|------|
| `Layout/` | 布局组件<br>- Header: 页头<br>- Sidebar: 侧边栏<br>- Footer: 页脚 |
| `Metrics/` | 指标展示组件<br>- MetricCard: 指标卡片<br>- MetricTable: 指标表格 |
| `Bidding/` | 竞价组件<br>- BiddingForm: 竞价表单<br>- BiddingHistory: 竞价历史 |
| `Keywords/` | 关键词组件<br>- KeywordList: 关键词列表<br>- NegativeKeywords: 否定词管理 |

#### frontend/src/pages/ - 页面

| 文件 | 路由 | 说明 |
|-----|------|------|
| `Dashboard.tsx` | `/` | 仪表盘页面<br>- 数据概览<br>- 图表展示 |
| `Campaigns.tsx` | `/campaigns` | 广告活动页面<br>- 活动列表<br>- 活动详情 |
| `Keywords.tsx` | `/keywords` | 关键词管理页面<br>- 关键词列表<br>- 推荐/否定词 |
| `Bidding.tsx` | `/bidding` | 竞价管理页面<br>- 策略配置<br>- 执行竞价 |
| `Settings.tsx` | `/settings` | 设置页面<br>- 账户配置<br>- 系统设置 |

#### frontend/src/services/ - API服务

| 文件 | 说明 |
|-----|------|
| `api.ts` | API客户端<br>- Axios实例配置<br>- 请求/响应拦截器<br>- 错误处理 |
| `metricsAPI.ts` | 指标API封装<br>- getCampaignMetrics<br>- getKeywordMetrics<br>- getDashboardOverview |
| `biddingAPI.ts` | 竞价API封装<br>- executeBidding<br>- getBiddingLogs<br>- getStrategies |
| `keywordsAPI.ts` | 关键词API封装<br>- getRecommendations<br>- manageNegativeKeywords |

#### frontend/src/hooks/ - React Hooks

| 文件 | 说明 |
|-----|------|
| `useMetrics.ts` | 指标数据Hook<br>- 活动指标获取<br>- 关键词指标获取<br>- 数据缓存 |
| `useBidding.ts` | 竞价Hook<br>- 策略执行<br>- 历史查询<br>- 状态管理 |
| `useKeywords.ts` | 关键词Hook<br>- 推荐获取<br>- 否定词管理 |

#### frontend/src/store/ - 状态管理

| 文件 | 说明 |
|-----|------|
| `useAppStore.ts` | 全局状态Store<br>- 用户信息<br>- 侧边栏状态<br>- 通知消息 |
| `useMetricStore.ts` | 指标状态Store<br>- 指标数据<br>- 筛选条件<br>- 时间范围 |

#### frontend/src/utils/ - 工具函数

| 文件 | 说明 |
|-----|------|
| `format.ts` | 格式化工具<br>- 数字格式化<br>- 日期格式化<br>- 百分比格式化 |
| `validators.ts` | 验证工具<br>- 表单验证<br>- 数据验证 |

#### frontend/src/App.tsx

应用主组件：
- 路由配置
- 全局Provider
- 布局结构

#### frontend/src/main.tsx

React应用入口：
- 渲染根组件
- 挂载到DOM

---

## 📂 k8s/ - Kubernetes配置

| 文件 | 说明 |
|-----|------|
| `namespace.yaml` | 命名空间定义 |
| `configmap.yaml` | 配置映射 |
| `secret.yaml` | 密钥配置 |
| `backend-deployment.yaml` | 后端部署配置 |
| `backend-service.yaml` | 后端服务配置 |
| `frontend-deployment.yaml` | 前端部署配置 |
| `frontend-service.yaml` | 前端服务配置 |
| `celery-worker-deployment.yaml` | Celery Worker部署 |
| `celery-beat-deployment.yaml` | Celery Beat部署 |
| `ingress.yaml` | Ingress路由配置 |
| `network-policy.yaml` | 网络策略 |
| `hpa.yaml` | 水平Pod自动扩缩 |

---

## 📂 scripts/ - 部署脚本

| 文件 | 说明 |
|-----|------|
| `deploy.sh` | 部署脚本<br>- 构建镜像<br>- 推送镜像<br>- 更新部署 |
| `health_check.sh` | 健康检查<br>- 服务状态检查<br>- 依赖服务检查 |
| `restart.sh` | 重启服务<br>- 优雅重启<br>- 滚动更新 |
| `backup.sh` | 备份脚本<br>- 数据库备份<br>- 文件备份 |
| `create_secrets.sh` | 密钥创建<br>- 生成JWT密钥<br>- 创建K8s密钥 |

---

## 📂 docs/ - 文档目录

| 文件 | 说明 |
|-----|------|
| `USER_MANUAL.md` | 用户使用手册<br>- 安装部署<br>- 配置说明<br>- 使用方法<br>- 故障排查 |
| `deployment_guide.md` | 部署指南<br>- Docker部署<br>- K8s部署<br>- 生产环境配置 |
| `USER_MANUAL_aliyun.md` | 阿里云部署手册 |
| `deployment_guide_aliyun.md` | 阿里云部署指南 |

---

## 📂 doc/ - 开发文档

| 文件 | 说明 |
|-----|------|
| `summary260507.md` | 2026-05-07开发总结 |
| `summary260508.md` | 2026-05-08代码完善总结 |
| `summary260512.md` | 2026-05-12项目检查总结 |
| `operation-readiness.md` | 运营就绪检查文档 |

---

## 📂 infrastructure/ - 基础设施

| 目录 | 说明 |
|-----|------|
| `docker/` | Docker配置文件 |
| `k8s/` | Kubernetes高级配置 |
| `terraform/` | Terraform基础设施即代码 |

---

## 📂 .codeartsdoer/ - CodeArts配置

项目规格和任务管理文档，包含：
- `specs/amazon_ads/` - 项目规格说明
- `specs/code_quality_improvement/` - 代码质量改进
- `specs/iteration_upgrade/` - 迭代升级计划
- `specs/deployment_solution/` - 部署方案
- `specs/user_agent/` - 用户代理设计

---

## 🔗 数据流向

```
用户请求
   ↓
Frontend (React)
   ↓
API Service (Axios)
   ↓
Backend API (FastAPI)
   ↓
Middleware
   ├→ Request Logger
   ├→ Auth Check
   └→ Performance Monitor
   ↓
Service Layer
   ↓
┌──────┬──────┬──────┐
│ MySQL│ Redis│Cache │
└──────┴──────┴──────┘
   ↓
Response
   ↓
Frontend Render
```

---

## 🔗 部署架构

```
┌─────────────────────────────────────┐
│          Load Balancer              │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│         Ingress (K8s)                │
└──────┬───────────────────┬──────────┘
       │                   │
┌──────┴──────┐      ┌─────┴───────┐
│  Frontend   │      │   Backend   │
│  (Nginx)    │      │  (FastAPI)  │
│  (Pod x2)   │      │  (Pod x3)   │
└─────────────┘      └──────┬──────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────┴────┐       ┌─────┴─────┐      ┌────┴────┐
    │  MySQL  │       │   Redis   │      │ Celery  │
    │(Primary)│       │  (Cache)  │      │ Worker  │
    └─────────┘       └───────────┘      └─────────┘
```

---

## 📊 技术栈总结

### 后端技术栈
- **框架**: FastAPI 0.136+
- **ORM**: SQLAlchemy 2.0+
- **验证**: Pydantic 2.5+
- **异步**: Celery 5.3+
- **缓存**: Redis 5.0+
- **数据库**: MySQL 8.0
- **认证**: JWT (PyJWT 2.8+)

### 前端技术栈
- **框架**: React 18+
- **语言**: TypeScript 5.3+
- **UI库**: Ant Design 5.13+
- **图表**: ECharts 5.4+
- **状态**: Zustand 4.5+
- **请求**: TanStack Query 5.17+
- **构建**: Vite 5.0+

### 基础设施
- **容器**: Docker
- **编排**: Kubernetes
- **云平台**: 华为云 CCE

---

**Amazon Ads Platform Team**  
**Powered by 华为云 CodeArts**
