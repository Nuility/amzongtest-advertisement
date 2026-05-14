#!/bin/bash

NAMESPACE="amazon-ads"

echo "========================================"
echo "Amazon Ads Platform - 服务重启"
echo "========================================"
echo ""

if [ -z "$1" ]; then
    echo "用法: ./scripts/restart.sh <service-name>"
    echo ""
    echo "可用服务:"
    echo "  - backend"
    echo "  - frontend"
    echo "  - celery-worker"
    echo "  - celery-beat"
    echo "  - all (重启所有服务)"
    exit 1
fi

SERVICE=$1

restart_service() {
    local svc=$1
    echo "重启 $svc..."
    kubectl rollout restart deployment/$svc -n $NAMESPACE
    kubectl rollout status deployment/$svc -n $NAMESPACE --timeout=180s
    echo "✓ $svc 重启完成"
}

if [ "$SERVICE" = "all" ]; then
    echo "重启所有服务..."
    restart_service "backend"
    restart_service "frontend"
    restart_service "celery-worker"
    restart_service "celery-beat"
else
    restart_service "$SERVICE"
fi

echo ""
echo "✓ 重启完成"
