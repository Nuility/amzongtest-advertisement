# 更新日志

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### 计划中

- 竞价API真实数据获取
- SQL注入防护增强
- JWT密钥验证加强
- Dashboard图表实现
- API类型定义完善

详见 [UPGRADE.md](UPGRADE.md)

---

## [1.0.1] - 2026-05-12

### 新增

- 完整的用户使用手册 [docs/USER_MANUAL.md](docs/USER_MANUAL.md)
- 部署指南文档 [docs/deployment_guide.md](docs/deployment_guide.md)
- 阿里云部署文档
- 数据库迁移配置

### 修复

#### 严重问题 (8个)
- ✅ Campaign模型补充性能指标字段 (impressions, clicks, spend, orders, sales)
- ✅ Keyword模型添加 is_negative 字段
- ✅ Keyword模型补充性能指标字段
- ✅ 竞价历史记录 old_bid 逻辑错误修复
- ✅ 补充缺失依赖包 (PyJWT, passlib, python-jose, bcrypt, python-json-logger)
- ✅ 前端API调用方法修正 (useBidding, useMetrics)
- ✅ 前端API参数类型匹配修正
- ✅ 数据库事务异常处理添加

#### 导入错误 (4个)
- ✅ backend/app/core/__init__.py 导入路径修正
- ✅ backend/app/models/__init__.py Schema类导入修正
- ✅ backend/app/services/__init__.py 服务类导入修正
- ✅ backend/app/jobs/__init__.py Celery任务导入修正

#### TypeScript错误 (7处)
- ✅ frontend/src/services/api.ts 参数类型定义
- ✅ 添加 CampaignMetricsParams 接口
- ✅ 添加 KeywordMetricsParams 接口
- ✅ 添加 DashboardParams 接口
- ✅ 添加 BiddingData 接口
- ✅ 添加 BiddingLogsParams 接口
- ✅ 添加 RecommendationsParams 接口

#### 类型不匹配 (2个)
- ✅ Decimal类型正确使用
- ✅ 添加 Decimal 导入

### 变更

- Pydantic v2 配置语法适配
- pytest 配置优化
- Docker环境变量配置优化

### 文档

- 更新 README.md 完整项目说明
- 添加 Bug修复报告 [BUGFIX_REPORT.md](BUGFIX_REPORT.md)
- 添加 错误修复报告 [ERROR_FIX_REPORT.md](ERROR_FIX_REPORT.md)
- 添加 恢复报告 [RECOVERY_REPORT.md](RECOVERY_REPORT.md)

### 测试

- ✅ 37个单元测试全部通过 (100%)
- ✅ 指标计算服务测试 (9个)
- ✅ 竞价策略测试 (18个)
- ✅ 业务逻辑测试 (10个)

---

## [1.0.0] - 2026-05-08

### 新增

#### 核心功能
- 指标计算与分析模块
  - 流量指标计算 (Impressions, Clicks, CTR)
  - 成本指标计算 (CPC, Spend)
  - 转化指标计算 (Orders, CVR)
  - KPI指标计算 (ACoS, ROAS, TACoS)
  
- 智能竞价引擎
  - ACoS目标策略
  - CVR优化策略
  - 风险控制机制
  - 竞价历史记录
  
- 关键词智能管理
  - 关键词推荐功能
  - 否定词管理
  - 推荐得分计算
  
- 数据可视化
  - Dashboard概览
  - 趋势分析框架
  - SKU分析框架

#### 技术架构
- FastAPI后端框架
- React 18 + TypeScript前端
- SQLAlchemy ORM
- Celery异步任务
- Redis缓存
- MySQL数据库
- Docker容器化
- Kubernetes部署配置

#### API端点
- GET /metrics/campaigns - 查询广告活动指标
- GET /metrics/keywords - 查询关键词指标
- GET /metrics/dashboard/overview - 获取看板概览
- POST /bidding/execute - 执行竞价策略
- GET /bidding/logs - 查询竞价历史
- GET /bidding/strategies - 获取策略列表
- GET /keywords/recommend - 获取关键词推荐
- POST /keywords/negative - 添加否定关键词
- GET /keywords/negative - 查询否定关键词
- DELETE /keywords/negative - 移除否定关键词

#### 基础设施
- Docker Compose配置
- Kubernetes部署配置 (12个YAML文件)
- 健康检查脚本
- 部署脚本
- 备份脚本

#### 文档
- README.md 项目说明
- MIT许可证
- .gitignore配置
- .env.example环境变量模板

### 项目结构

```
├── backend/           # 后端服务
│   ├── app/
│   │   ├── api/       # API接口
│   │   ├── core/      # 核心配置
│   │   ├── middleware/# 中间件
│   │   ├── models/    # 数据模型
│   │   ├── services/  # 业务服务
│   │   ├── agents/    # 智能体
│   │   └── jobs/      # 定时任务
│   └── tests/         # 测试套件
├── frontend/          # 前端应用
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── hooks/
│       └── store/
├── k8s/              # Kubernetes配置
├── scripts/          # 部署脚本
└── docs/             # 文档
```

---

## 版本说明

### 版本号规则

- **主版本号**: 不兼容的API变更
- **次版本号**: 向后兼容的功能新增
- **修订号**: 向后兼容的问题修复

### 变更类型

- `新增`: 新功能
- `变更`: 现有功能的变更
- `弃用`: 即将移除的功能
- `移除`: 已移除的功能
- `修复`: Bug修复
- `安全`: 安全相关修复

---

## 贡献

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 许可证

[MIT License](LICENSE)

---

**Amazon Ads Platform Team**  
**Powered by 华为云 CodeArts**
