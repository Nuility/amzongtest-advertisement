#!/bin/bash

NAMESPACE="amazon-ads"
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"

echo "========================================"
echo "Amazon Ads Platform - 数据备份"
echo "========================================"

mkdir -p $BACKUP_DIR

echo ""
echo "[1/3] 备份MySQL数据库..."
MYSQL_POD=$(kubectl get pods -n $NAMESPACE -l component=mysql -o jsonpath='{.items[0].metadata.name}')

if [ -z "$MYSQL_POD" ]; then
    echo "警告: 未找到MySQL Pod，跳过数据库备份"
else
    kubectl exec $MYSQL_POD -n $NAMESPACE -- mysqldump -u root -p"$DB_PASSWORD" amazon_ads > $BACKUP_DIR/database.sql
    echo "✓ 数据库备份完成: $BACKUP_DIR/database.sql"
fi

echo ""
echo "[2/3] 备份Redis数据..."
REDIS_POD=$(kubectl get pods -n $NAMESPACE -l component=redis -o jsonpath='{.items[0].metadata.name}')

if [ -z "$REDIS_POD" ]; then
    echo "警告: 未找到Redis Pod，跳过Redis备份"
else
    kubectl exec $REDIS_POD -n $NAMESPACE -- redis-cli --rdb /tmp/dump.rdb
    kubectl cp $NAMESPACE/$REDIS_POD:/tmp/dump.rdb $BACKUP_DIR/redis.rdb
    echo "✓ Redis备份完成: $BACKUP_DIR/redis.rdb"
fi

echo ""
echo "[3/3] 备份Kubernetes配置..."
kubectl get configmap -n $NAMESPACE -o yaml > $BACKUP_DIR/configmap.yaml
kubectl get secret -n $NAMESPACE -o yaml > $BACKUP_DIR/secret.yaml
kubectl get ingress -n $NAMESPACE -o yaml > $BACKUP_DIR/ingress.yaml
echo "✓ K8s配置备份完成"

echo ""
echo "========================================"
echo "✓ 备份完成"
echo "备份位置: $BACKUP_DIR"
echo "========================================"
