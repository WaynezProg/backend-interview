#!/usr/bin/env python3
"""
資料庫種子資料腳本
用於建立測試資料和範例內容
"""
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Post, Comment, Like, Blacklist, TargetType
from auth import get_password_hash
from datetime import datetime, timedelta
import random

def create_seed_data():
    """建立種子資料"""
    print("🌱 開始建立種子資料...")
    
    db = SessionLocal()
    
    try:
        # 檢查是否已有資料
        if db.query(User).count() > 0:
            print("ℹ️  資料庫已有資料，跳過種子資料建立")
            return
        
        # 1. 建立使用者
        print("👥 建立使用者...")
        users_data = [
            {"username": "alice", "email": "alice@example.com", "password": "password123"},
            {"username": "bob", "email": "bob@example.com", "password": "password123"},
            {"username": "charlie", "email": "charlie@example.com", "password": "password123"},
            {"username": "diana", "email": "diana@example.com", "password": "password123"},
            {"username": "eve", "email": "eve@example.com", "password": "password123"},
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=get_password_hash(user_data["password"])
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        print(f"✅ 建立了 {len(users)} 個使用者")
        
        # 2. 建立貼文
        print("📝 建立貼文...")
        posts_data = [
            {"content": "今天天氣真好！大家有什麼推薦的戶外活動嗎？", "user_id": 0},
            {"content": "剛學會了新的程式語言，感覺很有成就感！", "user_id": 1},
            {"content": "分享一個好用的開發工具，推薦給大家！", "user_id": 2},
            {"content": "週末計畫去爬山，有人要一起嗎？", "user_id": 3},
            {"content": "最近在學習機器學習，有推薦的課程嗎？", "user_id": 4},
            {"content": "今天嘗試了新的料理，結果還不錯！", "user_id": 0},
            {"content": "工作壓力好大，需要一些放鬆的方法...", "user_id": 1},
        ]
        
        posts = []
        for post_data in posts_data:
            post = Post(
                content=post_data["content"],
                user_id=users[post_data["user_id"]].id
            )
            db.add(post)
            posts.append(post)
        
        db.commit()
        print(f"✅ 建立了 {len(posts)} 篇貼文")
        
        # 3. 建立留言
        print("💬 建立留言...")
        comments_data = [
            {"content": "我推薦去公園散步！", "post_id": 0, "user_id": 1},
            {"content": "騎腳踏車也不錯喔", "post_id": 0, "user_id": 2},
            {"content": "恭喜！學什麼語言呢？", "post_id": 1, "user_id": 0},
            {"content": "Python，很適合初學者", "post_id": 1, "user_id": 1, "parent_id": 2},
            {"content": "我也在學 Python！", "post_id": 1, "user_id": 3, "parent_id": 2},
            {"content": "什麼工具這麼好用？", "post_id": 2, "user_id": 0},
            {"content": "VS Code，功能很強大", "post_id": 2, "user_id": 2, "parent_id": 5},
            {"content": "我也想去！什麼時候？", "post_id": 3, "user_id": 0},
            {"content": "週六早上，要一起嗎？", "post_id": 3, "user_id": 3, "parent_id": 7},
            {"content": "Coursera 上的機器學習課程不錯", "post_id": 4, "user_id": 0},
            {"content": "什麼料理？看起來很好吃！", "post_id": 5, "user_id": 1},
            {"content": "試試冥想或運動", "post_id": 6, "user_id": 2},
        ]
        
        comments = []
        for comment_data in comments_data:
            comment = Comment(
                content=comment_data["content"],
                post_id=posts[comment_data["post_id"]].id,
                user_id=users[comment_data["user_id"]].id,
                parent_id=comment_data.get("parent_id")
            )
            db.add(comment)
            comments.append(comment)
        
        db.commit()
        print(f"✅ 建立了 {len(comments)} 則留言")
        
        # 4. 建立按讚
        print("👍 建立按讚...")
        likes_data = [
            # 貼文按讚
            {"target_type": TargetType.POST, "target_id": posts[0].id, "user_id": 1},
            {"target_type": TargetType.POST, "target_id": posts[0].id, "user_id": 2},
            {"target_type": TargetType.POST, "target_id": posts[1].id, "user_id": 0},
            {"target_type": TargetType.POST, "target_id": posts[1].id, "user_id": 3},
            {"target_type": TargetType.POST, "target_id": posts[2].id, "user_id": 0},
            {"target_type": TargetType.POST, "target_id": posts[2].id, "user_id": 1},
            {"target_type": TargetType.POST, "target_id": posts[3].id, "user_id": 0},
            {"target_type": TargetType.POST, "target_id": posts[4].id, "user_id": 1},
            {"target_type": TargetType.POST, "target_id": posts[5].id, "user_id": 2},
            {"target_type": TargetType.POST, "target_id": posts[6].id, "user_id": 3},
            # 留言按讚
            {"target_type": TargetType.COMMENT, "target_id": comments[0].id, "user_id": 0},
            {"target_type": TargetType.COMMENT, "target_id": comments[1].id, "user_id": 0},
            {"target_type": TargetType.COMMENT, "target_id": comments[2].id, "user_id": 1},
            {"target_type": TargetType.COMMENT, "target_id": comments[3].id, "user_id": 0},
            {"target_type": TargetType.COMMENT, "target_id": comments[4].id, "user_id": 0},
            {"target_type": TargetType.COMMENT, "target_id": comments[5].id, "user_id": 1},
            {"target_type": TargetType.COMMENT, "target_id": comments[6].id, "user_id": 0},
            {"target_type": TargetType.COMMENT, "target_id": comments[7].id, "user_id": 1},
            {"target_type": TargetType.COMMENT, "target_id": comments[8].id, "user_id": 2},
            {"target_type": TargetType.COMMENT, "target_id": comments[9].id, "user_id": 1},
        ]
        
        for like_data in likes_data:
            like = Like(
                user_id=users[like_data["user_id"]].id,
                target_type=like_data["target_type"],
                target_id=like_data["target_id"]
            )
            db.add(like)
        
        db.commit()
        print(f"✅ 建立了 {len(likes_data)} 個按讚")
        
        # 5. 建立黑名單（模擬一些使用者關係）
        print("🚫 建立黑名單...")
        blacklist_data = [
            {"user_id": 0, "blocked_user_id": 4},  # alice 封鎖 eve
            {"user_id": 1, "blocked_user_id": 3},  # bob 封鎖 diana
        ]
        
        for blacklist_item in blacklist_data:
            blacklist = Blacklist(
                user_id=users[blacklist_item["user_id"]].id,
                blocked_user_id=users[blacklist_item["blocked_user_id"]].id
            )
            db.add(blacklist)
        
        db.commit()
        print(f"✅ 建立了 {len(blacklist_data)} 個黑名單記錄")
        
        # 6. 設定置頂留言
        print("📌 設定置頂留言...")
        # 將第一篇貼文的第一則留言設為置頂
        if comments:
            comments[0].is_top_comment = True
            db.commit()
            print("✅ 置頂留言設定完成")
        
        print("\n🎉 種子資料建立完成！")
        print("\n📝 測試帳號:")
        for i, user_data in enumerate(users_data):
            print(f"  {i+1}. 使用者名: {user_data['username']}")
            print(f"     密碼: {user_data['password']}")
            print(f"     電子郵件: {user_data['email']}")
            print()
        
        print("📊 資料統計:")
        print(f"  使用者: {db.query(User).count()}")
        print(f"  貼文: {db.query(Post).count()}")
        print(f"  留言: {db.query(Comment).count()}")
        print(f"  按讚: {db.query(Like).count()}")
        print(f"  黑名單: {db.query(Blacklist).count()}")
        
    except Exception as e:
        print(f"❌ 建立種子資料時發生錯誤: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()
