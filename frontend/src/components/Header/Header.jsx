import './Header.css'

function Header({ currentUser, theme, onToggleTheme }) {
  return (
    <header className="hero-card">
      <div>
        <p className="eyebrow">Guess the Word</p>
        <h1>Word Guessing Game</h1>
        <p className="subtitle">
          Register, log in, play up to 3 words per day, and review admin reports.
        </p>
      </div>
      <div className="header-right">
        {currentUser && (
          <div className="pill-box">
            <span className="pill">{currentUser.role} account</span>
            <span className="pill">Max 3 games / day</span>
          </div>
        )}
        <button
          className="theme-toggle-btn"
          onClick={onToggleTheme}
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
        </button>
      </div>
    </header>
  )
}

export default Header
