#!/usr/bin/env python3
"""
測試登入 API 修復
"""

import requests
import json

def test_login_api():
    base_url = "http://localhost:8000"
    
    print("🧪 測試登入 API 修復...")
    
    # 測試登入 API
    print("\n1. 測試登入 API...")
    try:
        response = requests.post(f"{base_url}/api/auth/login", 
                               json={
                                   "username": "testuser",
                                   "password": "testpassword"
                               })
        print(f"   狀態碼: {response.status_code}")
        print(f"   響應頭: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ 登入成功")
            print(f"   Token: {data.get('access_token', 'N/A')[:20]}...")
        elif response.status_code == 401:
            print("   ⚠️  認證失敗（用戶不存在或密碼錯誤）")
        elif response.status_code == 405:
            print("   ❌ 方法不允許 - 路由配置問題")
        else:
            print(f"   ❌ 登入失敗: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 登入請求失敗: {e}")
    
    # 測試註冊 API
    print("\n2. 測試註冊 API...")
    try:
        response = requests.post(f"{base_url}/api/auth/register", 
                               json={
                                   "username": "testuser123",
                                   "email": "test123@example.com",
                                   "password": "testpassword123"
                               })
        print(f"   狀態碼: {response.status_code}")
        
        if response.status_code == 201:
            print("   ✅ 註冊成功")
        elif response.status_code == 400:
            print("   ⚠️  用戶已存在")
        elif response.status_code == 405:
            print("   ❌ 方法不允許 - 路由配置問題")
        else:
            print(f"   ❌ 註冊失敗: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 註冊請求失敗: {e}")
    
    print("\n🎉 登入 API 測試完成！")

if __name__ == "__main__":
    test_login_api()
