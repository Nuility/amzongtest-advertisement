#!/bin/bash

###############################################################################
# 亚马逊广告智能投放平台 - 自动部署脚本
# 适用于：Ubuntu 20.04/22.04 服务器
# 使用方法：bash deploy.sh
###############################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 欢迎信息
echo "============================================================================="
echo "       亚马逊广告智能投放平台 - 自动部署脚本"
echo "============================================================================="
echo ""

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    log_error "请使用root用户运行此脚本"
    exit 1
fi

# 步骤1：检查系统
log_step "步骤1/10: 检查系统环境"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    log_info "系统: $NAME $VERSION"
else
    log_warn "无法识别系统版本"
fi

# 步骤2：安装依赖
log_step "步骤2/10: 安装系统依赖"
apt update -qq
apt install -y -qq curl wget git > /dev/null
log_info "系统依赖安装完成"

# 步骤3：安装Docker
log_step "步骤3/10: 安装Docker"
if command -v docker &> /dev/null; then
    log_info "Docker已安装，跳过"
else
    log_info "正在安装Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh > /dev/null 2>&1
    rm get-docker.sh
    systemctl start docker
    systemctl enable docker > /dev/null
    log_info "Docker安装完成"
fi

# 步骤4：安装Docker Compose
log_step "步骤4/10: 安装Docker Compose"
if docker compose version &> /dev/null; then
    log_info "Docker Compose已安装，跳过"
else
    apt install -y -qq docker-compose-plugin > /dev/null
    log_info "Docker Compose安装完成"
fi

# 步骤5：创建项目目录
log_step "步骤5/10: 创建项目目录"
PROJECT_DIR="/opt/amazon-ads"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR
log_info "项目目录: $PROJECT_DIR"

# 步骤6：获取项目代码
log_step "步骤6/10: 获取项目代码"
if [ -d ".git" ]; then
    log_info "项目已存在，拉取最新代码..."
    git pull
else
    log_info "正在从GitHub克隆项目..."
    git clone https://github.com/Nuility/amzongtest-advertisement.git . > /dev/null
fi

# 步骤7：配置环境变量
log_step "步骤7/10: 配置环境变量"
cd backend
if [ ! -f ".env" ]; then
    log_info "创建环境变量配置..."
    cp .env.example .env
    
    # 生成安全的JWT密钥
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -hex 32)
    
    # 更新配置
    sed -i "s|DEBUG=True|DEBUG=False|g" .env
    sed -i "s|your-secret-key-change-in-production|$JWT_SECRET|g" .env
    
    log_info "环境变量配置完成"
    log_info "JWT密钥已自动生成"
else
    log_warn ".env文件已存在，跳过配置"
fi

# 步骤8：配置防火墙
log_step "步骤8/10: 配置防火墙"
if command -v ufw &> /dev/null; then
    log_info "配置UFW防火墙..."
    ufw --force enable > /dev/null
    ufw allow 22/tcp > /dev/null
    ufw allow 80/tcp > /dev/null
    ufw allow 443/tcp > /dev/null
    ufw allow 8000/tcp > /dev/null
    log_info "防火墙配置完成"
else
    log_warn "UFW未安装，跳过防火墙配置"
fi

# 步骤9：构建并启动服务
log_step "步骤9/10: 构建并启动服务"
cd $PROJECT_DIR

log_info "构建Docker镜像（可能需要几分钟）..."
docker compose build

log_info "启动服务..."
docker compose up -d

log_info "等待服务启动..."
sleep 10

# 步骤10：验证部署
log_step "步骤10/10: 验证部署"

# 检查容器状态
BACKEND_STATUS=$(docker compose ps backend 2>/dev/null | grep -c "Up" || echo 0)
FRONTEND_STATUS=$(docker compose ps frontend 2>/dev/null | grep -c "Up" || echo 0)
MYSQL_STATUS=$(docker compose ps mysql 2>/dev/null | grep -c "Up" || echo 0)
REDIS_STATUS=$(docker compose ps redis 2>/dev/null | grep -c "Up" || echo 0)

echo ""
echo "============================================================================="
echo "                         部署状态检查"
echo "============================================================================="

if [ "$BACKEND_STATUS" -eq 1 ]; then
    echo -e "后端服务:    ${GREEN}✓ 运行中${NC}"
else
    echo -e "后端服务:    ${RED}✗ 未运行${NC}"
fi

if [ "$FRONTEND_STATUS" -eq 1 ]; then
    echo -e "前端服务:    ${GREEN}✓ 运行中${NC}"
else
    echo -e "前端服务:    ${RED}✗ 未运行${NC}"
fi

if [ "$MYSQL_STATUS" -eq 1 ]; then
    echo -e "MySQL数据库: ${GREEN}✓ 运行中${NC}"
else
    echo -e "MySQL数据库: ${RED}✗ 未运行${NC}"
fi

if [ "$REDIS_STATUS" -eq 1 ]; then
    echo -e "Redis缓存:   ${GREEN}✓ 运行中${NC}"
else
    echo -e "Redis缓存:   ${RED}✗ 未运行${NC}"
fi

echo "============================================================================="

# 获取服务器IP
SERVER_IP=$(curl -s ifconfig.me || hostname -I | awk '{print $1}')

# 测试服务
echo ""
log_info "测试服务连接..."
HEALTH_CHECK=$(curl -s http://localhost:8000/health 2>/dev/null || echo "failed")

if [ "$HEALTH_CHECK" != "failed" ]; then
    echo -e "API健康检查: ${GREEN}✓ 通过${NC}"
else
    echo -e "API健康检查: ${YELLOW}⚠ 等待启动${NC}"
fi

# 部署成功信息
echo ""
echo "============================================================================="
echo "                         部署完成！"
echo "============================================================================="
echo ""
echo "访问地址:"
echo "  前端界面:  http://$SERVER_IP"
echo "  后端API:   http://$SERVER_IP:8000"
echo "  API文档:   http://$SERVER_IP:8000/docs"
echo ""
echo "管理命令:"
echo "  查看状态:  cd $PROJECT_DIR && docker compose ps"
echo "  查看日志:  cd $PROJECT_DIR && docker compose logs -f"
echo "  重启服务:  cd $PROJECT_DIR && docker compose restart"
echo "  停止服务:  cd $PROJECT_DIR && docker compose down"
echo ""
echo "配置文件: $PROJECT_DIR/backend/.env"
echo ""
echo "============================================================================="

# 询问是否配置域名
echo ""
read -p "是否配置域名和HTTPS? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "请输入您的域名 (例如: example.com): " DOMAIN
    
    if [ -n "$DOMAIN" ]; then
        log_info "配置域名和HTTPS..."
        
        # 安装Certbot
        apt install -y -qq certbot python3-certbot-nginx > /dev/null
        
        # 申请证书
        certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --register-unsafely-without-email || true
        
        log_info "域名配置完成!"
        echo ""
        echo "访问地址: https://$DOMAIN"
    fi
fi

log_info "部署脚本执行完毕！"
