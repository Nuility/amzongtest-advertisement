# 快速部署指南

<div align="center">

**5分钟完成服务器部署**

</div>

---

## 🚀 极速部署（推荐）

### 前提条件
- 一台云服务器（阿里云/腾讯云/华为云等）
- Ubuntu 20.04 或 22.04 系统
- root权限

### 一键部署命令

```bash
# 连接服务器后，执行以下命令
wget https://raw.githubusercontent.com/Nuility/amzongtest-advertisement/main/scripts/deploy-server.sh
bash deploy-server.sh
```

**就这样！脚本会自动完成所有部署工作。**

---

## 📝 详细步骤

### 步骤1：购买服务器

推荐配置：
| 配置项 | 最低 | 推荐 |
|--------|------|------|
| CPU | 2核 | 4核 |
| 内存 | 4GB | 8GB |
| 硬盘 | 40GB | 100GB SSD |
| 带宽 | 3Mbps | 10Mbps |

**购买链接**：
- [阿里云ECS](https://www.aliyun.com/product/ecs)
- [腾讯云CVM](https://cloud.tencent.com/product/cvm)
- [华为云ECS](https://www.huaweicloud.com/product/ecs.html)

### 步骤2：连接服务器

**Windows用户**：
- 使用PowerShell或PuTTY
```powershell
ssh root@your_server_ip
```

**Mac/Linux用户**：
```bash
ssh root@your_server_ip
```

### 步骤3：执行部署脚本

```bash
# 下载脚本
wget https://raw.githubusercontent.com/Nuility/amzongtest-advertisement/main/scripts/deploy-server.sh

# 执行部署
bash deploy-server.sh
```

脚本会自动：
1. ✅ 安装Docker和Docker Compose
2. ✅ 克隆项目代码
3. ✅ 配置环境变量
4. ✅ 配置防火墙
5. ✅ 构建并启动所有服务
6. ✅ 验证部署

### 步骤4：访问应用

部署完成后，脚本会显示访问地址：

```
访问地址:
  前端界面:  http://123.45.67.89
  后端API:   http://123.45.67.89:8000
  API文档:   http://123.45.67.89:8000/docs
```

---

## 🌐 配置域名（可选）

### 1. 购买域名

推荐注册商：
- [阿里云万网](https://wanwang.aliyun.com/)
- [腾讯云DNSPod](https://dnspod.cloud.tencent.com/)
- [GoDaddy](https://www.godaddy.com/)

### 2. 域名解析

在域名管理控制台添加A记录：

| 记录类型 | 主机记录 | 记录值 |
|---------|---------|--------|
| A | @ | 服务器IP |
| CNAME | www | @ |

### 3. 配置HTTPS

部署脚本会询问是否配置域名和HTTPS，选择`y`并输入域名即可。

或手动执行：

```bash
# 安装Certbot
apt install -y certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## 📊 部署后管理

### 查看服务状态

```bash
cd /opt/amazon-ads
docker compose ps
```

### 查看日志

```bash
# 所有服务日志
docker compose logs -f

# 特定服务日志
docker compose logs -f backend
docker compose logs -f frontend
```

### 重启服务

```bash
docker compose restart
```

### 停止服务

```bash
docker compose down
```

### 更新代码

```bash
cd /opt/amazon-ads
git pull
docker compose build
docker compose up -d
```

---

## 🔧 常见问题

### Q1: 端口访问不了？

**检查防火墙**：

```bash
# 查看防火墙状态
ufw status

# 开放端口
ufw allow 80/tcp
ufw allow 8000/tcp
```

**检查云平台安全组**：

在云平台控制台 -> 安全组 -> 添加入站规则：
- 端口80（HTTP）
- 端口443（HTTPS）
- 端口8000（API，可选）

### Q2: 服务启动失败？

```bash
# 查看错误日志
docker compose logs

# 检查容器状态
docker compose ps

# 重新构建
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Q3: 忘记密码？

数据库默认密码在`docker-compose.yml`中：
```yaml
MYSQL_ROOT_PASSWORD: AmazonAds2024
```

修改后重启：
```bash
docker compose down
docker compose up -d
```

### Q4: 内存不足？

```bash
# 查看内存使用
free -h

# 查看Docker资源使用
docker stats

# 添加交换空间
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

---

## 📈 性能优化建议

### 生产环境配置

1. **修改数据库密码**
   ```bash
   nano /opt/amazon-ads/docker-compose.yml
   # 修改 MYSQL_ROOT_PASSWORD
   ```

2. **关闭DEBUG模式**
   ```bash
   nano /opt/amazon-ads/backend/.env
   # 设置 DEBUG=False
   ```

3. **增加Docker资源限制**
   ```yaml
   # 在docker-compose.yml中添加
   deploy:
     resources:
       limits:
         memory: 2G
   ```

4. **启用Nginx缓存和Gzip**
   已在默认配置中启用

---

## 🆘 获取帮助

- 📖 [详细部署文档](docs/SERVER_DEPLOYMENT.md)
- 📖 [用户手册](docs/USER_MANUAL.md)
- 🐛 [报告问题](https://github.com/Nuility/amzongtest-advertisement/issues)
- 💬 [讨论交流](https://github.com/Nuility/amzongtest-advertisement/discussions)

---

## ✅ 部署检查清单

部署前：
- [ ] 服务器配置满足最低要求
- [ ] 系统为Ubuntu 20.04/22.04
- [ ] 有root权限

部署后：
- [ ] 所有容器运行正常
- [ ] 前端页面可访问
- [ ] API接口可访问
- [ ] 数据库连接正常

生产环境：
- [ ] 已修改数据库密码
- [ ] DEBUG模式已关闭
- [ ] JWT密钥已更换
- [ ] 域名已配置（可选）
- [ ] HTTPS已启用（可选）

---

**祝您部署顺利！🎉**

**Amazon Ads Platform Team**  
**Powered by 华为云 CodeArts**
