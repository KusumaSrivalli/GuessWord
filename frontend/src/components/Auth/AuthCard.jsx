import { useState } from 'react'
import { register, login } from '../../api'
import './AuthCard.css'

function AuthCard({ onAuthSuccess }) {
  const [authMode, setAuthMode] = useState('login')
  const [formData, setFormData] = useState({ username: '', password: '', role: 'player' })
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage('')
    setLoading(true)
    try {
      if (authMode === 'register') {
        await register(formData.username, formData.password, formData.role)
        const loginData = await login(formData.username, formData.password)
        onAuthSuccess(loginData.user)
      } else {
        const loginData = await login(formData.username, formData.password)
        onAuthSuccess(loginData.user)
      }
      setFormData({ username: '', password: '', role: 'player' })
    } catch (err) {
      setMessage(err.error || 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card auth-card">
      <div className="section-heading">
        <h2>{authMode === 'login' ? 'Log in' : 'Create account'}</h2>
        <p>{authMode === 'login' ? 'Welcome back! Please login.' : 'Create a new account to get started.'}</p>
      </div>

      <form className="form-stack" onSubmit={handleSubmit}>
        <label>
          Username
          <input
            type="text"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            placeholder="At least 5 letters (upper & lower)"
            required
            maxLength={20}
          />
        </label>
        <label>
          Password
          <div className="password-input-wrapper">
            <input
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              placeholder="Letters, numbers, and $ % * &"
              required
            />
            <button
              type="button"
              className="password-toggle-btn"
              onClick={() => setShowPassword(!showPassword)}
              title={showPassword ? "Hide password" : "Show password"}
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
        </label>
        {authMode === 'register' && (
          <label className="role-select">
            Role
            <select
              value={formData.role}
              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
            >
              <option value="player">Player</option>
              <option value="admin">Admin</option>
            </select>
          </label>
        )}
        <div className="button-row">
          <button type="submit" className="primary-btn" disabled={loading}>
            {loading && <span className="loading-spinner" />}
            {authMode === 'login' ? 'Log in' : 'Register'}
          </button>
        </div>
      </form>

      <div className="toggle-row">
        <button
          type="button"
          className="text-btn"
          onClick={() => {
            setAuthMode(authMode === 'login' ? 'register' : 'login')
            setMessage('')
          }}
        >
          {authMode === 'login'
            ? 'Need an account? Register'
            : 'Already have an account? Log in'}
        </button>
      </div>

      {message && <div className="status-message">{message}</div>}
    </section>
  )
}

export default AuthCard
