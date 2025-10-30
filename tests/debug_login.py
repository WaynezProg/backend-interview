#!/usr/bin/env python3
"""
調試登入 401 錯誤
"""

import requests
import json

def debug_login():
    base_url = "http://localhost:8000"
    
    print("🔍 調試登入 401 錯誤...")
    
    # 測試登入 API
    print("\n1. 測試登入 API:")
    try:
        # 使用資料庫中存在的用戶
        response = requests.post(f"{base_url}/api/auth/login", 
                               json={
                                   "username": "wayne",
                                   "password": "test123"  # 嘗試常見密碼
                               })
        print(f"   狀態碼: {response.status_code}")
        print(f"   響應頭: {dict(response.headers)}")
        print(f"   響應內容: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ 登入成功")
            print(f"   Token: {data.get('access_token', 'N/A')[:20]}...")
        elif response.status_code == 401:
            print("   ❌ 認證失敗 - 用戶名或密碼錯誤")
        else:
            print(f"   ⚠️  意外狀態碼")
            
    except Exception as e:
        print(f"   ❌ 請求失敗: {e}")
    
    # 測試不同的密碼
    print("\n2. 測試不同密碼:")
    passwords_to_try = ["password", "123456", "admin", "wayne", ""]
    
    for pwd in passwords_to_try:
        try:
            response = requests.post(f"{base_url}/api/auth/login", 
                                   json={
                                       "username": "wayne",
                                       "password": pwd
                                   })
            print(f"   密碼 '{pwd}': {response.status_code}")
            if response.status_code == 200:
                print("   ✅ 找到正確密碼!")
                break
        except Exception as e:
            print(f"   密碼 '{pwd}': 請求失敗 - {e}")
    
    # 測試註冊新用戶
    print("\n3. 測試註冊新用戶:")
    try:
        response = requests.post(f"{base_url}/api/auth/register", 
                               json={
                                   "username": "testuser",
                                   "email": "test@example.com",
                                   "password": "testpassword123"
                               })
        print(f"   註冊狀態碼: {response.status_code}")
        print(f"   註冊響應: {response.text}")
        
        if response.status_code == 201:
            print("   ✅ 註冊成功")
            
            # 嘗試用新用戶登入
            print("\n4. 用新用戶登入:")
            login_response = requests.post(f"{base_url}/api/auth/login", 
                                         json={
                                             "username": "testuser",
                                             "password": "testpassword123"
                                         })
            print(f"   登入狀態碼: {login_response.status_code}")
            print(f"   登入響應: {login_response.text}")
            
            if login_response.status_code == 200:
                print("   ✅ 新用戶登入成功")
            else:
                print("   ❌ 新用戶登入失敗")
        else:
            print("   ❌ 註冊失敗")
            
    except Exception as e:
        print(f"   ❌ 註冊請求失敗: {e}")
    
    print("\n🎉 登入調試完成！")

if __name__ == "__main__":
    debug_login()
