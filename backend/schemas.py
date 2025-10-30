from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional, List
from datetime import datetime
from models import TargetType

# 使用者相關 Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# 貼文相關 Schema
class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    content: Optional[str] = None

class PostResponse(PostBase):
    id: int
    user_id: int
    author: UserResponse
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes_count: int = 0
    comments_count: int = 0
    is_liked: bool = False  # 當前用戶是否已按讚
    
    class Config:
        from_attributes = True

# 留言相關 Schema
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    parent_id: Optional[int] = None

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    parent_id: Optional[int] = None
    is_top_comment: bool
    author: UserResponse
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes_count: int = 0
    replies: List['CommentResponse'] = []
    
    class Config:
        from_attributes = True

# 按讚相關 Schema
class LikeCreate(BaseModel):
    target_type: TargetType
    target_id: int

class LikeResponse(BaseModel):
    id: int
    user_id: int
    target_type: TargetType
    target_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 黑名單相關 Schema
class BlacklistCreate(BaseModel):
    blocked_user_id: int

class BlacklistResponse(BaseModel):
    id: int
    user_id: int
    blocked_user_id: int
    blocked_user: UserResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

# 更新 CommentResponse 的 forward reference
CommentResponse.model_rebuild()
