import './Keyboard.css'

const ROWS = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '\u232B']
]

function Keyboard({ onKey, onEnter, onBackspace, usedLetters, disabled }) {
  const handleClick = (key) => {
    if (disabled) return
    if (key === 'ENTER') onEnter()
    else if (key === '\u232B') onBackspace()
    else onKey(key)
  }

  return (
    <div className="keyboard">
      {ROWS.map((row, i) => (
        <div key={i} className="keyboard-row">
          {row.map((key) => {
            const isSpecial = key === 'ENTER' || key === '\u232B'
            const color = usedLetters[key] || ''
            return (
              <button
                key={key}
                className={`key ${isSpecial ? 'key-wide' : ''} ${color ? `key-${color}` : ''}`}
                onClick={() => handleClick(key)}
                disabled={disabled}
                aria-label={key === '\u232B' ? 'Backspace' : key}
              >
                {key}
              </button>
            )
          })}
        </div>
      ))}
    </div>
  )
}

export default Keyboard
