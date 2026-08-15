import { useState, useEffect } from 'react'
import { logout as apiLogout, startGame as apiStartGame } from './api'
import Header from './components/Header/Header'
import AuthCard from './components/Auth/AuthCard'
import GameCard from './components/Game/GameCard'
import GamePage from './components/Game/GamePage'
import AdminDashboard from './components/Reports/AdminDashboard'
import LandingPage from './components/Landing/LandingPage'
import './App.css'

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [view, setView] = useState('dashboard')
  const [sessionId, setSessionId] = useState(null)
  const [startError, setStartError] = useState('')
  const [startLoading, setStartLoading] = useState(false)

  const [activeGameInfo, setActiveGameInfo] = useState({ mode: 'easy', timeLimit: null })
  const [statsKey, setStatsKey] = useState(0)

  const handleLogout = () => {
    apiLogout()
    setCurrentUser(null)
    setView('dashboard')
    setSessionId(null)
  }

  const handleStartGame = async (selectedMode = 'easy') => {
    setStartError('')
    setStartLoading(true)
    try {
      const data = await apiStartGame(selectedMode)
      setSessionId(data.session_id)
      setActiveGameInfo({
        mode: data.mode || selectedMode,
        timeLimit: data.time_limit,
        hint: data.hint
      })
      setView('game')
      setStatsKey(prev => prev + 1)
    } catch (err) {
      setStartError(err.error || 'Could not start new game')
    } finally {
      setStartLoading(false)
    }
  }

  const handleGameEnd = () => {
    setView('dashboard')
    setSessionId(null)
    setStatsKey(prev => prev + 1)
  }

  return (
    <div className="app-shell theme-dark">
      {!currentUser ? (
        <LandingPage onAuthSuccess={(user) => setCurrentUser(user)} />
      ) : view === 'game' && sessionId && currentUser.role !== 'admin' ? (
        <GamePage
          sessionId={sessionId}
          gameInfo={activeGameInfo}
          onBack={handleGameEnd}
          currentUser={currentUser}
        />
      ) : (
        <>
          <Header currentUser={currentUser} onLogout={handleLogout} />
          {currentUser.role === 'admin' ? (
            <AdminDashboard currentUser={currentUser} />
          ) : (
            <div className="dashboard-grid full-width">
              <GameCard
                key={statsKey}
                currentUser={currentUser}
                onLogout={handleLogout}
                onStartGame={handleStartGame}
                loading={startLoading}
                error={startError}
              />
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default App
