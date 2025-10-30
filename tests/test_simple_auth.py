#!/usr/bin/env python3
"""
簡單測試認證問題
"""

import requests

def test_simple_auth():
    base_url = "http://localhost:8000"
    
    print("🧪 簡單測試認證...")
    
    # 測試 /api/auth/me 沒有認證
    print("\n1. 測試 /api/auth/me 沒有認證:")
    try:
        response = requests.get(f"{base_url}/api/auth/me")
        print(f"   狀態碼: {response.status_code}")
        print(f"   響應: {response.text[:200]}")
        
        if response.status_code == 422:
            print("   ✅ 正確返回 422 (缺少認證信息)")
        elif response.status_code == 401:
            print("   ✅ 正確返回 401 (認證失敗)")
        elif response.status_code == 404:
            print("   ❌ 錯誤返回 404 (路由不存在)")
        else:
            print(f"   ⚠️  意外狀態碼")
            
    except Exception as e:
        print(f"   ❌ 請求失敗: {e}")
    
    # 測試其他 API 端點
    print("\n2. 測試 /api/posts 沒有認證:")
    try:
        response = requests.get(f"{base_url}/api/posts")
        print(f"   狀態碼: {response.status_code}")
        print(f"   響應: {response.text[:200]}")
        
        if response.status_code == 422:
            print("   ✅ 正確返回 422 (缺少認證信息)")
        elif response.status_code == 401:
            print("   ✅ 正確返回 401 (認證失敗)")
        elif response.status_code == 404:
            print("   ❌ 錯誤返回 404 (路由不存在)")
        else:
            print(f"   ⚠️  意外狀態碼")
            
    except Exception as e:
        print(f"   ❌ 請求失敗: {e}")
    
    # 測試健康檢查
    print("\n3. 測試 /health:")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   狀態碼: {response.status_code}")
        print(f"   響應: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ 健康檢查正常")
        else:
            print(f"   ❌ 健康檢查失敗")
            
    except Exception as e:
        print(f"   ❌ 請求失敗: {e}")

if __name__ == "__main__":
    test_simple_auth()
