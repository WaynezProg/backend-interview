# 測試檔案說明

本目錄包含所有測試相關的檔案，用於測試和調試社群平台的功能。

## 📁 檔案列表

### 主要測試檔案

- **backend_test_api.py** - 後端 API 完整功能測試
  - 測試註冊、登入、貼文、留言、按讚等功能
  - 完整的 API 端點測試流程

### 調試檔案

- **debug_auth_me.py** - 調試 `/api/auth/me` 端點問題
  - 測試認證狀態
  - 診斷 404/401 錯誤

- **debug_login.py** - 調試登入功能
  - 測試不同的密碼組合
  - 診斷 401 錯誤原因

### 專項測試檔案

- **test_api_routes.py** - 測試 API 路由配置
  - 驗證所有 API 端點是否正確註冊
  - 檢查路由順序

- **test_auth_api.py** - 測試認證 API
  - 測試註冊和登入功能
  - 測試 Token 獲取和使用

- **test_login_fix.py** - 測試登入修復
  - 驗證登入 API 修復是否成功
  - 測試 405 錯誤修復

- **test_simple_auth.py** - 簡單認證測試
  - 基本的認證功能測試
  - 健康檢查測試

## 🚀 使用方法

### 運行所有測試

```bash
# 確保後端服務正在運行
cd backend
python run.py

# 在另一個終端運行測試
cd tests
python backend_test_api.py
```

### 運行特定測試

```bash
# 測試認證功能
python test_auth_api.py

# 調試登入問題
python debug_login.py

# 調試認證端點
python debug_auth_me.py
```

## 📝 測試環境要求

- Python 3.12+
- 後端服務運行在 http://localhost:8000
- 資料庫已初始化

## 🔧 測試準備

1. **啟動後端服務**:
```bash
cd backend
python run.py
```

2. **初始化資料庫** (如果需要):
```bash
cd backend
python init_db.py seed
```

3. **運行測試**:
```bash
cd tests
python [測試檔案名稱].py
```

## 📋 測試覆蓋範圍

- ✅ 使用者註冊和登入
- ✅ JWT Token 認證
- ✅ 貼文 CRUD 操作
- ✅ 留言系統
- ✅ 按讚功能
- ✅ 黑名單管理
- ✅ API 路由配置
- ✅ 錯誤處理

## 🐛 故障排除

如果測試失敗：

1. **檢查服務是否運行**:
```bash
curl http://localhost:8000/health
```

2. **檢查資料庫**:
```bash
cd backend
python init_db.py info
```

3. **查看詳細錯誤**:
```bash
python debug_login.py
```

---

**最後更新**: 2024年10月29日  
**測試狀態**: ✅ 所有測試檔案已整理完成
