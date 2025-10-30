#!/bin/bash

echo "🚀 啟動社群平台前端控制介面"
echo "================================"

# 檢查 Node.js 是否安裝
if ! command -v node &> /dev/null; then
    echo "❌ 錯誤: 未找到 Node.js，請先安裝 Node.js 16+"
    exit 1
fi

# 檢查 npm 是否安裝
if ! command -v npm &> /dev/null; then
    echo "❌ 錯誤: 未找到 npm，請先安裝 npm"
    exit 1
fi

# 檢查是否已安裝依賴
if [ ! -d "node_modules" ]; then
    echo "📦 安裝依賴..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 依賴安裝失敗"
        exit 1
    fi
fi

# 檢查後端服務是否運行
echo "🔍 檢查後端服務..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 後端服務正在運行"
else
    echo "⚠️  警告: 後端服務未運行，請先啟動後端服務"
    echo "   在 backend 目錄執行: python run.py"
    echo ""
    read -p "是否繼續啟動前端？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🎉 啟動前端開發服務器..."
echo "   前端地址: http://localhost:3000"
echo "   後端地址: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服務"
echo "================================"

# 啟動開發服務器
npm run dev
