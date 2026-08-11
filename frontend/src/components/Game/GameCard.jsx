import './GameCard.css'

function GameCard({ currentUser, onLogout, onStartGame, loading, error }) {
  return (
    <section className="card game-card">
      <div className="section-heading">
        <h2>Play Game</h2>
        <p>Guess the 5-letter word in 5 tries or fewer!</p>
      </div>

      <div className="meta-row">
        <span className="pill">User: {currentUser.username}</span>
        <span className="pill">Role: {currentUser.role}</span>
      </div>

      <div className="button-row">
        <button
          className="primary-btn"
          onClick={onStartGame}
          disabled={loading}
        >
          {loading && <span className="loading-spinner" />}
          Start New Game
        </button>
        <button className="secondary-btn" onClick={onLogout}>
          Log out
        </button>
      </div>

      {error && <div className="status-message">{error}</div>}

      <div className="game-rules">
        <h3>How to Play</h3>
        <ul>
          <li>You have <strong>5 guesses</strong> to find the word</li>
          <li><span className="rule-color green"></span> Green = correct letter, correct position</li>
          <li><span className="rule-color orange"></span> Orange = correct letter, wrong position</li>
          <li><span className="rule-color grey"></span> Grey = letter not in the word</li>
          <li>Maximum <strong>3 games per day</strong></li>
        </ul>
      </div>
    </section>
  )
}

export default GameCard
