import './Header.css'

function Header({ currentUser }) {
  return (
    <header className="hero-card">
      <div>
        <p className="eyebrow">Guess the Word</p>
        <h1>Word Guessing Game</h1>
        <p className="subtitle">
          Register, log in, play up to 3 words per day, and review admin reports.
        </p>
      </div>
      {currentUser && (
        <div className="pill-box">
          <span className="pill">{currentUser.role} account</span>
          <span className="pill">Max 3 games / day</span>
        </div>
      )}
    </header>
  )
}

export default Header
