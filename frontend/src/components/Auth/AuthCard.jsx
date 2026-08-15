import { useState } from 'react'
import { register, login } from '../../api'
import './AuthCard.css'

function AuthCard({ onAuthSuccess, initialTab = 'login' }) {
  const [authMode, setAuthMode] = useState(initialTab)
  const [formData, setFormData] = useState({ username: '', password: '', role: 'player' })
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  // Username validation checks
  const uLen = formData.username.length >= 5
  const uCases = /[a-z]/.test(formData.username) && /[A-Z]/.test(formData.username)

  // Password validation checks
  const pLen = formData.password.length >= 5
  const pAlpha = /[a-zA-Z]/.test(formData.password)
  const pNum = /[0-9]/.test(formData.password)
  const pSpec = /[$%*&@]/.test(formData.password)

  const isFormValid = authMode === 'login' || (uLen && uCases && pLen && pAlpha && pNum && pSpec)

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
        <h2>{authMode === 'login' ? 'Log in' : 'Create Account'}</h2>
        <p>
          {authMode === 'login'
            ? 'Welcome back! Login to continue.'
            : 'Join Guess The Word to play or manage reports'}
        </p>
      </div>

      <form className="form-stack" onSubmit={handleSubmit}>
        {/* Username Field */}
        <label>
          Username
          <input
            type="text"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            placeholder={authMode === 'register' ? 'e.g. PlayerOne' : 'Enter username'}
            required
            maxLength={20}
          />
          {authMode === 'register' && (
            <ul className="req-rules-list">
              <li className={uLen ? 'rule-met' : 'rule-unmet'}>
                • At least 5 letters long
              </li>
              <li className={uCases ? 'rule-met' : 'rule-unmet'}>
                • Contains both uppercase & lowercase letters
              </li>
            </ul>
          )}
        </label>

        {/* Password Field */}
        <label>
          Password
          <div className="password-input-wrapper">
            <input
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              placeholder={authMode === 'register' ? 'e.g. Player1*' : 'Enter password'}
              required
            />
            <button
              type="button"
              className="password-toggle-btn"
              onClick={() => setShowPassword(!showPassword)}
              title={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
          {authMode === 'register' && (
            <ul className="req-rules-list">
              <li className={pLen ? 'rule-met' : 'rule-unmet'}>
                • At least 5 characters long
              </li>
              <li className={pAlpha ? 'rule-met' : 'rule-unmet'}>
                • Contains alpha character (a-z, A-Z)
              </li>
              <li className={pNum ? 'rule-met' : 'rule-unmet'}>
                • Contains numeric character (0-9)
              </li>
              <li className={pSpec ? 'rule-met' : 'rule-unmet'}>
                • Contains special char ($, %, *, &)
              </li>
            </ul>
          )}
        </label>

        {/* Account Role Dropdown (Registration Only) */}
        {authMode === 'register' && (
          <label className="role-select">
            Account Role
            <select
              value={formData.role}
              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              className="role-dropdown-input"
            >
              <option value="player">Player (Play Word Guessing Game)</option>
              <option value="admin">Admin (View Analytics & Reports)</option>
            </select>
          </label>
        )}

        {/* Submit Button */}
        <div className="button-row">
          <button
            type="submit"
            className="primary-btn"
            disabled={loading || (authMode === 'register' && !isFormValid)}
          >
            {loading && <span className="loading-spinner" />}
            {authMode === 'login' ? 'Log in' : 'Register'}
          </button>
        </div>
      </form>

      {/* Switch Tab Toggle */}
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

      {message && <div className="status-message error">{message}</div>}
    </section>
  )
}

export default AuthCard
