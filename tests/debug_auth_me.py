#!/usr/bin/env python3
"""
調試 /api/auth/me 端點問題
"""

import requests
import json

def debug_auth_me():
    base_url = "http://localhost:8000"
    
    print("🔍 調試 /api/auth/me 端點...")
    
    # 1. 測試沒有認證的情況
    print("\n1. 測試沒有認證的情況:")
    try:
        response = requests.get(f"{base_url}/api/auth/me")
        print(f"   狀態碼: {response.status_code}")
        print(f"   響應頭: {dict(response.headers)}")
        if response.status_code == 422:
            print("   ✅ 正確返回 422 (缺少認證信息)")
        elif response.status_code == 401:
            print("   ✅ 正確返回 401 (認證失敗)")
        elif response.status_code == 404:
            print("   ❌ 錯誤返回 404 (路由不存在)")
        else:
            print(f"   ⚠️  意外狀態碼: {response.text}")
    except Exception as e:
        print(f"   ❌ 請求失敗: {e}")
    
    # 2. 測試無效的認證
    print("\n2. 測試無效的認證:")
    try:
        headers = {"Authorization": "Bearer invalid_token"}
        response = requests.get(f"{base_url}/api/auth/me", headers=headers)
        print(f"   狀態碼: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ 正確返回 401 (認證失敗)")
        elif response.status_code == 404:
            print("   ❌ 錯誤返回 404 (路由不存在)")
        else:
            print(f"   ⚠️  意外狀態碼: {response.text}")
    except Exception as e:
        print(f"   ❌ 請求失敗: {e}")
    
    # 3. 先註冊並登入獲取有效 token
    print("\n3. 測試有效認證:")
    try:
        # 註冊用戶
        register_response = requests.post(f"{base_url}/api/auth/register", 
                                        json={
                                            "username": "debuguser",
                                            "email": "debug@example.com",
                                            "password": "debugpass123"
                                        })
        print(f"   註冊狀態碼: {register_response.status_code}")
        
        if register_response.status_code in [201, 400]:  # 201 成功或 400 已存在
            # 登入獲取 token
            login_response = requests.post(f"{base_url}/api/auth/login", 
                                         json={
                                             "username": "debuguser",
                                             "password": "debugpass123"
                                         })
            print(f"   登入狀態碼: {login_response.status_code}")
            
            if login_response.status_code == 200:
                token_data = login_response.json()
                token = token_data.get('access_token')
                print(f"   Token: {token[:20]}...")
                
                # 使用 token 調用 /api/auth/me
                headers = {"Authorization": f"Bearer {token}"}
                me_response = requests.get(f"{base_url}/api/auth/me", headers=headers)
                print(f"   /api/auth/me 狀態碼: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    user_data = me_response.json()
                    print("   ✅ 成功獲取用戶信息")
                    print(f"   用戶名: {user_data.get('username')}")
                elif me_response.status_code == 404:
                    print("   ❌ 錯誤返回 404 (路由不存在)")
                else:
                    print(f"   ⚠️  意外狀態碼: {me_response.text}")
            else:
                print(f"   ❌ 登入失敗: {login_response.text}")
        else:
            print(f"   ❌ 註冊失敗: {register_response.text}")
            
    except Exception as e:
        print(f"   ❌ 測試失敗: {e}")
    
    print("\n🎉 調試完成！")

if __name__ == "__main__":
    debug_auth_me()
