import { useState, useEffect } from 'react'
import { logout as apiLogout, startGame as apiStartGame } from './api'
import Header from './components/Header/Header'
import AuthCard from './components/Auth/AuthCard'
import GameCard from './components/Game/GameCard'
import GamePage from './components/Game/GamePage'
import AdminReports from './components/Reports/AdminReports'
import './App.css'

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [view, setView] = useState('dashboard')
  const [sessionId, setSessionId] = useState(null)
  const [startError, setStartError] = useState('')
  const [startLoading, setStartLoading] = useState(false)
  const [theme, setTheme] = useState(() => localStorage.getItem('app-theme') || 'dark')

  useEffect(() => {
    localStorage.setItem('app-theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'))
  }

  const handleLogout = () => {
    apiLogout()
    setCurrentUser(null)
    setView('dashboard')
    setSessionId(null)
  }

  const handleStartGame = async () => {
    setStartError('')
    setStartLoading(true)
    try {
      const data = await apiStartGame()
      setSessionId(data.session_id)
      setView('game')
    } catch (err) {
      setStartError(err.error || 'Could not start new game')
    } finally {
      setStartLoading(false)
    }
  }

  const handleGameEnd = () => {
    setView('dashboard')
    setSessionId(null)
  }

  return (
    <div className={`app-shell theme-${theme}`}>
      {!currentUser ? (
        <>
          <Header currentUser={null} theme={theme} onToggleTheme={toggleTheme} />
          <AuthCard onAuthSuccess={(user) => setCurrentUser(user)} />
        </>
      ) : view === 'game' && sessionId ? (
        <GamePage
          sessionId={sessionId}
          onBack={handleGameEnd}
          currentUser={currentUser}
          theme={theme}
          onToggleTheme={toggleTheme}
        />
      ) : (
        <>
          <Header currentUser={currentUser} theme={theme} onToggleTheme={toggleTheme} />
          <div className={`dashboard-grid ${currentUser.role === 'admin' ? 'has-admin' : 'full-width'}`}>
            <GameCard
              currentUser={currentUser}
              onLogout={handleLogout}
              onStartGame={handleStartGame}
              loading={startLoading}
              error={startError}
            />
            {currentUser.role === 'admin' && <AdminReports />}
          </div>
        </>
      )}
    </div>
  )
}

export default App
