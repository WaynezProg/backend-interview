import axios from 'axios'

// 創建 axios 實例
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 請求攔截器 - 添加認證 token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 響應攔截器 - 處理認證錯誤
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 認證 API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getCurrentUser: () => api.get('/auth/me'),
}

// 貼文 API
export const postsAPI = {
  getPosts: (skip = 0, limit = 10) => api.get(`/posts?skip=${skip}&limit=${limit}`),
  getPost: (id) => api.get(`/posts/${id}`),
  createPost: (postData) => api.post('/posts', postData),
  updatePost: (id, postData) => api.put(`/posts/${id}`, postData),
  deletePost: (id) => api.delete(`/posts/${id}`),
}

// 留言 API
export const commentsAPI = {
  getComments: (postId) => api.get(`/posts/${postId}/comments`),
  createComment: (postId, commentData) => api.post(`/posts/${postId}/comments`, commentData),
  setTopComment: (postId, commentId) => api.put(`/posts/${postId}/comments/${commentId}/top`),
}

// 按讚 API
export const likesAPI = {
  createLike: (likeData) => api.post('/likes', likeData),
  deleteLike: (likeId) => api.delete(`/likes/${likeId}`),
}

// 黑名單 API
export const blacklistAPI = {
  getBlacklist: () => api.get('/blacklist'),
  addToBlacklist: (userId) => api.post('/blacklist', { blocked_user_id: userId }),
  removeFromBlacklist: (blacklistId) => api.delete(`/blacklist/${blacklistId}`),
}

export default api
