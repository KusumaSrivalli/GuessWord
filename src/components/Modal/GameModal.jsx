import './GameModal.css'

function GameModal({ show, type, message, onClose }) {
  if (!show) return null

  return (
    <div className={`modal-overlay ${type === 'won' ? 'modal-won' : 'modal-lost'}`}>
      <div className="modal-card">
        <div className="modal-icon">{type === 'won' ? '🎉' : '💔'}</div>
        <h2>{type === 'won' ? 'You Won!' : 'Game Over'}</h2>
        <p>{message}</p>
        <button className="primary-btn" onClick={onClose}>OK</button>
      </div>
    </div>
  )
}

export default GameModal
