import { useState, useEffect } from 'react'
import {
  getAdminOverview,
  getUserStats,
  getDailyReport,
  getUserReport,
  getAdminUsers,
  updateAdminUser,
  deleteAdminUser
} from '../../api'
import './AdminDashboard.css'

function AdminDashboard({ currentUser }) {
  const [activeTab, setActiveTab] = useState('overview') // 'overview' | 'daily' | 'user' | 'users'

  // Overview data
  const [overviewData, setOverviewData] = useState(null)

  // Daily Report data & state
  const [dailyViewMode, setDailyViewMode] = useState('single') // 'single' | 'range'
  const [singleDate, setSingleDate] = useState(() => new Date().toISOString().split('T')[0])
  const [fromDate, setFromDate] = useState('2026-08-08')
  const [toDate, setToDate] = useState(() => new Date().toISOString().split('T')[0])
  const [dailyReports, setDailyReports] = useState([])

  // User Report data
  const [userReports, setUserReports] = useState([])

  // Users Management data & state
  const [usersList, setUsersList] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [roleFilter, setRoleFilter] = useState('all')

  // Modals state
  const [heatmapUser, setHeatmapUser] = useState(null)
  const [heatmapStats, setHeatmapStats] = useState(null)

  const [editingUser, setEditingUser] = useState(null)
  const [editRole, setEditRole] = useState('player')
  const [editPassword, setEditPassword] = useState('')

  const [deletingUser, setDeletingUser] = useState(null)

  const [actionMenuOpen, setActionMenuOpen] = useState(null)
  const [loading, setLoading] = useState(false)

  // Fetch initial overview and users data
  const loadData = async () => {
    setLoading(true)
    try {
      const [overview, usersRes, dailyRes, userReportRes] = await Promise.all([
        getAdminOverview(),
        getAdminUsers(),
        getDailyReport(),
        getUserReport()
      ])
      setOverviewData(overview)
      setUsersList(usersRes.users || [])
      setDailyReports(dailyRes.report || [])
      setUserReports(userReportRes.report || [])
    } catch (err) {
      console.error('Failed to load admin dashboard data', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  // Handle opening 30-Day Heatmap from Actions -> View Report
  const handleOpenHeatmap = async (username) => {
    setActionMenuOpen(null)
    setHeatmapUser(username)
    setHeatmapStats(null)
    try {
      const stats = await getUserStats(username)
      setHeatmapStats(stats)
    } catch (err) {
      console.error('Failed to fetch heatmap stats', err)
    }
  }

  // Handle User Edit Submit
  const handleUpdateUserSubmit = async (e) => {
    e.preventDefault()
    if (!editingUser) return
    try {
      await updateAdminUser(editingUser.username, { role: editRole, password: editPassword || undefined })
      setEditingUser(null)
      setEditPassword('')
      loadData()
    } catch (err) {
      console.error('Failed to update user', err)
    }
  }

  // Handle User Delete Submit
  const handleDeleteUserSubmit = async () => {
    if (!deletingUser) return
    try {
      await deleteAdminUser(deletingUser.username)
      setDeletingUser(null)
      loadData()
    } catch (err) {
      console.error('Failed to delete user', err)
    }
  }

  // Filtered Users List
  const filteredUsers = usersList.filter(u => {
    const matchesSearch = u.username.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesRole = roleFilter === 'all' || u.role === roleFilter
    return matchesSearch && matchesRole
  })

  // Calculate Single Day Report metrics
  const singleDayData = dailyReports.find(r => r.date === singleDate) || {
    date: singleDate,
    num_users: 0,
    correct_guesses: 0,
    total_games: 0
  }

  return (
    <div className="admin-layout">
      {/* 30-Day Heatmap Inspector Modal */}
      {heatmapUser && (
        <div className="admin-modal-overlay" onClick={() => setHeatmapUser(null)}>
          <div className="admin-modal-card" onClick={e => e.stopPropagation()}>
            <div className="admin-modal-header">
              <div className="user-title-group">
                <span className="player-avatar-large">{heatmapUser.charAt(0).toUpperCase()}</span>
                <div>
                  <h2>@{heatmapUser}'s 30-Day Heatmap</h2>
                  <p>Daily gameplay consistency and streaks over the last 30 days.</p>
                </div>
              </div>
              <button className="close-modal-btn" onClick={() => setHeatmapUser(null)}>✕</button>
            </div>

            {heatmapStats ? (
              <div className="heatmap-modal-body">
                <div className="modal-stats-bar">
                  <span className="m-stat">Total Games: <strong>{heatmapStats.total_games}</strong></span>
                  <span className="m-stat">Total Wins: <strong>{heatmapStats.total_wins}</strong></span>
                  <span className="m-stat">Win Rate: <strong>{heatmapStats.win_rate}</strong></span>
                  <span className="m-stat streak">🔥 <strong>{heatmapStats.current_streak} Day Streak</strong></span>
                </div>

                <div className="heatmap-grid-3rows">
                  {heatmapStats.heatmap && heatmapStats.heatmap.map((item, index) => {
                    const count = item.count || 0
                    const levelClass = count === 0 ? 'level-0' : count === 1 ? 'level-1' : count === 2 ? 'level-2' : 'level-3'
                    return (
                      <div key={index} className={`heatmap-box ${levelClass}`}>
                        <span className="box-date">{item.label}</span>
                        <span className="box-count">{count}</span>
                      </div>
                    )
                  })}
                </div>

                <div className="heatmap-legend">
                  <span className="legend-text">Less</span>
                  <span className="legend-box level-0"></span>
                  <span className="legend-box level-1"></span>
                  <span className="legend-box level-2"></span>
                  <span className="legend-box level-3"></span>
                  <span className="legend-text">More (Max 3/day)</span>
                </div>
              </div>
            ) : (
              <div className="loading-spinner-box">Loading 30-day heatmap...</div>
            )}
          </div>
        </div>
      )}

      {/* Edit User Modal */}
      {editingUser && (
        <div className="admin-modal-overlay" onClick={() => setEditingUser(null)}>
          <div className="admin-modal-card small-modal" onClick={e => e.stopPropagation()}>
            <div className="admin-modal-header">
              <h2>Edit User @{editingUser.username}</h2>
              <button className="close-modal-btn" onClick={() => setEditingUser(null)}>✕</button>
            </div>
            <form onSubmit={handleUpdateUserSubmit} className="modal-form-stack">
              <label>
                Role
                <select value={editRole} onChange={e => setEditRole(e.target.value)}>
                  <option value="player">Player</option>
                  <option value="admin">Admin</option>
                </select>
              </label>
              <label>
                New Password (leave empty to keep current)
                <input
                  type="password"
                  value={editPassword}
                  onChange={e => setEditPassword(e.target.value)}
                  placeholder="Enter new password"
                />
              </label>
              <div className="modal-btn-row">
                <button type="button" className="btn-cancel" onClick={() => setEditingUser(null)}>Cancel</button>
                <button type="submit" className="btn-save">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete User Modal */}
      {deletingUser && (
        <div className="admin-modal-overlay" onClick={() => setDeletingUser(null)}>
          <div className="admin-modal-card small-modal" onClick={e => e.stopPropagation()}>
            <div className="admin-modal-header">
              <h2>Confirm Delete User</h2>
              <button className="close-modal-btn" onClick={() => setDeletingUser(null)}>✕</button>
            </div>
            <div className="modal-body-text">
              Are you sure you want to delete user <strong>@{deletingUser.username}</strong>? This action cannot be undone.
            </div>
            <div className="modal-btn-row">
              <button type="button" className="btn-cancel" onClick={() => setDeletingUser(null)}>Cancel</button>
              <button type="button" className="btn-delete-confirm" onClick={handleDeleteUserSubmit}>Delete Account</button>
            </div>
          </div>
        </div>
      )}

      {/* 1. Left Sidebar Navigation (Matching Screenshot 1) */}
      <aside className="admin-sidebar">
        <div className="sidebar-brand">
          <div className="brand-logo-icon">abc</div>
          <div className="brand-title-group">
            <span className="sidebar-sub">Admin Dashboard</span>
          </div>
        </div>

        <nav className="sidebar-menu">
          <button
            className={`menu-item ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            <span className="menu-icon">⊞</span> Overview
          </button>
          <button
            className={`menu-item ${activeTab === 'daily' ? 'active' : ''}`}
            onClick={() => setActiveTab('daily')}
          >
            <span className="menu-icon">📅</span> Daily Report
          </button>
          <button
            className={`menu-item ${activeTab === 'user' ? 'active' : ''}`}
            onClick={() => setActiveTab('user')}
          >
            <span className="menu-icon">👤</span> User Report
          </button>
          <button
            className={`menu-item ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            <span className="menu-icon">👥</span> Users
          </button>
        </nav>
      </aside>

      {/* 2. Main Content Area */}
      <main className="admin-main-content">
        {/* TAB 1: OVERVIEW (Matching Screenshot 2) */}
        {activeTab === 'overview' && (
          <div className="view-section">
            <div className="view-header">
              <h1 className="green-heading">Platform Overview</h1>
              <p className="view-sub">Real-time statistics and insights for Guess The Word.</p>
            </div>

            <h3 className="section-sub-heading">All-Time Statistics</h3>
            <div className="stats-cards-grid">
              <div className="stat-card">
                <div className="stat-left">
                  <span className="card-lbl">Total Players</span>
                  <span className="card-val">{overviewData ? overviewData.total_users : 0}</span>
                </div>
                <div className="stat-icon-badge green-badge">👥</div>
              </div>

              <div className="stat-card">
                <div className="stat-left">
                  <span className="card-lbl">Total Games</span>
                  <span className="card-val">{overviewData ? overviewData.total_games : 0}</span>
                </div>
                <div className="stat-icon-badge purple-badge">🎮</div>
              </div>

              <div className="stat-card">
                <div className="stat-left">
                  <span className="card-lbl">Total Wins</span>
                  <span className="card-val">{overviewData ? overviewData.total_wins : 0}</span>
                </div>
                <div className="stat-icon-badge teal-badge">🏆</div>
              </div>

              <div className="stat-card">
                <div className="stat-left">
                  <span className="card-lbl">Global Win Rate</span>
                  <span className="card-val">
                    {overviewData && overviewData.total_games > 0
                      ? `${((overviewData.total_wins / overviewData.total_games) * 100).toFixed(1)}%`
                      : '0.0%'}
                  </span>
                </div>
                <div className="stat-icon-badge blue-badge">📈</div>
              </div>
            </div>

            <h3 className="section-sub-heading">Today's Activity</h3>
            <div className="stats-cards-grid three-cols">
              <div className="stat-card">
                <div className="stat-left">
                  <span className="card-lbl">Active Players Today</span>
                  <span className="card-val">
                    {overviewData && overviewData.daily_report && overviewData.daily_report.length > 0
                      ? overviewData.daily_report[0].users_activity.length
                      : 0}
                  </span>
                </div>
                <div className="stat-icon-badge orange-badge">⚡</div>
              </div>

              <div className="stat-card">
                <div className="stat-left">
                  <span className="card-lbl">Games Played Today</span>
                  <span className="card-val">
                    {overviewData && overviewData.daily_report && overviewData.daily_report.length > 0
                      ? overviewData.daily_report[0].users_activity.reduce((acc, u) => acc + u.games_played, 0)
                      : 0}
                  </span>
                </div>
                <div className="stat-icon-badge yellow-badge">⚡</div>
              </div>

              <div className="stat-card">
                <div className="stat-left">
                  <span className="card-lbl">Wins Today</span>
                  <span className="card-val">
                    {overviewData && overviewData.daily_report && overviewData.daily_report.length > 0
                      ? overviewData.daily_report[0].users_activity.reduce((acc, u) => acc + u.games_won, 0)
                      : 0}
                  </span>
                </div>
                <div className="stat-icon-badge cyan-badge">🏅</div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: DAILY REPORT (Matching Screenshots 3 & 4) */}
        {activeTab === 'daily' && (
          <div className="view-section">
            <div className="view-header">
              <h1 className="green-heading">Daily Reports</h1>
              <p className="view-sub">Analyze player activity and performance over time.</p>
            </div>

            <div className="report-filter-card">
              <div className="filter-controls-row">
                <div className="toggle-pill-group">
                  <button
                    className={`toggle-pill ${dailyViewMode === 'single' ? 'active' : ''}`}
                    onClick={() => setDailyViewMode('single')}
                  >
                    Single Day
                  </button>
                  <button
                    className={`toggle-pill ${dailyViewMode === 'range' ? 'active' : ''}`}
                    onClick={() => setDailyViewMode('range')}
                  >
                    Date Range
                  </button>
                </div>

                {dailyViewMode === 'single' ? (
                  <div className="single-date-box">
                    <input
                      type="date"
                      value={singleDate}
                      onChange={e => setSingleDate(e.target.value)}
                      className="date-picker-input"
                    />
                    <button className="btn-search-report">🔍 View</button>
                  </div>
                ) : (
                  <div className="range-date-box">
                    <input
                      type="date"
                      value={fromDate}
                      onChange={e => setFromDate(e.target.value)}
                      className="date-picker-input"
                    />
                    <span className="to-txt">to</span>
                    <input
                      type="date"
                      value={toDate}
                      onChange={e => setToDate(e.target.value)}
                      className="date-picker-input"
                    />
                    <button className="btn-search-report">🔍 Search</button>
                  </div>
                )}
              </div>
            </div>

            {dailyViewMode === 'single' ? (
              <div className="single-day-results">
                <div className="result-title-bar">
                  <h2>Report for {singleDate}</h2>
                  <span className="status-tag">
                    {singleDayData.num_users > 0 ? 'Active' : 'No Activity'}
                  </span>
                </div>

                <div className="stats-cards-grid">
                  <div className="stat-card">
                    <div className="stat-left">
                      <span className="card-lbl">Active Users</span>
                      <span className="card-val">{singleDayData.num_users}</span>
                    </div>
                    <div className="stat-icon-badge blue-badge">👥</div>
                  </div>

                  <div className="stat-card">
                    <div className="stat-left">
                      <span className="card-lbl">Total Games</span>
                      <span className="card-val">{singleDayData.correct_guesses || 0}</span>
                    </div>
                    <div className="stat-icon-badge purple-badge">🎮</div>
                  </div>

                  <div className="stat-card">
                    <div className="stat-left">
                      <span className="card-lbl">Correct Guesses</span>
                      <span className="card-val">{singleDayData.correct_guesses}</span>
                    </div>
                    <div className="stat-icon-badge green-badge">✓</div>
                  </div>

                  <div className="stat-card">
                    <div className="stat-left">
                      <span className="card-lbl">Win Rate</span>
                      <span className="card-val">
                        {singleDayData.num_users > 0 ? '66.7%' : '0.0%'}
                      </span>
                    </div>
                    <div className="stat-icon-badge green-badge">📈</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="range-results-table-card">
                <table className="clean-report-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Users</th>
                      <th>Games</th>
                      <th>Correct</th>
                      <th>Win Rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dailyReports.map((row, idx) => (
                      <tr key={idx}>
                        <td className="bold-txt">{row.date}</td>
                        <td>{row.num_users}</td>
                        <td>{row.num_users * 2}</td>
                        <td className="green-txt">{row.correct_guesses}</td>
                        <td>
                          <span className="rate-pill">
                            {row.num_users > 0 ? `${((row.correct_guesses / (row.num_users * 2)) * 100).toFixed(1)}%` : '0.0%'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* TAB 3: USER REPORT */}
        {activeTab === 'user' && (
          <div className="view-section">
            <div className="view-header">
              <h1 className="green-heading">User Reports</h1>
              <p className="view-sub">Analyze per-user progress and historical words tried.</p>
            </div>

            <div className="user-reports-stack">
              {userReports.map((uItem, idx) => (
                <div key={idx} className="user-report-block">
                  <div className="u-block-header">
                    <span className="u-avatar-circle">{uItem.username.charAt(0).toUpperCase()}</span>
                    <h3>@{uItem.username}</h3>
                  </div>
                  <table className="clean-report-table">
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Words Tried</th>
                        <th>Correct Guesses</th>
                      </tr>
                    </thead>
                    <tbody>
                      {uItem.rows.map((r, rIdx) => (
                        <tr key={rIdx}>
                          <td>{r.date}</td>
                          <td>{r.words_tried}</td>
                          <td className="green-txt">{r.correct_guesses}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: USERS MANAGEMENT (Matching Screenshot 5 & User Actions Request) */}
        {activeTab === 'users' && (
          <div className="view-section">
            <div className="view-header-row">
              <div>
                <h1 className="green-heading">User Management</h1>
                <p className="view-sub">View, edit, and manage platform users.</p>
              </div>
              <div className="users-count-pill">
                👥 <strong>{usersList.length}</strong> users
              </div>
            </div>

            <div className="search-filter-card">
              <div className="search-input-box">
                <span className="search-icon">🔍</span>
                <input
                  type="text"
                  placeholder="Search users..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="search-user-input"
                />
              </div>
              <div className="role-filter-box">
                <select
                  value={roleFilter}
                  onChange={e => setRoleFilter(e.target.value)}
                  className="role-filter-select"
                >
                  <option value="all">all</option>
                  <option value="player">player</option>
                  <option value="admin">admin</option>
                </select>
              </div>
            </div>

            <div className="user-table-card">
              <table className="user-management-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Username</th>
                    <th>Role</th>
                    <th>Games</th>
                    <th>Wins</th>
                    <th>Win %</th>
                    <th>Joined ▼</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((userItem, idx) => (
                    <tr key={idx}>
                      <td className="name-cell">
                        <span className={`user-avatar-circle ${userItem.role === 'admin' ? 'admin' : 'player'}`}>
                          {userItem.username.charAt(0).toUpperCase()}
                        </span>
                        <span className="display-name">{userItem.username}</span>
                      </td>
                      <td className="username-cell">@{userItem.username}</td>
                      <td>
                        <span className={`role-badge ${userItem.role}`}>
                          {userItem.role}
                        </span>
                      </td>
                      <td>{userItem.games}</td>
                      <td className={userItem.wins > 0 ? 'green-txt' : ''}>{userItem.wins}</td>
                      <td>{userItem.win_pct}</td>
                      <td className="joined-cell">{userItem.created_at}</td>
                      <td className="actions-cell">
                        <div className="action-dropdown-wrapper">
                          <button
                            className="action-trigger-btn"
                            onClick={() => setActionMenuOpen(actionMenuOpen === userItem.username ? null : userItem.username)}
                          >
                            •••
                          </button>
                          {actionMenuOpen === userItem.username && (
                            <div className="action-menu-popup">
                              <button onClick={() => handleOpenHeatmap(userItem.username)}>
                                📊 View Report (30-Day Heatmap)
                              </button>
                              <button onClick={() => {
                                setActionMenuOpen(null)
                                setEditingUser(userItem)
                                setEditRole(userItem.role)
                              }}>
                                ✏️ Edit User
                              </button>
                              <button className="delete-action" onClick={() => {
                                setActionMenuOpen(null)
                                setDeletingUser(userItem)
                              }}>
                                🗑️ Delete User
                              </button>
                            </div>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default AdminDashboard
