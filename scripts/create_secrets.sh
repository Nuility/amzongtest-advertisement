#!/bin/bash

set -e

NAMESPACE="amazon-ads"

echo "========================================"
echo "创建Kubernetes Secrets"
echo "========================================"

echo ""
echo "请输入以下配置信息:"
echo ""

read -p "数据库用户名 [root]: " DB_USER
DB_USER=${DB_USER:-root}

read -sp "数据库密码: " DB_PASSWORD
echo ""

read -sp "Redis密码: " REDIS_PASSWORD
echo ""

read -sp "JWT密钥 (按Enter自动生成): " JWT_SECRET
echo ""
if [ -z "$JWT_SECRET" ]; then
    JWT_SECRET=$(openssl rand -hex 32)
    echo "已自动生成JWT密钥"
fi

read -p "AWS Access Key ID: " AWS_ACCESS_KEY
read -sp "AWS Secret Access Key: " AWS_SECRET_KEY
echo ""
read -p "AWS区域 [us-east-1]: " AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}

read -p "Sentry DSN (可选，按Enter跳过): " SENTRY_DSN

cat > k8s/secret.yaml <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: $NAMESPACE
  labels:
    app: amazon-ads
type: Opaque
stringData:
  DATABASE_USER: "$DB_USER"
  DATABASE_PASSWORD: "$DB_PASSWORD"
  REDIS_PASSWORD: "$REDIS_PASSWORD"
  JWT_SECRET_KEY: "$JWT_SECRET"
  JWT_ALGORITHM: "HS256"
  JWT_EXPIRATION_HOURS: "24"
  AWS_ACCESS_KEY_ID: "$AWS_ACCESS_KEY"
  AWS_SECRET_ACCESS_KEY: "$AWS_SECRET_KEY"
  AWS_REGION: "$AWS_REGION"
  SENTRY_DSN: "$SENTRY_DSN"
EOF

echo ""
echo "✓ Secrets创建完成: k8s/secret.yaml"
echo ""
echo "警告: 请勿将k8s/secret.yaml提交到版本控制系统!"
