#!/usr/bin/env python3
"""
測試 API 路由是否正確配置
"""

import requests
import json

def test_api_routes():
    base_url = "http://localhost:8000"
    
    print("🧪 測試 API 路由配置...")
    
    # 測試健康檢查
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ 健康檢查: {response.status_code}")
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}")
    
    # 測試 API 文檔
    try:
        response = requests.get(f"{base_url}/docs")
        print(f"✅ API 文檔: {response.status_code}")
    except Exception as e:
        print(f"❌ API 文檔失敗: {e}")
    
    # 測試登入 API
    try:
        response = requests.post(f"{base_url}/api/auth/login", 
                               json={"username": "test", "password": "test"})
        print(f"✅ 登入 API: {response.status_code} (預期 401 或 422)")
    except Exception as e:
        print(f"❌ 登入 API 失敗: {e}")
    
    # 測試註冊 API
    try:
        response = requests.post(f"{base_url}/api/auth/register", 
                               json={"username": "test", "email": "test@test.com", "password": "test"})
        print(f"✅ 註冊 API: {response.status_code} (預期 201 或 400)")
    except Exception as e:
        print(f"❌ 註冊 API 失敗: {e}")
    
    # 測試貼文 API
    try:
        response = requests.get(f"{base_url}/api/posts")
        print(f"✅ 貼文 API: {response.status_code} (預期 401)")
    except Exception as e:
        print(f"❌ 貼文 API 失敗: {e}")
    
    print("\n🎉 API 路由測試完成！")
    print("如果看到 401 狀態碼，表示 API 路由配置正確（需要認證）")

if __name__ == "__main__":
    test_api_routes()
