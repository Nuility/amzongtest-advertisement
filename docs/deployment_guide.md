# 部署操作手册

## 文档信息
- 版本: v1.0
- 更新日期: 2026-05-11
- 适用环境: 华为云CCE (Cloud Container Engine)

---

## 一、部署前准备

### 1.1 云资源准备

#### 步骤1：创建华为云CCE Kubernetes集群

**控制台操作步骤**：
1. 登录华为云控制台：https://console.huaweicloud.com
2. 进入"云容器引擎 CCE"服务
3. 点击"创建集群"按钮
4. 填写集群配置：
   - **集群名称**：amazon-ads-prod
   - **集群版本**：v1.28（推荐最新稳定版）
   - **集群规模**：50节点
   - **地域**：cn-north-4（华北-北京四）或其他
   - **可用区**：选择多可用区（提高可用性）
   - **集群类型**：CCE Turbo（高性能）或标准集群
   - **网络模式**：容器隧道网络
5. 点击"下一步：创建节点"

**节点配置**：
- **节点规格**：c6.xlarge.2（4vCPU 8GB）
- **节点数量**：3个（生产环境建议3个以上）
- **操作系统**：EulerOS 2.9
- **系统盘**：高IO，40GB
- **数据盘**：高IO，100GB（容器运行时）
- **弹性伸缩**：开启，最小3节点，最大10节点

**网络配置**：
- **VPC**：自动创建或选择已有VPC
- **子网**：自动创建或选择已有子网
- **容器网段**：自动分配（172.16.0.0/16）
- **服务网段**：自动分配（10.247.0.0/16）

**高级配置**：
- **认证方式**：IAM认证
- **日志采集**：开启LTS日志
- **监控**：开启云监控

6. 点击"立即创建"，等待集群创建完成（约10-15分钟）
7. 创建完成后，点击"集群"->"概览"，确认集群状态为"可用"

#### 步骤2：创建RDS MySQL实例

**控制台操作步骤**：
1. 进入"云数据库 RDS"服务
2. 点击"购买数据库实例"
3. 填写配置：
   - **地域**：与CCE集群相同（cn-north-4）
   - **实例类型**：主备（高可用）
   - **数据库引擎**：MySQL
   - **版本**：8.0
   - **实例规格**：rds.mysql.c6.large.2.ha（2核4GB）
   - **存储类型**：高IO
   - **存储空间**：50GB
   - **VPC**：选择与CCE集群相同的VPC
   - **安全组**：创建或选择安全组，开放3306端口
4. 设置管理员账户：
   - **用户名**：root
   - **密码**：设置强密码（记录备用）
5. 点击"立即购买"，等待实例创建完成（约5-10分钟）

**参数配置**：
```bash
# 在实例创建完成后，进入"参数修改"页面
# 修改以下参数：
max_connections = 500
innodb_buffer_pool_size = 2G
wait_timeout = 28800
interactive_timeout = 28800
character_set_server = utf8mb4
collation_server = utf8mb4_general_ci
```

#### 步骤3：创建Redis实例

**控制台操作步骤**：
1. 进入"分布式缓存服务 DCS"服务
2. 点击"购买缓存实例"
3. 填写配置：
   - **地域**：与CCE集群相同
   - **缓存类型**：Redis
   - **版本**：Redis 7.0
   - **实例类型**：主备
   - **实例规格**：redis.ha.xu1.large.2（1GB）
   - **副本数**：2（主备）
   - **VPC**：选择与CCE集群相同的VPC
   - **安全组**：开放6379端口
4. 设置密码：设置强密码（记录备用）
5. 点击"立即购买"，等待实例创建完成（约3-5分钟）

**Redis参数配置**：
```bash
# 在实例详情页面，进入"参数设置"
# 修改以下参数：
maxclients = 10000
timeout = 300
tcp-keepalive = 300
```

#### 步骤4：配置网络和安全组

**安全组配置**：
```bash
# 进入VPC控制台 -> 安全组

# CCE节点安全组（自动创建，确认以下规则）：
# 入方向规则：
# - 端口 22: 允许SSH访问（生产环境建议限制IP）
# - 端口 80/443: 允许HTTP/HTTPS访问
# - 端口 30000-32767: Kubernetes NodePort范围
# 出方向规则：
# - 全部允许

# MySQL安全组：
# 入方向规则：
# - 端口 3306: 源地址选择CCE节点安全组或VPC网段
# 出方向规则：
# - 全部允许

# Redis安全组：
# 入方向规则：
# - 端口 6379: 源地址选择CCE节点安全组或VPC网段
# 出方向规则：
# - 全部允许
```

#### 步骤5：获取kubeconfig配置

```bash
# 方法1：通过控制台下载
# 1. 进入CCE集群详情页
# 2. 点击"集群" -> "概览" -> "连接信息"
# 3. 点击"kubectl"页签
# 4. 选择"内网访问"或"公网访问"
# 5. 点击"下载kubeconfig"，保存为 ~/.kube/config-huawei

# 方法2：通过命令行配置
# 安装华为云CLI工具
pip install esdk-obs-python

# 或使用kubectl直接连接
export KUBECONFIG=~/.kube/config-huawei
kubectl cluster-info  # 验证连接
kubectl get nodes     # 查看节点列表
```

### 1.2 域名与SSL准备

#### 步骤1：购买域名

**华为云域名购买**：
```bash
# 1. 进入"域名注册服务"控制台
# 2. 搜索并购买域名（如 yourdomain.com）
# 3. 完成实名认证（个人或企业）
# 4. 域名购买成功后，进入"域名控制台"
```

#### 步骤2：ICP备案（国内业务必须）

```bash
# 1. 进入"ICP备案"控制台
# 2. 点击"开始备案"
# 3. 填写备案信息：
#    - 主体信息（企业或个人）
#    - 网站信息（域名、用途等）
#    - 上传证件材料
# 4. 提交审核，等待管局审核（5-20个工作日）
# 5. 备案成功后，获得备案号

# 注意：备案期间可先使用IP访问进行测试
```

#### 步骤3：配置DNS解析

```bash
# 1. 获取Ingress负载均衡IP
#    进入CCE集群 -> 服务路由 -> 路由设置 -> 查看Nginx Ingress服务的外部IP

# 2. 进入"公网域名解析"控制台
# 3. 点击域名进入解析设置页面
# 4. 添加解析记录：

# 前端域名记录：
# - 记录类型：A
# - 主机记录：@
# - 记录值：负载均衡IP
# - TTL：600秒

# API域名记录：
# - 记录类型：A
# - 主机记录：api
# - 记录值：负载均衡IP
# - TTL：600秒

# 5. 等待解析生效（10-30分钟）
# 6. 验证解析：
ping yourdomain.com
ping api.yourdomain.com
```

### 1.3 安装必要组件

#### 步骤1：安装Nginx Ingress Controller

```bash
# 华为云CCE默认已安装Nginx Ingress，检查是否已安装
kubectl get svc -n kube-system | grep nginx-ingress

# 如未安装，手动安装：
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# 等待安装完成
kubectl get pods -n ingress-nginx -w

# 验证Ingress Controller运行正常
kubectl get svc -n ingress-nginx
# 应看到类型为LoadBalancer的服务及其外部IP
```

#### 步骤2：安装cert-manager

```bash
# 安装cert-manager（用于自动签发SSL证书）
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml

# 等待cert-manager组件就绪
kubectl get pods -n cert-manager -w

# 验证安装成功
kubectl get deployment cert-manager -n cert-manager
kubectl get deployment cert-manager-webhook -n cert-manager

# 创建Let's Encrypt签发机构
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com  # 修改为你的邮箱
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# 验证签发机构创建成功
kubectl get clusterissuer letsencrypt-prod
```

#### 步骤3：配置容器镜像仓库

```bash
# 使用华为云SWR（容器镜像服务）
# 1. 进入"容器镜像服务 SWR"控制台
# 2. 创建组织（命名空间）
#    - 组织名称：amazon-ads
#    - 地域：与CCE集群相同

# 3. 配置镜像仓库地址
export REGISTRY="swr.cn-north-4.myhuaweicloud.com/amazon-ads"

# 4. 登录镜像仓库
docker login -u cn-north-4@{AK} -p {SK} swr.cn-north-4.myhuaweicloud.com
# 其中AK为华为云Access Key ID，SK为Secret Access Key

# 5. 修改k8s配置文件中的镜像地址
# 将 registry.cn-hangzhou.aliyuncs.com/amazon-ads 替换为
# swr.cn-north-4.myhuaweicloud.com/amazon-ads
```

---

## 二、执行部署

### 2.1 配置密钥

```bash
# 运行密钥创建脚本
./scripts/create_secrets.sh

# 或手动创建
kubectl create secret generic app-secrets \
  --namespace=amazon-ads \
  --from-literal=DATABASE_USER=root \
  --from-literal=DATABASE_PASSWORD=your_password \
  --from-literal=REDIS_PASSWORD=your_redis_password \
  --from-literal=JWT_SECRET_KEY=$(openssl rand -hex 32) \
  --from-literal=AWS_ACCESS_KEY_ID=your_key \
  --from-literal=AWS_SECRET_ACCESS_KEY=your_secret
```

### 2.2 一键部署

```bash
# 执行完整部署流程
./scripts/deploy.sh v1.0.0
```

### 2.3 手动部署步骤

如需手动部署，按以下步骤执行:

```bash
# 步骤1: 创建命名空间
kubectl apply -f k8s/namespace.yaml

# 步骤2: 应用配置
kubectl apply -f k8s/configmap.yaml -n amazon-ads
kubectl apply -f k8s/secret.yaml -n amazon-ads

# 步骤3: 部署服务
kubectl apply -f k8s/backend-deployment.yaml -n amazon-ads
kubectl apply -f k8s/celery-worker-deployment.yaml -n amazon-ads
kubectl apply -f k8s/celery-beat-deployment.yaml -n amazon-ads
kubectl apply -f k8s/frontend-deployment.yaml -n amazon-ads

# 步骤4: 配置网络
kubectl apply -f k8s/ingress.yaml -n amazon-ads
kubectl apply -f k8s/network-policy.yaml -n amazon-ads

# 步骤5: 等待就绪
kubectl rollout status deployment/backend -n amazon-ads --timeout=300s
kubectl rollout status deployment/frontend -n amazon-ads --timeout=180s
```

---

## 三、验证部署

### 3.1 健康检查

```bash
# 运行健康检查脚本
./scripts/health_check.sh

# 或手动检查
kubectl get pods -n amazon-ads
kubectl get services -n amazon-ads
kubectl get ingress -n amazon-ads
```

### 3.2 功能验证

```bash
# 验证前端访问
curl -I https://yourdomain.com

# 验证API访问
curl -I https://api.yourdomain.com/health

# 验证HTTPS证书
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### 3.3 日志查看

```bash
# 查看Backend日志
kubectl logs -f deployment/backend -n amazon-ads

# 查看Frontend日志
kubectl logs -f deployment/frontend -n amazon-ads

# 查看Celery Worker日志
kubectl logs -f deployment/celery-worker -n amazon-ads
```

---

## 四、日常运维

### 4.1 服务管理

```bash
# 重启服务
./scripts/restart.sh backend
./scripts/restart.sh all

# 扩缩容
kubectl scale deployment backend --replicas=3 -n amazon-ads

# 滚动更新
kubectl set image deployment/backend backend=registry.cn-hangzhou.aliyuncs.com/amazon-ads/backend:v1.0.1 -n amazon-ads
```

### 4.2 数据备份

```bash
# 执行备份
./scripts/backup.sh

# 备份文件位置
ls -la backups/
```

### 4.3 监控查看

```bash
# 查看资源使用
kubectl top pods -n amazon-ads
kubectl top nodes

# 查看事件
kubectl get events -n amazon-ads --sort-by='.lastTimestamp'
```

---

## 五、故障排查

### 5.1 Pod无法启动

```bash
# 查看Pod详情
kubectl describe pod <pod-name> -n amazon-ads

# 查看Pod事件
kubectl get events -n amazon-ads --field-selector involvedObject.name=<pod-name>

# 查看容器日志
kubectl logs <pod-name> -n amazon-ads --previous
```

### 5.2 服务无法访问

```bash
# 检查Service端点
kubectl get endpoints -n amazon-ads

# 检查Ingress状态
kubectl describe ingress amazon-ads-ingress -n amazon-ads

# 检查网络策略
kubectl get networkpolicy -n amazon-ads
```

### 5.3 数据库连接失败

```bash
# 进入Pod测试连接
kubectl exec -it deployment/backend -n amazon-ads -- /bin/bash
# 在容器内执行
python -c "from app.core.database import engine; engine.connect()"
```

---

## 六、配置参考

### 6.1 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| APP_NAME | 应用名称 | amazon-ads |
| APP_ENV | 运行环境 | production |
| DATABASE_HOST | 数据库地址 | mysql-service |
| DATABASE_PORT | 数据库端口 | 3306 |
| REDIS_HOST | Redis地址 | redis-service |
| LOG_LEVEL | 日志级别 | INFO |

### 6.2 资源配置

| 服务 | CPU请求 | 内存请求 | CPU限制 | 内存限制 |
|------|---------|----------|---------|----------|
| Backend | 500m | 512Mi | 1000m | 1Gi |
| Frontend | 100m | 128Mi | 200m | 256Mi |
| Celery Worker | 500m | 512Mi | 1000m | 1Gi |
| Celery Beat | 100m | 256Mi | 500m | 512Mi |

---

## 七、常见问题

### Q1: 域名无法访问?
A: 检查DNS解析是否正确，SSL证书是否签发成功

### Q2: Pod一直Pending?
A: 检查节点资源是否充足， PVC是否绑定成功

### Q3: 数据库连接超时?
A: 检查数据库服务是否正常，安全组规则是否开放

---

## 九、P2阶段详细操作说明

### 9.1 部署脚本作用说明

#### scripts/create_secrets.sh - 密钥创建脚本

**作用**：交互式创建Kubernetes Secrets，存储敏感信息

**执行步骤**：
```bash
# 1. 进入项目根目录
cd /path/to/project

# 2. 运行密钥创建脚本
./scripts/create_secrets.sh

# 3. 按提示输入以下信息：
#    - 数据库用户名（默认root）
#    - 数据库密码（在华为云RDS创建时设置的密码）
#    - Redis密码（在华为云DCS创建时设置的密码）
#    - JWT密钥（可自动生成）
#    - AWS Access Key ID
#    - AWS Secret Access Key
#    - AWS区域（默认us-east-1）
#    - Sentry DSN（可选，用于错误监控）

# 4. 脚本自动生成 k8s/secret.yaml 文件

# 5. 验证创建成功
kubectl get secret app-secrets -n amazon-ads -o yaml
```

**注意事项**：
- 密码输入时不会显示在屏幕上
- k8s/secret.yaml文件不应提交到版本控制
- 建议使用华为云DEW（数据加密服务）管理密钥

#### scripts/deploy.sh - 一键部署脚本

**作用**：自动化完成Docker镜像构建、推送和Kubernetes部署

**执行步骤**：
```bash
# 1. 确保已登录华为云SWR镜像仓库
docker login -u cn-north-4@{AK} -p {SK} swr.cn-north-4.myhuaweicloud.com

# 2. 执行部署（指定版本号）
./scripts/deploy.sh v1.0.0

# 脚本执行流程：
# Step 1/6: 检查kubectl连接
# Step 2/6: 构建并推送Docker镜像
#   - 构建Backend镜像：docker build -t swr.../backend:v1.0.0 ./backend
#   - 推送Backend镜像：docker push swr.../backend:v1.0.0
#   - 构建Frontend镜像：docker build -t swr.../frontend:v1.0.0 ./frontend
#   - 推送Frontend镜像：docker push swr.../frontend:v1.0.0
# Step 3/6: 创建命名空间
# Step 4/6: 应用ConfigMap和Secret
# Step 5/6: 部署所有服务（Backend、Frontend、Celery）
# Step 6/6: 等待服务就绪

# 3. 查看部署进度
kubectl get pods -n amazon-ads -w
```

**输出结果**：
```
========================================
✓ 部署完成!
========================================

查看服务状态:
  kubectl get pods -n amazon-ads

访问应用:
  前端: https://yourdomain.com
  API:  https://api.yourdomain.com
```

#### scripts/health_check.sh - 健康检查脚本

**作用**：检查所有服务的运行状态和健康状况

**执行步骤**：
```bash
# 执行健康检查
./scripts/health_check.sh

# 输出示例：
========================================
Amazon Ads Platform - 健康检查
========================================

[Pods状态]
NAME                        READY   STATUS    RESTARTS   AGE
backend-xxx                 1/1     Running   0          5m
frontend-xxx                1/1     Running   0          5m
celery-worker-xxx           1/1     Running   0          5m
celery-beat-xxx             1/1     Running   0          5m

[服务状态]
NAME              TYPE        CLUSTER-IP      PORT(S)
backend-service   ClusterIP   10.247.x.x      8000/TCP
frontend-service  ClusterIP   10.247.x.x      80/TCP

[检查Pod健康]
✓ backend-xxx - 健康
✓ frontend-xxx - 健康
✓ celery-worker-xxx - 健康
✓ celery-beat-xxx - 健康

✓ 所有服务运行正常
```

**异常处理**：
```bash
# 如果检查失败，查看异常Pod日志
kubectl logs <pod-name> -n amazon-ads

# 查看Pod事件
kubectl describe pod <pod-name> -n amazon-ads
```

#### scripts/restart.sh - 服务重启脚本

**作用**：滚动重启指定服务或所有服务

**执行步骤**：
```bash
# 重启单个服务
./scripts/restart.sh backend
./scripts/restart.sh frontend
./scripts/restart.sh celery-worker

# 重启所有服务
./scripts/restart.sh all

# 输出示例：
========================================
Amazon Ads Platform - 服务重启
========================================

重启 backend...
deployment.apps/backend restarted
Waiting for deployment "backend" rollout to finish: 1 of 2 updated replicas are available...
deployment "backend" successfully rolled out
✓ backend 重启完成
```

**使用场景**：
- 配置更新后需要重启服务
- 服务异常需要重启恢复
- 定期维护重启

#### scripts/backup.sh - 数据备份脚本

**作用**：备份MySQL数据库、Redis数据和Kubernetes配置

**执行步骤**：
```bash
# 执行备份
./scripts/backup.sh

# 输出示例：
========================================
Amazon Ads Platform - 数据备份
========================================

[1/3] 备份MySQL数据库...
✓ 数据库备份完成: backups/20260511_213000/database.sql

[2/3] 备份Redis数据...
✓ Redis备份完成: backups/20260511_213000/redis.rdb

[3/3] 备份Kubernetes配置...
✓ K8s配置备份完成

========================================
✓ 备份完成
备份位置: backups/20260511_213000
========================================

# 查看备份文件
ls -la backups/20260511_213000/
# database.sql  redis.rdb  configmap.yaml  secret.yaml  ingress.yaml
```

**恢复操作**：
```bash
# 恢复MySQL数据库
kubectl exec -it mysql-pod -n amazon-ads -- mysql -u root -p amazon_ads < backups/20260511_213000/database.sql

# 恢复Redis数据
kubectl cp backups/20260511_213000/redis.rdb amazon-ads/redis-pod:/tmp/dump.rdb
kubectl exec redis-pod -n amazon-ads -- redis-cli --rdb /tmp/dump.rdb
```

### 9.2 手动部署详细步骤

如需更精细控制，可按以下步骤手动部署：

#### 步骤1：构建Docker镜像

```bash
# 设置镜像仓库地址
export REGISTRY="swr.cn-north-4.myhuaweicloud.com/amazon-ads"
export VERSION="v1.0.0"

# 构建Backend镜像
cd backend
docker build -t $REGISTRY/backend:$VERSION .
docker push $REGISTRY/backend:$VERSION

# 构建Frontend镜像
cd ../frontend
docker build -t $REGISTRY/frontend:$VERSION .
docker push $REGISTRY/frontend:$VERSION

cd ..
```

#### 步骤2：创建命名空间和配置

```bash
# 创建命名空间
kubectl apply -f k8s/namespace.yaml

# 创建ConfigMap（修改configmap.yaml中的配置）
# 编辑 k8s/configmap.yaml，更新以下配置：
# - DATABASE_HOST: 华为云RDS内网地址
# - REDIS_HOST: 华为云DCS内网地址
# - API_BASE_URL: https://api.yourdomain.com
# - FRONTEND_URL: https://yourdomain.com

kubectl apply -f k8s/configmap.yaml -n amazon-ads

# 创建Secret
kubectl apply -f k8s/secret.yaml -n amazon-ads
```

#### 步骤3：部署应用服务

```bash
# 部署Backend（API服务）
kubectl apply -f k8s/backend-deployment.yaml -n amazon-ads
kubectl rollout status deployment/backend -n amazon-ads --timeout=300s

# 部署Celery Worker（异步任务处理）
kubectl apply -f k8s/celery-worker-deployment.yaml -n amazon-ads
kubectl rollout status deployment/celery-worker -n amazon-ads --timeout=180s

# 部署Celery Beat（定时任务调度）
kubectl apply -f k8s/celery-beat-deployment.yaml -n amazon-ads
kubectl rollout status deployment/celery-beat -n amazon-ads --timeout=60s

# 部署Frontend（前端应用）
kubectl apply -f k8s/frontend-deployment.yaml -n amazon-ads
kubectl rollout status deployment/frontend -n amazon-ads --timeout=180s
```

#### 步骤4：配置网络和SSL

```bash
# 修改 k8s/ingress.yaml，更新域名
# - yourdomain.com -> 实际域名
# - api.yourdomain.com -> API域名

# 应用Ingress配置
kubectl apply -f k8s/ingress.yaml -n amazon-ads

# 应用网络策略
kubectl apply -f k8s/network-policy.yaml -n amazon-ads

# 等待SSL证书自动签发（约5-10分钟）
kubectl get certificate -n amazon-ads -w

# 验证证书签发成功
kubectl describe certificate amazon-ads-tls -n amazon-ads
```

#### 步骤5：验证部署结果

```bash
# 检查所有Pod状态
kubectl get pods -n amazon-ads
# 期望输出：所有Pod状态为Running，READY为1/1

# 检查服务访问
kubectl get svc -n amazon-ads
kubectl get ingress -n amazon-ads

# 测试API健康检查
curl -k https://api.yourdomain.com/health

# 测试前端访问
curl -I https://yourdomain.com

# 查看服务日志
kubectl logs -f deployment/backend -n amazon-ads --tail=100
```

### 9.3 部署后配置检查清单

- [ ] 所有Pod状态为Running
- [ ] Backend健康检查返回200
- [ ] Frontend可正常访问
- [ ] SSL证书已签发（HTTPS绿锁）
- [ ] Celery Worker可接收任务
- [ ] Celery Beat定时任务运行
- [ ] 数据库连接正常
- [ ] Redis连接正常
- [ ] API接口响应正常
- [ ] 前端页面加载无错误

---

## 十、联系方式

- 技术支持: tech-support@example.com
- 运维团队: ops-team@example.com
