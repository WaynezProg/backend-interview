#!/bin/bash

echo "🚀 啟動社群平台 (後端 + 前端整合版)"
echo "=================================="

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 未找到 Python3，請先安裝 Python 3.12+"
    exit 1
fi

# 檢查是否在正確的目錄
if [ ! -f "backend/main.py" ]; then
    echo "❌ 錯誤: 請在專案根目錄執行此腳本"
    exit 1
fi

# 進入後端目錄
cd backend

# 檢查依賴是否安裝
if [ ! -d "venv" ]; then
    echo "📦 創建虛擬環境..."
    python3 -m venv venv
fi

echo "🔧 激活虛擬環境..."
source venv/bin/activate

echo "📦 安裝依賴..."
pip install -r requirements.txt

# 檢查資料庫是否需要初始化
echo "🗄️  檢查資料庫..."
python init_db.py info

echo ""
echo "🎉 啟動社群平台服務..."
echo "   前端地址: http://localhost:8000"
echo "   API 文檔: http://localhost:8000/docs"
echo "   後端 API: http://localhost:8000/api"
echo ""
echo "按 Ctrl+C 停止服務"
echo "=================================="

# 啟動服務
python run.py
