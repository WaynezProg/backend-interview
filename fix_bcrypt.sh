#!/bin/bash

# ============================================================================
# ⚠️  注意：此腳本為歷史修復腳本，現已不需要使用
# ============================================================================
# 
# 此腳本用於修復 bcrypt 密碼加密兼容性問題（2024年10月）。
# 
# 【現狀說明】
# - ✅ 問題已在程式碼中修復（backend/auth.py 已加入密碼長度截斷邏輯）
# - ✅ 依賴版本已在 requirements.txt 中鎖定（bcrypt==4.0.1）
# - ✅ 新環境可直接使用 `pip install -r requirements.txt` 安裝
# 
# 【何時需要此腳本】
# 僅在以下情況需要執行此腳本：
# 1. 現有環境中 bcrypt 版本不兼容，出現密碼加密錯誤
# 2. 需要快速修復舊環境的依賴問題
# 
# 【新環境設置】
# 對於新環境，建議直接使用：
# ```bash
# cd backend
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# ```
# 
# ============================================================================

echo "🔧 修復 bcrypt 密碼加密問題"
echo "================================"
echo "⚠️  注意：此腳本為歷史修復腳本"
echo "   新環境建議直接使用: pip install -r requirements.txt"
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
