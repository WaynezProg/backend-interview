# 社群平台前端控制介面

這是一個基於 React 的簡潔前端控制介面，用於管理社群平台的所有功能。

## 🚀 快速開始

### 1. 安裝依賴
```bash
cd frontend
npm install
```

### 2. 啟動開發服務器
```bash
npm run dev
```

前端將在 http://localhost:3000 運行

### 3. 確保後端服務運行
確保後端 API 服務在 http://localhost:8000 運行：
```bash
cd ../backend
python run.py
```

## 📋 功能特色

### 🔐 身份驗證
- 使用者註冊和登入
- JWT Token 自動管理
- 受保護的路由

### 📝 貼文管理
- 查看所有貼文列表
- 創建新貼文
- 編輯和刪除自己的貼文
- 按讚功能

### 💬 留言系統
- 查看貼文的所有留言
- 發表新留言
- 支援巢狀回覆
- 按讚留言
- 設定置頂留言（貼文擁有者）

### 👥 使用者管理
- 黑名單管理
- 封鎖/解封使用者
- 權限控制

## 🛠️ 技術架構

### 核心技術
- **React 18** - 現代化 UI 框架
- **React Router** - 客戶端路由
- **Axios** - HTTP 客戶端
- **Context API** - 狀態管理
- **Vite** - 快速構建工具

### 項目結構
```
frontend/
├── src/
│   ├── components/          # 可重用組件
│   │   ├── Navbar.jsx      # 導航欄
│   │   └── ProtectedRoute.jsx  # 受保護路由
│   ├── contexts/           # React Context
│   │   └── AuthContext.jsx # 認證上下文
│   ├── pages/              # 頁面組件
│   │   ├── Login.jsx       # 登入頁面
│   │   ├── Register.jsx    # 註冊頁面
│   │   ├── Dashboard.jsx   # 主控制台
│   │   ├── PostDetail.jsx  # 貼文詳情
│   │   └── UserManagement.jsx  # 使用者管理
│   ├── services/           # API 服務
│   │   └── api.js         # API 客戶端
│   ├── App.jsx            # 主應用組件
│   ├── main.jsx           # 應用入口
│   └── index.css          # 全域樣式
├── index.html             # HTML 模板
├── package.json           # 項目配置
├── vite.config.js         # Vite 配置
└── README.md             # 說明文檔
```

## 🎨 設計特色

### 簡潔的 UI 設計
- 現代化的卡片式佈局
- 響應式設計，支援桌面和移動端
- 直觀的操作界面
- 清晰的視覺層次

### 用戶體驗優化
- 載入狀態提示
- 錯誤處理和提示
- 確認對話框
- 自動表單驗證

## 🔧 開發說明

### 環境要求
- Node.js 16+
- npm 或 yarn
- 後端 API 服務運行在 8000 端口

### 開發命令
```bash
# 啟動開發服務器
npm run dev

# 構建生產版本
npm run build

# 預覽生產版本
npm run preview
```

### API 整合
前端通過 `/api` 前綴代理所有 API 請求到後端：
- 認證 API: `/api/auth/*`
- 貼文 API: `/api/posts/*`
- 留言 API: `/api/posts/*/comments/*`
- 按讚 API: `/api/likes/*`
- 黑名單 API: `/api/blacklist/*`

## 📱 響應式設計

前端採用響應式設計，支援：
- 桌面端 (1200px+)
- 平板端 (768px - 1199px)
- 移動端 (< 768px)

## 🔒 安全性

- JWT Token 自動管理
- 受保護的路由
- 自動登出機制
- 輸入驗證和清理

## 🚀 部署

### 構建生產版本
```bash
npm run build
```

構建後的檔案將在 `dist/` 目錄中。

### 靜態文件服務
可以使用任何靜態文件服務器來提供構建後的檔案，例如：
- Nginx
- Apache
- Vercel
- Netlify

## 📝 使用指南

### 1. 註冊和登入
- 訪問 http://localhost:3000/register 註冊新帳號
- 訪問 http://localhost:3000/login 登入現有帳號

### 2. 管理貼文
- 在首頁查看所有貼文
- 點擊「發表新貼文」創建新內容
- 點擊「查看留言」進入貼文詳情頁面

### 3. 互動功能
- 對貼文和留言按讚
- 發表留言和回覆
- 設定置頂留言（僅限貼文擁有者）

### 4. 使用者管理
- 前往「使用者管理」頁面
- 輸入使用者 ID 加入黑名單
- 管理現有的黑名單列表

## 🐛 故障排除

### 常見問題

1. **API 請求失敗**
   - 確保後端服務正在運行
   - 檢查 API 端點是否正確

2. **認證問題**
   - 清除瀏覽器本地存儲
   - 重新登入

3. **樣式問題**
   - 清除瀏覽器快取
   - 重新啟動開發服務器

## 📞 支援

如有問題，請檢查：
1. 後端 API 是否正常運行
2. 網路連接是否正常
3. 瀏覽器控制台是否有錯誤訊息

---

**開發時間**: 2024年10月29日  
**技術棧**: React 18 + Vite + Axios  
**專案狀態**: ✅ 完成並測試通過
