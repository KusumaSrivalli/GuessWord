import { useState } from 'react'
import { logout as apiLogout } from './api'
import Header from './components/Header/Header'
import AuthCard from './components/Auth/AuthCard'
import GameCard from './components/Game/GameCard'
import AdminReports from './components/Reports/AdminReports'
import './App.css'

function App() {
  const [currentUser, setCurrentUser] = useState(null)

  const handleLogout = () => {
    apiLogout()
    setCurrentUser(null)
  }

  return (
    <div className="app-shell">
      <Header currentUser={currentUser} />

      {!currentUser ? (
        <AuthCard onAuthSuccess={(user) => setCurrentUser(user)} />
      ) : (
        <div className="dashboard-grid">
          <GameCard currentUser={currentUser} onLogout={handleLogout} />
          {currentUser.role === 'admin' && <AdminReports />}
        </div>
      )}
    </div>
  )
}

export default App
