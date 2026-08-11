function GameGrid({ guesses, currentGuess, maxGuesses }) {
  const rows = []

  for (let i = 0; i < guesses.length; i++) {
    const g = guesses[i]
    rows.push(
      <div key={`guess-${i}`} className="grid-row">
        {g.feedback.map((color, j) => (
          <div
            key={j}
            className={`tile tile-filled tile-${color}`}
            style={{ animationDelay: `${j * 0.15}s` }}
          >
            {g.guess[j]}
          </div>
        ))}
      </div>
    )
  }

  if (guesses.length < maxGuesses) {
    const currentLetters = currentGuess.split('')
    rows.push(
      <div key="current" className="grid-row">
        {Array.from({ length: 5 }, (_, j) => (
          <div
            key={j}
            className={`tile ${currentLetters[j] ? 'tile-active' : 'tile-empty'}`}
          >
            {currentLetters[j] || ''}
          </div>
        ))}
      </div>
    )

    for (let i = guesses.length + 1; i < maxGuesses; i++) {
      rows.push(
        <div key={`empty-${i}`} className="grid-row">
          {Array.from({ length: 5 }, (_, j) => (
            <div key={j} className="tile tile-empty" />
          ))}
        </div>
      )
    }
  }

  return <div className="game-grid">{rows}</div>
}

export default GameGrid
