#!/usr/bin/env python3
"""
調試按讚 API 400 錯誤
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_likes_api():
    """測試按讚 API"""
    print("🔍 調試按讚 API 400 錯誤...")
    
    # 1. 先登入獲取 token
    print("\n1. 登入獲取 token...")
    login_data = {
        "username": "wayne",
        "password": "wayne"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"登入狀態碼: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ 登入失敗: {response.text}")
        return
    
    token_data = response.json()
    token = token_data["access_token"]
    print(f"✅ 登入成功，Token: {token[:50]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. 獲取貼文列表
    print("\n2. 獲取貼文列表...")
    response = requests.get(f"{BASE_URL}/api/posts", headers=headers)
    print(f"貼文列表狀態碼: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ 獲取貼文失敗: {response.text}")
        return
    
    posts = response.json()
    print(f"✅ 找到 {len(posts)} 篇貼文")
    
    if not posts:
        print("❌ 沒有貼文可以測試按讚")
        return
    
    post_id = posts[0]["id"]
    print(f"使用貼文 ID: {post_id}")
    
    # 3. 測試不同的按讚請求格式
    print("\n3. 測試按讚請求格式...")
    
    # 測試格式 1: 使用字串 "post"
    print("\n測試格式 1: target_type = 'post'")
    like_data1 = {
        "target_type": "post",
        "target_id": post_id
    }
    response = requests.post(f"{BASE_URL}/api/likes", json=like_data1, headers=headers)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    # 測試格式 2: 使用枚舉值 "POST"
    print("\n測試格式 2: target_type = 'POST'")
    like_data2 = {
        "target_type": "POST",
        "target_id": post_id
    }
    response = requests.post(f"{BASE_URL}/api/likes", json=like_data2, headers=headers)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    # 測試格式 3: 檢查是否已經按過讚
    print("\n測試格式 3: 檢查重複按讚")
    like_data3 = {
        "target_type": "post",
        "target_id": post_id
    }
    response = requests.post(f"{BASE_URL}/api/likes", json=like_data3, headers=headers)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    # 4. 測試無效的 target_id
    print("\n4. 測試無效的 target_id...")
    like_data4 = {
        "target_type": "post",
        "target_id": 99999
    }
    response = requests.post(f"{BASE_URL}/api/likes", json=like_data4, headers=headers)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")
    
    # 5. 測試無效的 target_type
    print("\n5. 測試無效的 target_type...")
    like_data5 = {
        "target_type": "invalid_type",
        "target_id": post_id
    }
    response = requests.post(f"{BASE_URL}/api/likes", json=like_data5, headers=headers)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.text}")

if __name__ == "__main__":
    try:
        test_likes_api()
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 API 服務器，請確保服務器正在運行")
        print("執行: cd backend && python run.py")
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
