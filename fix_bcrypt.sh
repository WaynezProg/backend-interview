#!/bin/bash

echo "🔧 修復 bcrypt 密碼加密問題"
echo "================================"

cd backend

# 激活虛擬環境
if [ -d "venv" ]; then
    echo "🔧 激活虛擬環境..."
    source venv/bin/activate
else
    echo "📦 創建虛擬環境..."
    python3 -m venv venv
    source venv/bin/activate
fi

# 升級 pip
echo "📦 升級 pip..."
pip install --upgrade pip

# 卸載有問題的 bcrypt 版本
echo "🗑️  卸載舊版 bcrypt..."
pip uninstall -y bcrypt

# 安裝兼容的 bcrypt 版本
echo "📦 安裝兼容的 bcrypt 版本..."
pip install bcrypt==4.0.1

# 重新安裝 passlib
echo "📦 重新安裝 passlib..."
pip install --force-reinstall passlib[bcrypt]==1.7.4

# 安裝其他依賴
echo "📦 安裝其他依賴..."
pip install -r requirements.txt

echo ""
echo "✅ bcrypt 修復完成！"
echo "現在可以重新啟動服務："
echo "  python run.py"
echo "================================"
