#!/bin/bash

NAMESPACE="amazon-ads"

echo "========================================"
echo "Amazon Ads Platform - 健康检查"
echo "========================================"
echo ""

echo "[Pods状态]"
kubectl get pods -n $NAMESPACE -o wide
echo ""

echo "[服务状态]"
kubectl get services -n $NAMESPACE
echo ""

echo "[Deployment状态]"
kubectl get deployments -n $NAMESPACE
echo ""

echo "[Ingress状态]"
kubectl get ingress -n $NAMESPACE
echo ""

echo "[检查Pod健康]"
ALL_HEALTHY=true

for pod in $(kubectl get pods -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    READY=$(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
    if [ "$READY" != "True" ]; then
        echo "❌ $pod - 未就绪"
        ALL_HEALTHY=false
    else
        echo "✓ $pod - 健康"
    fi
done

echo ""

if [ "$ALL_HEALTHY" = true ]; then
    echo "✓ 所有服务运行正常"
    exit 0
else
    echo "❌ 存在异常服务，请检查日志"
    echo ""
    echo "查看异常Pod日志:"
    for pod in $(kubectl get pods -n $NAMESPACE --field-selector=status.phase!=Running -o jsonpath='{.items[*].metadata.name}'); do
        echo "  kubectl logs $pod -n $NAMESPACE"
    done
    exit 1
fi
