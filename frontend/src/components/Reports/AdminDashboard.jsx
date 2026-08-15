import { useState, useEffect } from 'react'
import { getAdminOverview, getUserStats } from '../../api'
import './AdminDashboard.css'

function AdminDashboard({ currentUser }) {
  const [overview, setOverview] = useState({
    total_users: 0,
    total_games: 0,
    total_wins: 0,
    user_names: [],
    daily_report: []
  })

  // Date selection state (defaults to today's date YYYY-MM-DD)
  const [selectedDate, setSelectedDate] = useState(() => {
    const d = new Date()
    const yyyy = d.getFullYear()
    const mm = String(d.getMonth() + 1).padStart(2, '0')
    const dd = String(d.getDate()).padStart(2, '0')
    return `${yyyy}-${mm}-${dd}`
  })

  const [heatmapUser, setHeatmapUser] = useState(null)
  const [heatmapStats, setHeatmapStats] = useState(null)
  const [loading, setLoading] = useState(false)

  // Generate last 5 days list for the filter bar
  const getLast5Days = () => {
    const dates = []
    const today = new Date()
    for (let i = 0; i < 5; i++) {
      const d = new Date(today)
      d.setDate(d.getDate() - i)
      const yyyy = d.getFullYear()
      const mm = String(d.getMonth() + 1).padStart(2, '0')
      const dd = String(d.getDate()).padStart(2, '0')
      const dateStr = `${yyyy}-${mm}-${dd}`
      const monthDay = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
      const label = i === 0 ? `Today (${monthDay})` : monthDay
      dates.push({ dateStr, label })
    }
    return dates
  }

  const last5Days = getLast5Days()

  const fetchOverview = async () => {
    setLoading(true)
    try {
      const data = await getAdminOverview()
      setOverview(data)
    } catch (err) {
      console.error('Failed to load admin overview', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchOverview()
  }, [])

  // Fetch heatmap when a user is selected via "View Heatmap" button
  const handleOpenHeatmap = async (username) => {
    setHeatmapUser(username)
    setHeatmapStats(null)
    try {
      const stats = await getUserStats(username)
      setHeatmapStats(stats)
    } catch (err) {
      console.error('Failed to fetch user heatmap stats', err)
    }
  }

  // Get report data for the currently selected date
  const currentDayData = overview.daily_report.find(d => d.date === selectedDate) || {
    date: selectedDate,
    users_activity: []
  }

  const activeUsersCount = currentDayData.users_activity.length
  const totalGamesPlayedToday = currentDayData.users_activity.reduce((acc, u) => acc + u.games_played, 0)
  const totalGamesWonToday = currentDayData.users_activity.reduce((acc, u) => acc + u.games_won, 0)

  return (
    <div className="admin-dashboard-container">
      {/* 30-Day Heatmap Modal */}
      {heatmapUser && (
        <div className="heatmap-modal-overlay" onClick={() => setHeatmapUser(null)}>
          <div className="heatmap-modal-card" onClick={e => e.stopPropagation()}>
            <div className="heatmap-modal-header">
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

      {/* Header Banner */}
      <div className="admin-banner-card">
        <div>
          <h1 className="admin-title">👑 Admin Daily Summary Dashboard</h1>
          <p className="admin-subtitle">
            View daily active players, games played, games won, and inspect individual 30-day heatmaps.
          </p>
        </div>
        <button className="refresh-admin-btn" onClick={fetchOverview} disabled={loading}>
          {loading ? <span className="loading-spinner" /> : '🔄 Refresh Data'}
        </button>
      </div>

      {/* 5-Day Date Selector Filter Bar */}
      <div className="date-filter-bar">
        <span className="filter-label">📅 Select Date (Last 5 Days):</span>
        <div className="date-pills-group">
          {last5Days.map((day, idx) => (
            <button
              key={idx}
              className={`date-pill-btn ${selectedDate === day.dateStr ? 'active' : ''}`}
              onClick={() => setSelectedDate(day.dateStr)}
            >
              {day.label}
            </button>
          ))}
        </div>
      </div>

      {/* Top 3 Summary Metrics Cards for Selected Date */}
      <div className="admin-metrics-grid">
        <div className="admin-metric-card">
          <div className="metric-info">
            <span className="metric-value">{activeUsersCount}</span>
            <span className="metric-label">Active Players ({selectedDate})</span>
          </div>
          <div className="admin-metric-icon">👥</div>
        </div>

        <div className="admin-metric-card">
          <div className="metric-info">
            <span className="metric-value">{totalGamesPlayedToday}</span>
            <span className="metric-label">Games Played</span>
          </div>
          <div className="admin-metric-icon">🎮</div>
        </div>

        <div className="admin-metric-card">
          <div className="metric-info">
            <span className="metric-value">{totalGamesWonToday}</span>
            <span className="metric-label">Total Games Won</span>
          </div>
          <div className="admin-metric-icon">🏆</div>
        </div>
      </div>

      {/* Daily Player Performance Table */}
      <div className="admin-table-card">
        <div className="table-header">
          <h2>📊 Player Activity & Victories for {selectedDate}</h2>
          <p>Usernames, games played, games won, and 30-day consistency heatmap inspector.</p>
        </div>

        {currentDayData.users_activity && currentDayData.users_activity.length > 0 ? (
          <div className="table-wrapper">
            <table className="admin-data-table">
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Games Played</th>
                  <th>Games Won</th>
                  <th>30-Day Heatmap</th>
                </tr>
              </thead>
              <tbody>
                {currentDayData.users_activity.map((uAct, index) => (
                  <tr key={index}>
                    <td className="user-cell">
                      <span className="player-avatar">{uAct.username.charAt(0).toUpperCase()}</span>
                      <span className="user-name-text">@{uAct.username}</span>
                    </td>
                    <td>
                      <span className="count-badge played">🎮 {uAct.games_played} played</span>
                    </td>
                    <td>
                      <span className={`count-badge ${uAct.games_won > 0 ? 'won' : 'zero'}`}>
                        🏆 {uAct.games_won} won
                      </span>
                    </td>
                    <td>
                      <button
                        className="view-heatmap-btn"
                        onClick={() => handleOpenHeatmap(uAct.username)}
                      >
                        🔥 View 30-Day Heatmap
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-day-state">
            <p>No player activity recorded on <strong>{selectedDate}</strong>.</p>
            <p className="sub-empty">Select another date from the top filter bar (Last 5 Days) to view activity.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminDashboard
