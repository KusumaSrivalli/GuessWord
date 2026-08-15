import { useState, useEffect } from 'react'
import { getUserStats } from '../../api'
import './GameCard.css'

function GameCard({ currentUser, onStartGame, loading, error }) {
  const [stats, setStats] = useState({
    total_games: 0,
    total_wins: 0,
    win_rate: '0.0%',
    current_streak: 0,
    games_left_today: 3,
    heatmap: []
  })

  const [showModeModal, setShowModeModal] = useState(false)

  useEffect(() => {
    async function fetchStats() {
      try {
        const data = await getUserStats()
        setStats(data)
      } catch (err) {
        console.error('Failed to load user stats', err)
      }
    }
    fetchStats()
  }, [])

  const handleSelectMode = (mode) => {
    setShowModeModal(false)
    onStartGame(mode)
  }

  return (
    <div className="dashboard-container">
      {/* Mode Selection Modal */}
      {showModeModal && (
        <div className="mode-modal-overlay" onClick={() => setShowModeModal(false)}>
          <div className="mode-modal-card" onClick={e => e.stopPropagation()}>
            <div className="mode-modal-header">
              <h2>Select Difficulty Mode</h2>
              <button className="close-modal-btn" onClick={() => setShowModeModal(false)}>✕</button>
            </div>
            <p className="mode-modal-subtitle">Choose your challenge level for this session:</p>

            <div className="mode-options-grid">
              <div className="mode-card easy" onClick={() => handleSelectMode('easy')}>
                <div className="mode-icon">🟢</div>
                <h3>EASY</h3>
                <div className="mode-detail">⏱️ No Time Limit</div>
                <div className="mode-detail">📖 Easy Vocab</div>
                <div className="mode-detail hint-off">🚫 No Hint</div>
                <button className="select-mode-btn easy">Play Easy</button>
              </div>

              <div className="mode-card medium" onClick={() => handleSelectMode('medium')}>
                <div className="mode-icon">🟡</div>
                <h3>MEDIUM</h3>
                <div className="mode-detail">⏱️ 5 Minutes Limit</div>
                <div className="mode-detail">📖 Medium Vocab</div>
                <div className="mode-detail hint-off">🚫 No Hint</div>
                <button className="select-mode-btn medium">Play Medium</button>
              </div>

              <div className="mode-card hard" onClick={() => handleSelectMode('hard')}>
                <div className="mode-icon">🔴</div>
                <h3>HARD</h3>
                <div className="mode-detail">⏱️ 3 Minutes Limit</div>
                <div className="mode-detail">📖 Hard Vocab</div>
                <div className="mode-detail hint-on">💡 Hint Option Available</div>
                <button className="select-mode-btn hard">Play Hard</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 1. Welcome Hero Banner Card */}
      <div className="hero-banner-card">
        <div className="hero-banner-left">
          <h1 className="welcome-title">Welcome back, {currentUser.username}!</h1>
          <p className="user-handle">@{currentUser.username}</p>
        </div>
        <div className="hero-banner-right">
          <button
            className="start-game-cta"
            onClick={() => setShowModeModal(true)}
            disabled={loading}
          >
            {loading ? <span className="loading-spinner" /> : <span className="cta-icon">🎮</span>}
            Start New Game
          </button>
          <div className="games-left-pill">
            <span className="dots-icon">•••</span> {stats.games_left_today} of 3 games left today
          </div>
        </div>
      </div>

      {error && <div className="status-message error">{error}</div>}

      {/* 2. 4 Metric Stat Cards Row */}
      <div className="stats-metric-grid">
        <div className="metric-card">
          <div className="metric-info">
            <span className="metric-value">{stats.total_games}</span>
            <span className="metric-label">Total Games</span>
          </div>
          <div className="metric-icon controller-icon">🎮</div>
        </div>

        <div className="metric-card">
          <div className="metric-info">
            <span className="metric-value">{stats.total_wins}</span>
            <span className="metric-label">Total Wins</span>
          </div>
          <div className="metric-icon trophy-icon">🏆</div>
        </div>

        <div className="metric-card">
          <div className="metric-info">
            <span className="metric-value">{stats.win_rate}</span>
            <span className="metric-label">Win Rate</span>
          </div>
          <div className="metric-icon trend-icon">📈</div>
        </div>

        <div className="metric-card">
          <div className="metric-info">
            <span className="metric-value">{stats.current_streak}</span>
            <span className="metric-label">Current Streak</span>
          </div>
          <div className="metric-icon flame-icon">🔥</div>
        </div>
      </div>

      {/* 3. Gameplay Consistency Heatmap Card */}
      <div className="heatmap-card">
        <div className="heatmap-header">
          <div>
            <h2 className="heatmap-title">
              🔥 {currentUser.username}'s Gameplay Consistency Heatmap
            </h2>
            <p className="heatmap-subtitle">
              Track your daily play activity, consistency level & streaks
            </p>
          </div>
          <div className="streak-badge">
            🔥 {stats.current_streak} Day Streak
          </div>
        </div>

        <div className="heatmap-grid-3rows">
          {stats.heatmap && stats.heatmap.length > 0 ? (
            stats.heatmap.map((item, index) => {
              const count = item.count || 0
              const levelClass = count === 0 ? 'level-0' : count === 1 ? 'level-1' : count === 2 ? 'level-2' : 'level-3'
              return (
                <div
                  key={index}
                  className={`heatmap-box ${levelClass}`}
                >
                  <span className="box-date">{item.label}</span>
                  <span className="box-count">{count}</span>
                </div>
              )
            })
          ) : (
            <p className="empty-heatmap">Play games to build your streak!</p>
          )}
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
    </div>
  )
}

export default GameCard
