function GuessRow({ guess, feedback }) {
  return (
    <div className="guess-row">
      {feedback.map((color, i) => (
        <span key={i} className={`letter-box ${color}`}>
          {guess[i]}
        </span>
      ))}
    </div>
  )
}

export default GuessRow
