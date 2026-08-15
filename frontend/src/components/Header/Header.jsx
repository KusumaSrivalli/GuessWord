import './Header.css'

function Header({ currentUser, onLogout }) {
  const getInitial = (name) => {
    return name ? name.charAt(0).toUpperCase() : 'U'
  }

  return (
    <header className="navbar-container">
      <div className="navbar-left">
        <div className="logo-badge">abc</div>
        <span className="brand-name">
          GUESS <span className="brand-accent">THE WORD</span>
        </span>
      </div>

      {currentUser && (
        <div className="navbar-center">
          <button className="nav-tab active">
            <span className="tab-icon">🎮</span> Play Game
          </button>
        </div>
      )}

      <div className="navbar-right">
        {currentUser ? (
          <>
            <div className="user-profile-badge">
              <div className="user-avatar">{getInitial(currentUser.username)}</div>
              <span className="user-name">{currentUser.username}</span>
              <span className={`role-pill role-${currentUser.role}`}>
                {currentUser.role.toUpperCase()}
              </span>
            </div>

            <button className="logout-btn" onClick={onLogout} title="Log out">
              Logout
            </button>
          </>
        ) : null}
      </div>
    </header>
  )
}

export default Header
