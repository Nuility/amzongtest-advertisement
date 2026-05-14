#!/bin/bash

set -e

NAMESPACE="amazon-ads"
K8S_DIR="k8s"
REGISTRY="registry.cn-hangzhou.aliyuncs.com/amazon-ads"
VERSION="${1:-v1.0.0}"

echo "========================================"
echo "Amazon Ads Platform - 一键部署脚本"
echo "版本: $VERSION"
echo "========================================"

echo ""
echo "[Step 1/6] 检查kubectl连接..."
if ! kubectl cluster-info &> /dev/null; then
    echo "错误: 无法连接到Kubernetes集群"
    echo "请确保已配置正确的kubeconfig"
    exit 1
fi
echo "✓ Kubernetes集群连接正常"

echo ""
echo "[Step 2/6] 构建并推送Docker镜像..."
echo "构建Backend镜像..."
docker build -t $REGISTRY/backend:$VERSION ./backend
docker push $REGISTRY/backend:$VERSION
echo "✓ Backend镜像推送完成: $REGISTRY/backend:$VERSION"

echo "构建Frontend镜像..."
docker build -t $REGISTRY/frontend:$VERSION ./frontend
docker push $REGISTRY/frontend:$VERSION
echo "✓ Frontend镜像推送完成: $REGISTRY/frontend:$VERSION"

echo ""
echo "[Step 3/6] 创建命名空间..."
kubectl apply -f $K8S_DIR/namespace.yaml
echo "✓ 命名空间创建完成"

echo ""
echo "[Step 4/6] 应用配置..."
kubectl apply -f $K8S_DIR/configmap.yaml -n $NAMESPACE

if [ ! -f "$K8S_DIR/secret.yaml" ]; then
    echo "警告: secret.yaml不存在，请先创建secrets"
    echo "参考: k8s/secret.yaml.template"
    exit 1
fi
kubectl apply -f $K8S_DIR/secret.yaml -n $NAMESPACE
echo "✓ 配置应用完成"

echo ""
echo "[Step 5/6] 部署服务..."
kubectl apply -f $K8S_DIR/backend-deployment.yaml -n $NAMESPACE
kubectl apply -f $K8S_DIR/celery-worker-deployment.yaml -n $NAMESPACE
kubectl apply -f $K8S_DIR/celery-beat-deployment.yaml -n $NAMESPACE
kubectl apply -f $K8S_DIR/frontend-deployment.yaml -n $NAMESPACE
kubectl apply -f $K8S_DIR/ingress.yaml -n $NAMESPACE
kubectl apply -f $K8S_DIR/network-policy.yaml -n $NAMESPACE
echo "✓ 服务部署完成"

echo ""
echo "[Step 6/6] 等待服务就绪..."
echo "等待Backend服务..."
kubectl rollout status deployment/backend -n $NAMESPACE --timeout=300s

echo "等待Frontend服务..."
kubectl rollout status deployment/frontend -n $NAMESPACE --timeout=180s

echo "等待Celery Worker服务..."
kubectl rollout status deployment/celery-worker -n $NAMESPACE --timeout=180s

echo ""
echo "========================================"
echo "✓ 部署完成!"
echo "========================================"
echo ""
echo "查看服务状态:"
echo "  kubectl get pods -n $NAMESPACE"
echo ""
echo "查看服务日志:"
echo "  kubectl logs -f deployment/backend -n $NAMESPACE"
echo ""
echo "访问应用:"
echo "  前端: https://yourdomain.com"
echo "  API:  https://api.yourdomain.com"
