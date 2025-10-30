import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            社群平台控制台
          </Link>
          
          {isAuthenticated() ? (
            <div className="navbar-nav">
              <Link to="/" className="nav-link">首頁</Link>
              <Link to="/users" className="nav-link">使用者管理</Link>
              <span className="nav-link">歡迎，{user?.username}</span>
              <button onClick={handleLogout} className="btn btn-secondary">
                登出
              </button>
            </div>
          ) : (
            <div className="navbar-nav">
              <Link to="/login" className="nav-link">登入</Link>
              <Link to="/register" className="nav-link">註冊</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
