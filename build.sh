#!/bin/bash
# build.sh - 用於Render部署的構建腳本

# 安裝依賴項
echo "安裝依賴項..."
pip install -r requirements.txt

# 確保目錄結構正確
echo "檢查目錄結構..."
mkdir -p static/docs
mkdir -p data
mkdir -p models
mkdir -p templates

# 確保日誌目錄存在
mkdir -p logs

# 確保文件有執行權限
chmod +x build.sh

# 顯示完成信息
echo "構建完成！"
