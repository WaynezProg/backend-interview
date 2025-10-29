#!/usr/bin/env python3
"""
社群平台後端 API 啟動腳本
"""
import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開發模式，檔案變更時自動重載
        log_level="info"
    )
