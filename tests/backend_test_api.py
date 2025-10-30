#!/usr/bin/env python3
"""
API 測試腳本
用於快速測試社群平台 API 的基本功能
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """測試 API 基本功能"""
    print("🚀 開始測試社群平台 API...")
    
    # 1. 測試健康檢查
    print("\n1. 測試健康檢查...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.json()}")
    
    # 2. 註冊使用者
    print("\n2. 註冊使用者...")
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"狀態碼: {response.status_code}")
    if response.status_code == 201:
        print("✅ 使用者註冊成功")
        user_info = response.json()
        print(f"使用者 ID: {user_info['id']}")
    else:
        print(f"❌ 註冊失敗: {response.text}")
        return
    
    # 3. 登入取得 Token
    print("\n3. 使用者登入...")
    login_data = {
        "username": "testuser2",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"狀態碼: {response.status_code}")
    if response.status_code == 200:
        print("✅ 登入成功")
        token_data = response.json()
        token = token_data["access_token"]
        print(f"Token: {token[:50]}...")
    else:
        print(f"❌ 登入失敗: {response.text}")
        return
    
    # 設定 Authorization Header
    headers = {"Authorization": f"Bearer {token}"}
    
    # 4. 建立貼文
    print("\n4. 建立貼文...")
    post_data = {
        "content": "這是我的第一篇貼文！歡迎大家來互動～"
    }
    response = requests.post(f"{BASE_URL}/api/posts", json=post_data, headers=headers)
    print(f"狀態碼: {response.status_code}")
    if response.status_code == 201:
        print("✅ 貼文建立成功")
        post_info = response.json()
        post_id = post_info["id"]
        print(f"貼文 ID: {post_id}")
    else:
        print(f"❌ 貼文建立失敗: {response.text}")
        return
    
    # 5. 取得貼文列表
    print("\n5. 取得貼文列表...")
    response = requests.get(f"{BASE_URL}/api/posts", headers=headers)
    print(f"狀態碼: {response.status_code}")
    if response.status_code == 200:
        print("✅ 取得貼文列表成功")
        posts = response.json()
        print(f"貼文數量: {len(posts)}")
    else:
        print(f"❌ 取得貼文列表失敗: {response.text}")
    
    # 6. 建立留言
    print("\n6. 建立留言...")
    comment_data = {
        "content": "這篇貼文很棒！"
    }
    response = requests.post(f"{BASE_URL}/api/posts/{post_id}/comments", json=comment_data, headers=headers)
    print(f"狀態碼: {response.status_code}")
    if response.status_code == 201:
        print("✅ 留言建立成功")
        comment_info = response.json()
        comment_id = comment_info["id"]
        print(f"留言 ID: {comment_id}")
    else:
        print(f"❌ 留言建立失敗: {response.text}")
    
    # 7. 按讚貼文
    print("\n7. 按讚貼文...")
    like_data = {
        "target_type": "post",
        "target_id": post_id
    }
    response = requests.post(f"{BASE_URL}/api/likes", json=like_data, headers=headers)
    print(f"狀態碼: {response.status_code}")
    if response.status_code == 201:
        print("✅ 按讚成功")
    else:
        print(f"❌ 按讚失敗: {response.text}")
    
    # 8. 取得使用者資訊
    print("\n8. 取得使用者資訊...")
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print(f"狀態碼: {response.status_code}")
    if response.status_code == 200:
        print("✅ 取得使用者資訊成功")
        user_info = response.json()
        print(f"使用者名: {user_info['username']}")
        print(f"電子郵件: {user_info['email']}")
    else:
        print(f"❌ 取得使用者資訊失敗: {response.text}")
    
    print("\n🎉 API 測試完成！")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 API 服務器，請確保服務器正在運行")
        print("執行: python run.py")
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
