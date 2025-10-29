# 社群平台後端 API

基於 FastAPI 開發的社群平台後端 API，支援使用者系統、發文、互動及黑名單等功能。

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 初始化資料庫

**基本初始化（只有使用者帳號）:**
```bash
python init_db.py init
```

**完整初始化（包含測試資料）:**
```bash
python init_db.py seed
```

### 3. 啟動服務

```bash
python run.py
```

或

```bash
python main.py
```

### 4. 訪問 API 文檔

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. 測試 API

```bash
python test_api.py
```

## 📋 API 功能

### 身份驗證
- `POST /auth/register` - 使用者註冊
- `POST /auth/login` - 使用者登入
- `GET /auth/me` - 取得當前使用者資訊

### 貼文管理
- `POST /posts` - 建立貼文
- `GET /posts` - 取得貼文列表
- `GET /posts/{post_id}` - 取得單一貼文
- `PUT /posts/{post_id}` - 更新貼文
- `DELETE /posts/{post_id}` - 刪除貼文

### 留言系統
- `POST /posts/{post_id}/comments` - 建立留言
- `GET /posts/{post_id}/comments` - 取得留言列表
- `PUT /posts/{post_id}/comments/{comment_id}/top` - 設定置頂留言

### 互動功能
- `POST /likes` - 按讚（支援貼文和留言）
- `DELETE /likes/{like_id}` - 取消按讚

### 黑名單管理
- `POST /blacklist` - 加入黑名單
- `GET /blacklist` - 取得黑名單列表
- `DELETE /blacklist/{blacklist_id}` - 從黑名單移除

## 🛠️ 技術特色

- **非同步設計**: 全面使用 async/await 模式
- **JWT 身份驗證**: 安全的 Token 機制
- **密碼加密**: 使用 bcrypt 加密密碼
- **資料庫關聯**: 支援巢狀留言和複雜關聯
- **黑名單機制**: 完整的權限控制
- **自動文檔**: 自動生成 API 文檔

## 📊 資料庫設計

- **users**: 使用者資料
- **posts**: 貼文資料
- **comments**: 留言資料（支援巢狀結構）
- **likes**: 按讚記錄
- **blacklists**: 黑名單記錄

## 🔧 開發說明

### 專案結構
```
backend/
├── main.py          # 主應用程式
├── models.py        # 資料庫模型
├── schemas.py       # Pydantic 模型
├── auth.py          # 身份驗證
├── database.py      # 資料庫配置
├── config.py        # 設定檔
├── init_db.py       # 資料庫初始化工具
├── seed_data.py     # 種子資料腳本
├── test_api.py      # API 測試腳本
├── run.py           # 啟動腳本
└── requirements.txt # 依賴清單
```

### 資料庫管理工具

#### 初始化資料庫
```bash
# 基本初始化（只有使用者帳號）
python init_db.py init

# 完整初始化（包含測試資料）
python init_db.py seed
```

#### 重置資料庫
```bash
python init_db.py reset
```

#### 查看資料庫資訊
```bash
python init_db.py info
```

#### 建立種子資料
```bash
python seed_data.py
```

### 環境變數
建立 `.env` 檔案（可選）：
```
DATABASE_URL=sqlite:///./social_platform.db
SECRET_KEY=your-secret-key
DEBUG=True
```

## 🧪 測試範例

### 1. 註冊使用者
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. 登入取得 Token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 3. 建立貼文
```bash
curl -X POST "http://localhost:8000/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "這是我的第一篇貼文！"
  }'
```

## 📝 注意事項

- 所有需要身份驗證的 API 都需要在 Header 中攜帶 `Authorization: Bearer <token>`
- 黑名單功能會影響使用者對特定內容的存取權限
- 支援巢狀留言，可以對任何留言進行回覆
- 每個貼文只能有一個置頂留言
