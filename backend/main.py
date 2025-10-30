
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import os

from database import get_db, engine, Base, SessionLocal
from models import User, Post, Comment, Like, Blacklist, TargetType
from schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    PostCreate, PostUpdate, PostResponse,
    CommentCreate, CommentUpdate, CommentResponse,
    LikeCreate, LikeResponse,
    BlacklistCreate, BlacklistResponse
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_active_user, verify_token
)
from config import settings

# 建立資料庫表
Base.metadata.create_all(bind=engine)

# 檢查並初始化資料庫（如果沒有資料）
def check_and_init_db():
    """檢查資料庫是否需要初始化"""
    db = SessionLocal()
    try:
        # 檢查是否已有使用者資料
        user_count = db.query(User).count()
        if user_count == 0:
            print("ℹ️  資料庫為空，建議執行: python init_db.py init")
    except Exception as e:
        print(f"⚠️  資料庫檢查失敗: {e}")
    finally:
        db.close()

# 在應用程式啟動時檢查資料庫
check_and_init_db()

# 建立 FastAPI 應用程式
app = FastAPI(
    title=settings.app_name,
    description="社群平台後端 API",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 靜態文件服務
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 創建 API 子應用
from fastapi import APIRouter
api_router = APIRouter(prefix="/api")

# 根路由 - 返回前端頁面
@app.get("/")
async def root():
    static_file = os.path.join(static_dir, "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return {"message": "歡迎使用社群平台 API", "version": "1.0.0"}

# 前端路由將在 API 路由定義之後添加

# 健康檢查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 使用者相關 API
@api_router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """使用者註冊"""
    # 檢查使用者名是否已存在
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="使用者名已存在"
        )
    
    # 檢查電子郵件是否已存在
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="電子郵件已存在"
        )
    
    # 建立新使用者
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@api_router.post("/auth/login", response_model=Token)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """使用者登入"""
    # 驗證使用者
    user = db.query(User).filter(User.username == user_credentials.username).first()
    
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者名或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 建立 JWT Token
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """取得當前使用者資訊"""
    return current_user

# 貼文相關 API
@api_router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """建立貼文"""
    db_post = Post(
        content=post.content,
        user_id=current_user.id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post

@api_router.get("/posts", response_model=List[PostResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取得貼文列表"""
    # 取得黑名單使用者 ID
    blacklisted_users = db.query(Blacklist.blocked_user_id).filter(
        Blacklist.user_id == current_user.id
    ).subquery()
    
    # 查詢貼文（排除黑名單使用者的貼文）
    posts = db.query(Post).filter(
        Post.user_id.notin_(blacklisted_users)
    ).offset(skip).limit(limit).all()
    
    # 為每個貼文添加按讚狀態和計數
    result = []
    for post in posts:
        # 計算按讚數量
        likes_count = db.query(Like).filter(
            Like.target_type == TargetType.POST,
            Like.target_id == post.id
        ).count()
        
        # 檢查當前用戶是否已按讚
        is_liked = db.query(Like).filter(
            Like.user_id == current_user.id,
            Like.target_type == TargetType.POST,
            Like.target_id == post.id
        ).first() is not None
        
        # 計算留言數量
        comments_count = db.query(Comment).filter(
            Comment.post_id == post.id,
            Comment.parent_id.is_(None)
        ).count()
        
        # 創建響應對象
        post_dict = {
            "id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "author": post.author,
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked": is_liked
        }
        result.append(post_dict)
    
    return result

@api_router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取得單一貼文"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="貼文不存在"
        )
    
    # 檢查是否在黑名單中
    blacklist = db.query(Blacklist).filter(
        Blacklist.user_id == current_user.id,
        Blacklist.blocked_user_id == post.user_id
    ).first()
    
    if blacklist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限查看此貼文"
        )
    
    return post

@api_router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新貼文"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="貼文不存在"
        )
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限修改此貼文"
        )
    
    if post_update.content is not None:
        post.content = post_update.content
    
    db.commit()
    db.refresh(post)
    
    return post

@api_router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """刪除貼文"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="貼文不存在"
        )
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限刪除此貼文"
        )
    
    db.delete(post)
    db.commit()
    
    return {"message": "貼文已刪除"}

# 留言相關 API
@api_router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """建立留言"""
    # 檢查貼文是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="貼文不存在"
        )
    
    # 檢查是否在黑名單中
    blacklist = db.query(Blacklist).filter(
        Blacklist.user_id == current_user.id,
        Blacklist.blocked_user_id == post.user_id
    ).first()
    
    if blacklist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限對此貼文留言"
        )
    
    # 如果是回覆留言，檢查父留言是否存在
    if comment.parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == comment.parent_id).first()
        if not parent_comment or parent_comment.post_id != post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="父留言不存在或不在同一貼文"
            )
    
    db_comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        parent_id=comment.parent_id,
        content=comment.content
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return db_comment

@api_router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取得貼文留言列表"""
    # 檢查貼文是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="貼文不存在"
        )
    
    # 檢查是否在黑名單中
    blacklist = db.query(Blacklist).filter(
        Blacklist.user_id == current_user.id,
        Blacklist.blocked_user_id == post.user_id
    ).first()
    
    if blacklist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限查看此貼文留言"
        )
    
    # 取得留言（只取得頂層留言，巢狀留言會透過關聯自動載入）
    comments = db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.parent_id.is_(None)
    ).all()
    
    return comments

# 按讚相關 API
@api_router.post("/likes", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
async def create_like(
    like: LikeCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """建立按讚"""
    # 檢查是否已經按過讚
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.target_type == like.target_type,
        Like.target_id == like.target_id
    ).first()
    
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已經按過讚"
        )
    
    # 檢查目標是否存在
    if like.target_type.value == "post":
        target = db.query(Post).filter(Post.id == like.target_id).first()
    else:  # comment
        target = db.query(Comment).filter(Comment.id == like.target_id).first()
    
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="目標不存在"
        )
    
    # 檢查黑名單
    target_user_id = target.user_id if hasattr(target, 'user_id') else target.author.id
    blacklist = db.query(Blacklist).filter(
        Blacklist.user_id == current_user.id,
        Blacklist.blocked_user_id == target_user_id
    ).first()
    
    if blacklist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限對此內容按讚"
        )
    
    db_like = Like(
        user_id=current_user.id,
        target_type=like.target_type,
        target_id=like.target_id
    )
    
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    
    return db_like

@api_router.get("/likes", response_model=List[LikeResponse])
async def get_likes(
    target_type: TargetType = None,
    target_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取得按讚列表"""
    query = db.query(Like)
    
    if target_type and target_id:
        query = query.filter(
            Like.target_type == target_type,
            Like.target_id == target_id
        )
    
    likes = query.all()
    return likes

@api_router.delete("/likes/{like_id}")
async def delete_like(
    like_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取消按讚"""
    like = db.query(Like).filter(Like.id == like_id).first()
    
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="按讚記錄不存在"
        )
    
    if like.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限取消此按讚"
        )
    
    db.delete(like)
    db.commit()
    
    return {"message": "已取消按讚"}

# 黑名單相關 API
@api_router.post("/blacklist", response_model=BlacklistResponse, status_code=status.HTTP_201_CREATED)
async def add_to_blacklist(
    blacklist: BlacklistCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """加入黑名單"""
    # 檢查不能將自己加入黑名單
    if blacklist.blocked_user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能將自己加入黑名單"
        )
    
    # 檢查目標使用者是否存在
    target_user = db.query(User).filter(User.id == blacklist.blocked_user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="目標使用者不存在"
        )
    
    # 檢查是否已經在黑名單中
    existing_blacklist = db.query(Blacklist).filter(
        Blacklist.user_id == current_user.id,
        Blacklist.blocked_user_id == blacklist.blocked_user_id
    ).first()
    
    if existing_blacklist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="該使用者已在黑名單中"
        )
    
    db_blacklist = Blacklist(
        user_id=current_user.id,
        blocked_user_id=blacklist.blocked_user_id
    )
    
    db.add(db_blacklist)
    db.commit()
    db.refresh(db_blacklist)
    
    return db_blacklist

@api_router.get("/blacklist", response_model=List[BlacklistResponse])
async def get_blacklist(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取得黑名單列表"""
    blacklist = db.query(Blacklist).filter(Blacklist.user_id == current_user.id).all()
    return blacklist

@api_router.delete("/blacklist/{blacklist_id}")
async def remove_from_blacklist(
    blacklist_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """從黑名單移除"""
    blacklist = db.query(Blacklist).filter(Blacklist.id == blacklist_id).first()
    
    if not blacklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="黑名單記錄不存在"
        )
    
    if blacklist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限移除此黑名單記錄"
        )
    
    db.delete(blacklist)
    db.commit()
    
    return {"message": "已從黑名單移除"}

# 置頂留言 API
@api_router.put("/posts/{post_id}/comments/{comment_id}/top")
async def set_top_comment(
    post_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """設定置頂留言"""
    # 檢查貼文是否存在且為當前使用者所有
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="貼文不存在"
        )
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限設定此貼文的置頂留言"
        )
    
    # 檢查留言是否存在且屬於該貼文
    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.post_id == post_id
    ).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="留言不存在或不在該貼文中"
        )
    
    # 先取消其他置頂留言
    db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.is_top_comment == True
    ).update({"is_top_comment": False})
    
    # 設定新的置頂留言
    comment.is_top_comment = True
    db.commit()
    
    return {"message": "置頂留言已設定"}

# 將 API 路由包含到主應用中（在所有 API 路由定義之後）
app.include_router(api_router)

# 前端路由 - 支援 SPA 路由（必須在 API 路由之後）
@app.get("/{path:path}")
async def serve_frontend(path: str):
    # 如果是 API 路由，讓 FastAPI 處理
    if path.startswith("api/") or path.startswith("docs") or path.startswith("redoc") or path.startswith("openapi.json"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # 檢查靜態文件
    static_file = os.path.join(static_dir, path)
    if os.path.exists(static_file) and os.path.isfile(static_file):
        return FileResponse(static_file)
    
    # 對於前端路由，返回 index.html
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    
    raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
