import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { postsAPI, commentsAPI, likesAPI } from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const PostDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  
  const [post, setPost] = useState(null)
  const [comments, setComments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [newComment, setNewComment] = useState('')
  const [replyingTo, setReplyingTo] = useState(null)
  const [creating, setCreating] = useState(false)

  // 載入貼文詳情
  const loadPost = async () => {
    try {
      setLoading(true)
      const response = await postsAPI.getPost(id)
      setPost(response.data)
    } catch (err) {
      setError('載入貼文失敗')
    } finally {
      setLoading(false)
    }
  }

  // 載入留言列表
  const loadComments = async () => {
    try {
      const response = await commentsAPI.getComments(id)
      setComments(response.data)
    } catch (err) {
      console.error('載入留言失敗:', err)
    }
  }

  useEffect(() => {
    loadPost()
    loadComments()
  }, [id])

  // 創建留言
  const handleCreateComment = async (e) => {
    e.preventDefault()
    if (!newComment.trim()) return

    try {
      setCreating(true)
      await commentsAPI.createComment(id, {
        content: newComment,
        parent_id: replyingTo
      })
      setNewComment('')
      setReplyingTo(null)
      loadComments()
    } catch (err) {
      setError('創建留言失敗')
    } finally {
      setCreating(false)
    }
  }

  // 按讚/取消按讚功能（針對貼文與留言分支）
  const handleLike = async (targetType, targetId) => {
    try {
      if (targetType === 'post') {
        // 使用當前貼文狀態決定按讚/取消
        const likesResponse = await likesAPI.getLikes('post', targetId)
        const likes = likesResponse.data
        const userLike = likes.find(like => like.user_id === user?.id)

        if (post?.is_liked && userLike) {
          await likesAPI.deleteLike(userLike.id)
        } else {
          await likesAPI.createLike({ target_type: 'post', target_id: targetId })
        }

        await loadPost()
      } else {
        // comment 分支
        const commentsRes = await commentsAPI.getComments(id)
        const comment = commentsRes.data.find(c => c.id === targetId)

        const likesResponse = await likesAPI.getLikes('comment', targetId)
        const likes = likesResponse.data
        const userLike = likes.find(like => like.user_id === user?.id)

        if (comment?.is_liked && userLike) {
          await likesAPI.deleteLike(userLike.id)
        } else {
          await likesAPI.createLike({ target_type: 'comment', target_id: targetId })
        }

        await loadComments()
      }
    } catch (err) {
      console.error('按讚操作失敗:', err)
    }
  }

  // 貼文置頂/取消置頂（僅貼文作者可用）
  const handlePinPost = async () => {
    try {
      await postsAPI.pinPost(post.id)
      await loadPost()
    } catch (err) {
      setError('置頂貼文失敗')
    }
  }

  const handleUnpinPost = async () => {
    try {
      await postsAPI.unpinPost(post.id)
      await loadPost()
    } catch (err) {
      setError('取消置頂失敗')
    }
  }

  // 設定置頂留言
  const handleSetTopComment = async (commentId) => {
    try {
      await commentsAPI.setTopComment(id, commentId)
      loadComments()
    } catch (err) {
      setError('設定置頂留言失敗')
    }
  }

  // 渲染留言組件
  const renderComment = (comment, level = 0) => {
    return (
      <div 
        key={comment.id} 
        style={{ 
          marginLeft: level * 20, 
          marginBottom: '12px',
          padding: '12px',
          background: level > 0 ? '#f8f9fa' : 'white',
          border: '1px solid #e9ecef',
          borderRadius: '4px'
        }}
      >
        <div className="d-flex justify-between align-center mb-1">
          <strong>{comment.author?.username || '未知使用者'}</strong>
          <div className="d-flex gap-1">
            <small style={{ color: '#666' }}>
              {new Date(comment.created_at).toLocaleString('zh-TW')}
            </small>
            {comment.is_top_comment && (
              <span style={{ 
                background: '#ffc107', 
                color: '#000', 
                padding: '2px 6px', 
                borderRadius: '3px', 
                fontSize: '12px' 
              }}>
                置頂
              </span>
            )}
          </div>
        </div>
        
        <p style={{ marginBottom: '8px', whiteSpace: 'pre-wrap' }}>
          {comment.content}
        </p>

        <div className="d-flex gap-1">
          <button 
            className={`btn ${comment.is_liked ? 'btn-warning' : 'btn-success'}`}
            onClick={() => handleLike('comment', comment.id)}
          >
            👍 {comment.likes_count || 0}
          </button>
          <button 
            className="btn btn-secondary"
            onClick={() => setReplyingTo(comment.id)}
          >
            回覆
          </button>
          {user?.id && !comment.is_top_comment && level === 0 && (
            <button 
              className="btn btn-warning"
              onClick={() => handleSetTopComment(comment.id)}
              disabled={post?.user_id !== user?.id}
              title={post?.user_id !== user?.id ? '僅貼文作者可設定置頂' : undefined}
            >
              設為置頂
            </button>
          )}
        </div>

        {/* 回覆表單 */}
        {replyingTo === comment.id && (
          <form onSubmit={handleCreateComment} style={{ marginTop: '8px' }}>
            <div className="form-group">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                className="form-textarea"
                placeholder="回覆留言..."
                rows="2"
              />
            </div>
            <div className="d-flex gap-1">
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={creating || !newComment.trim()}
              >
                {creating ? '回覆中...' : '回覆'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => {
                  setReplyingTo(null)
                  setNewComment('')
                }}
              >
                取消
              </button>
            </div>
          </form>
        )}

        {/* 巢狀留言 */}
        {comment.replies && comment.replies.length > 0 && (
          <div style={{ marginTop: '8px' }}>
            {comment.replies.map(reply => renderComment(reply, level + 1))}
          </div>
        )}
      </div>
    )
  }

  if (loading) {
    return (
      <div className="text-center">
        <p>載入中...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <p style={{ color: '#dc3545' }}>{error}</p>
        <button className="btn btn-primary" onClick={() => navigate('/')}>
          返回首頁
        </button>
      </div>
    )
  }

  if (!post) {
    return (
      <div className="card">
        <p>貼文不存在</p>
        <button className="btn btn-primary" onClick={() => navigate('/')}>
          返回首頁
        </button>
      </div>
    )
  }

  return (
    <div>
      <div className="d-flex justify-between align-center mb-3">
        <button 
          className="btn btn-secondary"
          onClick={() => navigate('/')}
        >
          ← 返回首頁
        </button>
        <h1>貼文詳情</h1>
      </div>

      {/* 貼文內容 */}
      <div className="card mb-3">
        <div className="d-flex justify-between align-center mb-2">
          <h2>
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
          </h2>
          <small style={{ color: '#666' }}>
            {new Date(post.created_at).toLocaleString('zh-TW')}
          </small>
        </div>
        
        <p style={{ marginBottom: '16px', whiteSpace: 'pre-wrap' }}>
          {post.content}
        </p>

        <div className="d-flex gap-1">
          <button 
            className={`btn ${post?.is_liked ? 'btn-warning' : 'btn-success'}`}
            onClick={() => handleLike('post', post.id)}
          >
            👍 {post?.likes_count || 0}
          </button>
          {user?.id === post?.user_id && (
            post.is_pinned ? (
              <button 
                className="btn btn-secondary"
                onClick={handleUnpinPost}
              >
                取消置頂
              </button>
            ) : (
              <button 
                className="btn btn-warning"
                onClick={handlePinPost}
              >
                設為置頂
              </button>
            )
          )}
        </div>
      </div>

      {/* 留言表單 */}
      <div className="card mb-3">
        <h3>發表留言</h3>
        <form onSubmit={handleCreateComment}>
          <div className="form-group">
            <textarea
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              className="form-textarea"
              placeholder="分享你的想法..."
              rows="3"
            />
          </div>
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={creating || !newComment.trim()}
          >
            {creating ? '發布中...' : '發布留言'}
          </button>
        </form>
      </div>

      {/* 留言列表 */}
      <div className="card">
        <h3>留言 ({comments.length})</h3>
        {comments.length === 0 ? (
          <p style={{ color: '#666' }}>還沒有留言，快來發表第一篇吧！</p>
        ) : (
          <div>
            {comments.map(comment => renderComment(comment))}
          </div>
        )}
      </div>
    </div>
  )
}

export default PostDetail
