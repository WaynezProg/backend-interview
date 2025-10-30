#!/usr/bin/env python3
"""
測試認證 API 是否正常工作
"""

import requests
import json

def test_auth_api():
    base_url = "http://localhost:8000"
    
    print("🧪 測試認證 API...")
    
    # 測試註冊 API
    print("\n1. 測試註冊 API...")
    try:
        response = requests.post(f"{base_url}/api/auth/register", 
                               json={
                                   "username": "testuser123",
                                   "email": "test@example.com",
                                   "password": "testpassword123"
                               })
        print(f"   狀態碼: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ 註冊成功")
        elif response.status_code == 400:
            print("   ⚠️  用戶已存在")
        else:
            print(f"   ❌ 註冊失敗: {response.text}")
    except Exception as e:
        print(f"   ❌ 註冊請求失敗: {e}")
    
    # 測試登入 API
    print("\n2. 測試登入 API...")
    try:
        response = requests.post(f"{base_url}/api/auth/login", 
                               json={
                                   "username": "testuser123",
                                   "password": "testpassword123"
                               })
        print(f"   狀態碼: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print("   ✅ 登入成功")
            print(f"   Token: {token[:20]}...")
            
            # 測試 /api/auth/me
            print("\n3. 測試 /api/auth/me API...")
            headers = {"Authorization": f"Bearer {token}"}
            me_response = requests.get(f"{base_url}/api/auth/me", headers=headers)
            print(f"   狀態碼: {me_response.status_code}")
            if me_response.status_code == 200:
                user_data = me_response.json()
                print("   ✅ 獲取用戶信息成功")
                print(f"   用戶名: {user_data.get('username')}")
            else:
                print(f"   ❌ 獲取用戶信息失敗: {me_response.text}")
        else:
            print(f"   ❌ 登入失敗: {response.text}")
    except Exception as e:
        print(f"   ❌ 登入請求失敗: {e}")
    
    print("\n🎉 認證 API 測試完成！")

if __name__ == "__main__":
    test_auth_api()
