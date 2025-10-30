import React, { useState, useEffect } from 'react'
import { blacklistAPI } from '../services/api'

const UserManagement = () => {
  const [blacklist, setBlacklist] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [newBlockUserId, setNewBlockUserId] = useState('')
  const [adding, setAdding] = useState(false)

  // 載入黑名單列表
  const loadBlacklist = async () => {
    try {
      setLoading(true)
      const response = await blacklistAPI.getBlacklist()
      setBlacklist(response.data)
    } catch (err) {
      setError('載入黑名單失敗')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadBlacklist()
  }, [])

  // 加入黑名單
  const handleAddToBlacklist = async (e) => {
    e.preventDefault()
    if (!newBlockUserId.trim()) return

    try {
      setAdding(true)
      await blacklistAPI.addToBlacklist(parseInt(newBlockUserId))
      setNewBlockUserId('')
      loadBlacklist()
    } catch (err) {
      setError(err.response?.data?.detail || '加入黑名單失敗')
    } finally {
      setAdding(false)
    }
  }

  // 從黑名單移除
  const handleRemoveFromBlacklist = async (blacklistId) => {
    if (!window.confirm('確定要從黑名單中移除此使用者嗎？')) return

    try {
      await blacklistAPI.removeFromBlacklist(blacklistId)
      loadBlacklist()
    } catch (err) {
      setError('移除黑名單失敗')
    }
  }

  if (loading) {
    return (
      <div className="text-center">
        <p>載入中...</p>
      </div>
    )
  }

  return (
    <div>
      <h1>使用者管理</h1>
      <p className="mb-3">管理你的黑名單，被加入黑名單的使用者將無法看到你的貼文或與你互動。</p>

      {error && (
        <div style={{ 
          background: '#f8d7da', 
          color: '#721c24', 
          padding: '12px', 
          borderRadius: '4px', 
          marginBottom: '16px' 
        }}>
          {error}
        </div>
      )}

      {/* 加入黑名單表單 */}
      <div className="card mb-3">
        <h3>加入黑名單</h3>
        <form onSubmit={handleAddToBlacklist}>
          <div className="form-group">
            <label className="form-label">使用者 ID</label>
            <input
              type="number"
              value={newBlockUserId}
              onChange={(e) => setNewBlockUserId(e.target.value)}
              className="form-input"
              placeholder="輸入要封鎖的使用者 ID"
              required
            />
            <small style={{ color: '#666' }}>
              提示：你可以在貼文詳情頁面查看使用者 ID
            </small>
          </div>
          <button 
            type="submit" 
            className="btn btn-danger"
            disabled={adding || !newBlockUserId.trim()}
          >
            {adding ? '加入中...' : '加入黑名單'}
          </button>
        </form>
      </div>

      {/* 黑名單列表 */}
      <div className="card">
        <h3>黑名單列表 ({blacklist.length})</h3>
        
        {blacklist.length === 0 ? (
          <p style={{ color: '#666' }}>黑名單是空的</p>
        ) : (
          <div className="grid">
            {blacklist.map((item) => (
              <div key={item.id} className="card" style={{ marginBottom: '12px' }}>
                <div className="d-flex justify-between align-center">
                  <div>
                    <h4>使用者 ID: {item.blocked_user_id}</h4>
                    <small style={{ color: '#666' }}>
                      加入時間: {new Date(item.created_at).toLocaleString('zh-TW')}
                    </small>
                  </div>
                  <button 
                    className="btn btn-secondary"
                    onClick={() => handleRemoveFromBlacklist(item.id)}
                  >
                    移除
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 使用說明 */}
      <div className="card mt-3">
        <h3>使用說明</h3>
        <ul style={{ paddingLeft: '20px' }}>
          <li>被加入黑名單的使用者將無法看到你發布的貼文</li>
          <li>被加入黑名單的使用者無法對你的貼文或留言按讚</li>
          <li>被加入黑名單的使用者無法對你的貼文或留言進行回覆</li>
          <li>你可以隨時從黑名單中移除使用者</li>
          <li>要查看使用者 ID，請前往貼文詳情頁面</li>
        </ul>
      </div>
    </div>
  )
}

export default UserManagement
