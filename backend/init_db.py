#!/usr/bin/env python3
"""
資料庫初始化腳本
用於建立資料庫表和初始資料
"""
import asyncio
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import User
from auth import get_password_hash

def init_database():
    """初始化資料庫"""
    print("🚀 開始初始化資料庫...")
    
    # 建立所有資料表
    print("📋 建立資料表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 資料表建立完成")
    
    # 建立資料庫會話
    db = SessionLocal()
    
    try:
        # 檢查是否已有使用者
        existing_user = db.query(User).first()
        if existing_user:
            print("ℹ️  資料庫已有資料，跳過初始化")
            return
        
        # 建立基本測試使用者
        print("👤 建立基本測試使用者...")
        test_users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password": "admin123"
            },
            {
                "username": "testuser1",
                "email": "user1@example.com",
                "password": "password123"
            },
            {
                "username": "testuser2",
                "email": "user2@example.com",
                "password": "password123"
            }
        ]
        
        for user_data in test_users:
            hashed_password = get_password_hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=hashed_password
            )
            db.add(user)
        
        db.commit()
        print("✅ 基本測試使用者建立完成")
        
        print("🎉 資料庫初始化完成！")
        print("\n📝 基本測試帳號:")
        for user_data in test_users:
            print(f"  使用者名: {user_data['username']}")
            print(f"  密碼: {user_data['password']}")
            print(f"  電子郵件: {user_data['email']}")
            print()
        
        print("\n💡 提示：")
        print("  執行 'python seed_data.py' 可以建立更多測試資料")
        
    except Exception as e:
        print(f"❌ 初始化過程中發生錯誤: {e}")
        db.rollback()
    finally:
        db.close()

def init_with_seed():
    """初始化資料庫並建立種子資料"""
    print("🚀 開始初始化資料庫並建立種子資料...")
    
    # 建立所有資料表
    print("📋 建立資料表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 資料表建立完成")
    
    # 匯入並執行種子資料腳本
    try:
        from seed_data import create_seed_data
        create_seed_data()
    except ImportError:
        print("❌ 無法匯入種子資料腳本")
    except Exception as e:
        print(f"❌ 建立種子資料時發生錯誤: {e}")

def reset_database():
    """重置資料庫（刪除所有資料）"""
    print("⚠️  警告：即將刪除所有資料庫資料！")
    confirm = input("確定要繼續嗎？(y/N): ")
    
    if confirm.lower() != 'y':
        print("❌ 操作已取消")
        return
    
    print("🗑️  刪除所有資料表...")
    Base.metadata.drop_all(bind=engine)
    print("✅ 資料表已刪除")
    
    print("🔄 重新建立資料表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 資料表重新建立完成")
    
    print("🎉 資料庫重置完成！")

def show_database_info():
    """顯示資料庫資訊"""
    print("📊 資料庫資訊:")
    print(f"  資料庫 URL: {engine.url}")
    print(f"  資料表數量: {len(Base.metadata.tables)}")
    print("  資料表列表:")
    for table_name in Base.metadata.tables.keys():
        print(f"    - {table_name}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_database()
        elif command == "seed":
            init_with_seed()
        elif command == "reset":
            reset_database()
        elif command == "info":
            show_database_info()
        else:
            print("❌ 未知命令")
            print("可用命令: init, seed, reset, info")
    else:
        print("🔧 資料庫管理工具")
        print("\n可用命令:")
        print("  python init_db.py init   - 初始化資料庫（基本使用者）")
        print("  python init_db.py seed   - 初始化資料庫並建立種子資料")
        print("  python init_db.py reset  - 重置資料庫")
        print("  python init_db.py info   - 顯示資料庫資訊")
        print("\n範例:")
        print("  python init_db.py init   # 基本初始化")
        print("  python init_db.py seed   # 完整初始化（推薦）")
