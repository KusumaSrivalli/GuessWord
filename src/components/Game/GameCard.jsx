import { useState } from 'react'
import { startGame as apiStartGame, submitGuess as apiSubmitGuess } from '../../api'
import GameModal from '../Modal/GameModal'
import GuessInput from './GuessInput'
import GuessRow from './GuessRow'
import './GameCard.css'

function GameCard({ currentUser, onLogout }) {
  const [gameState, setGameState] = useState(null)
  const [guessInput, setGuessInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [modalMessage, setModalMessage] = useState('')
  const [modalType, setModalType] = useState('won')

  const startNewGame = async () => {
    setMessage('')
    setLoading(true)
    try {
      const data = await apiStartGame()
      setGameState({
        sessionId: data.session_id,
        guesses: [],
        status: 'playing',
        targetWord: null
      })
    } catch (err) {
      setMessage(err.error || 'Could not start new game')
    } finally {
      setLoading(false)
    }
  }

  const handleGuessSubmit = async () => {
    if (!gameState || gameState.status !== 'playing') return
    if (guessInput.length !== 5) {
      setMessage('Guess must be exactly 5 letters')
      return
    }

    setMessage('')
    setLoading(true)
    try {
      const data = await apiSubmitGuess(gameState.sessionId, guessInput)
      setGameState({
        sessionId: gameState.sessionId,
        guesses: data.guesses,
        status: data.status,
        targetWord: data.target_word || null
      })
      setGuessInput('')

      if (data.status === 'won') {
        setModalType('won')
        setModalMessage('Congratulations! You guessed the word correctly!')
        setShowModal(true)
      } else if (data.status === 'lost') {
        setModalType('lost')
        setModalMessage(`Better luck next time! The word was ${data.target_word}.`)
        setShowModal(true)
      }
    } catch (err) {
      setMessage(err.error || 'Failed to submit guess')
    } finally {
      setLoading(false)
    }
  }

  const closeModal = () => {
    setShowModal(false)
    setGameState(null)
  }

  return (
    <>
      <GameModal
        show={showModal}
        type={modalType}
        message={modalMessage}
        onClose={closeModal}
      />

      <section className="card game-card">
        <div className="section-heading">
          <h2>Play Game</h2>
          <p>Submit a 5-letter word and watch the feedback colors.</p>
        </div>

        <div className="meta-row">
          <span className="pill">User: {currentUser.username}</span>
          <span className="pill">Role: {currentUser.role}</span>
        </div>

        <div className="button-row">
          <button
            className="primary-btn"
            onClick={startNewGame}
            disabled={loading || (gameState && gameState.status === 'playing')}
          >
            {loading && !gameState && <span className="loading-spinner" />}
            Start New Game
          </button>
          <button className="secondary-btn" onClick={onLogout}>
            Log out
          </button>
        </div>

        {message && <div className="status-message">{message}</div>}

        {gameState && (
          <div className="game-area">
            <GuessInput
              value={guessInput}
              onChange={setGuessInput}
              onSubmit={handleGuessSubmit}
              disabled={loading || gameState.status !== 'playing'}
              loading={loading && gameState.status === 'playing'}
            />

            {gameState.guesses.length > 0 && (
              <div className="guess-history">
                <h3>Guess History</h3>
                {gameState.guesses.map((g, i) => (
                  <GuessRow key={i} guess={g.guess} feedback={g.feedback} />
                ))}
              </div>
            )}
          </div>
        )}
      </section>
    </>
  )
}

export default GameCard
