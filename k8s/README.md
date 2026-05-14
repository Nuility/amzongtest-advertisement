# Kubernetes配置说明

## 目录结构

```
k8s/
├── namespace.yaml              # 命名空间配置
├── configmap.yaml              # 应用配置
├── secret.yaml.template        # 密钥模板
├── backend-deployment.yaml     # Backend部署配置
├── celery-worker-deployment.yaml  # Celery Worker配置
├── celery-beat-deployment.yaml    # Celery Beat配置
├── frontend-deployment.yaml    # Frontend部署配置
├── ingress.yaml                # Ingress路由配置
└── network-policy.yaml         # 网络策略配置
```

## 配置文件说明

### 1. namespace.yaml
定义Kubernetes命名空间，隔离不同环境。

### 2. configmap.yaml
应用非敏感配置，包括:
- 数据库连接信息
- Redis配置
- Celery配置
- API地址
- 日志配置

### 3. secret.yaml.template
敏感信息模板，需要填入实际值:
- 数据库密码
- Redis密码
- JWT密钥
- AWS凭证

### 4. backend-deployment.yaml
Backend服务部署配置:
- 副本数: 2
- 资源: 1核1GB
- 健康检查: /health
- 自动扩缩容支持

### 5. celery-worker-deployment.yaml
Celery Worker配置:
- 副本数: 2
- 并发数: 4
- 队列: default, ads_sync, bidding

### 6. celery-beat-deployment.yaml
Celery Beat定时任务调度器:
- 副本数: 1 (单实例)
- 资源: 0.5核512MB

### 7. frontend-deployment.yaml
Frontend服务部署配置:
- 副本数: 2
- 资源: 0.2核256MB
- 静态资源服务

### 8. ingress.yaml
Ingress路由配置:
- 前端域名: yourdomain.com
- API域名: api.yourdomain.com
- HTTPS强制重定向
- Let's Encrypt自动证书

### 9. network-policy.yaml
网络策略配置:
- 限制服务间通信
- 允许必要访问
- 拒绝未授权连接

## 使用流程

1. 复制secret.yaml.template为secret.yaml并填入实际值
2. 修改ingress.yaml中的域名为实际域名
3. 修改configmap.yaml中的配置为实际配置
4. 执行部署脚本或手动apply配置文件
