import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { postsAPI, likesAPI } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const Dashboard = () => {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [newPost, setNewPost] = useState('')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [creating, setCreating] = useState(false)
  
  const { user } = useAuth()

  // 載入貼文列表
  const loadPosts = async () => {
    try {
      setLoading(true)
      const response = await postsAPI.getPosts()
      setPosts(response.data)
    } catch (err) {
      setError('載入貼文失敗')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPosts()
  }, [])

  // 創建新貼文
  const handleCreatePost = async (e) => {
    e.preventDefault()
    if (!newPost.trim()) return

    try {
      setCreating(true)
      await postsAPI.createPost({ content: newPost })
      setNewPost('')
      setShowCreateForm(false)
      loadPosts() // 重新載入貼文列表
    } catch (err) {
      setError('創建貼文失敗')
    } finally {
      setCreating(false)
    }
  }

  // 按讚/取消按讚功能
  const handleLike = async (postId) => {
    try {
      // 找到對應的貼文
      const post = posts.find(p => p.id === postId)
      if (!post) return

      // 檢查是否已按讚
      if (post.is_liked) {
        // 已按讚，需要取消按讚
        const likesResponse = await likesAPI.getLikes('post', postId)
        const likes = likesResponse.data
        const userLike = likes.find(like => like.user_id === user?.id)
        
        if (userLike) {
          await likesAPI.deleteLike(userLike.id)
        }
      } else {
        // 未按讚，新增按讚
        await likesAPI.createLike({
          target_type: 'post',
          target_id: postId
        })
      }
      
      loadPosts() // 重新載入以更新按讚數
    } catch (err) {
      console.error('按讚操作失敗:', err)
      setError('按讚操作失敗')
    }
  }

  // 刪除貼文
  const handleDeletePost = async (postId) => {
    if (!window.confirm('確定要刪除此貼文嗎？')) return

    try {
      await postsAPI.deletePost(postId)
      loadPosts()
    } catch (err) {
      setError('刪除貼文失敗')
    }
  }

  // 置頂/取消置頂貼文
  const handlePinPost = async (postId) => {
    try {
      await postsAPI.pinPost(postId)
      loadPosts()
    } catch (err) {
      setError('置頂貼文失敗')
    }
  }

  const handleUnpinPost = async (postId) => {
    try {
      await postsAPI.unpinPost(postId)
      loadPosts()
    } catch (err) {
      setError('取消置頂失敗')
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
      <div className="d-flex justify-between align-center mb-3">
        <h1>貼文列表</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? '取消' : '發表新貼文'}
        </button>
      </div>

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

      {/* 創建貼文表單 */}
      {showCreateForm && (
        <div className="card mb-3">
          <h3>發表新貼文</h3>
          <form onSubmit={handleCreatePost}>
            <div className="form-group">
              <textarea
                value={newPost}
                onChange={(e) => setNewPost(e.target.value)}
                className="form-textarea"
                placeholder="分享你的想法..."
                rows="3"
              />
            </div>
            <div className="d-flex gap-1">
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={creating || !newPost.trim()}
              >
                {creating ? '發布中...' : '發布'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => {
                  setShowCreateForm(false)
                  setNewPost('')
                }}
              >
                取消
              </button>
            </div>
          </form>
        </div>
      )}

      {/* 貼文列表 */}
      {posts.length === 0 ? (
        <div className="card text-center">
          <p>還沒有貼文，快來發表第一篇吧！</p>
        </div>
      ) : (
        <div className="grid">
          {posts.map((post) => (
            <div key={post.id} className="card">
              <div className="d-flex justify-between align-center mb-2">
                <h3>
                  {post.author?.username || '未知使用者'}
                  {post.is_pinned && (
                    <span style={{
                      marginLeft: 8,
                      background: '#ffc107',
                      color: '#000',
                      padding: '2px 6px',
                      borderRadius: '3px',
                      fontSize: '12px'
                    }}>置頂</span>
                  )}
                </h3>
                <small style={{ color: '#666' }}>
                  {new Date(post.created_at).toLocaleString('zh-TW')}
                </small>
              </div>
              
              <p style={{ marginBottom: '16px', whiteSpace: 'pre-wrap' }}>
                {post.content}
              </p>

              <div className="d-flex justify-between align-center">
                <div className="d-flex gap-1">
                  <button 
                    className={`btn ${post.is_liked ? 'btn-warning' : 'btn-success'}`}
                    onClick={() => handleLike(post.id)}
                  >
                    👍 {post.likes_count || 0}
                  </button>
                  <Link 
                    to={`/post/${post.id}`} 
                    className="btn btn-secondary"
                  >
                    查看留言 ({post.comments_count || 0})
                  </Link>
                </div>

                {post.user_id === user?.id && (
                  <div className="d-flex gap-1">
                    {post.is_pinned ? (
                      <button 
                        className="btn btn-secondary"
                        onClick={() => handleUnpinPost(post.id)}
                      >
                        取消置頂
                      </button>
                    ) : (
                      <button 
                        className="btn btn-warning"
                        onClick={() => handlePinPost(post.id)}
                      >
                        設為置頂
                      </button>
                    )}
                    <button 
                      className="btn btn-danger"
                      onClick={() => handleDeletePost(post.id)}
                    >
                      刪除
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Dashboard
