import { useState, useEffect, useCallback } from 'react'
import { submitGuess as apiSubmitGuess } from '../../api'
import GameGrid from './GameGrid'
import Keyboard from './Keyboard'
import GameModal from '../Modal/GameModal'
import './GamePage.css'

function GamePage({ sessionId, onBack, currentUser }) {
  const [guesses, setGuesses] = useState([])
  const [currentGuess, setCurrentGuess] = useState('')
  const [status, setStatus] = useState('playing')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [modalMessage, setModalMessage] = useState('')
  const [modalType, setModalType] = useState('won')

  const usedLetters = {}
  guesses.forEach(g => {
    g.feedback.forEach((color, i) => {
      const letter = g.guess[i]
      const prev = usedLetters[letter]
      if (color === 'green') usedLetters[letter] = 'green'
      else if (color === 'orange' && prev !== 'green') usedLetters[letter] = 'orange'
      else if (!prev) usedLetters[letter] = 'grey'
    })
  })

  const handleSubmit = useCallback(async () => {
    if (status !== 'playing' || currentGuess.length !== 5 || loading) return

    setMessage('')
    setLoading(true)
    try {
      const data = await apiSubmitGuess(sessionId, currentGuess)
      setGuesses(data.guesses)
      setCurrentGuess('')

      if (data.status === 'won') {
        setStatus('won')
        setModalType('won')
        setModalMessage('Congratulations! You guessed the word correctly!')
        setShowModal(true)
      } else if (data.status === 'lost') {
        setStatus('lost')
        setModalType('lost')
        setModalMessage(`Better luck next time! The word was ${data.target_word}.`)
        setShowModal(true)
      }
    } catch (err) {
      setMessage(err.error || 'Failed to submit guess')
    } finally {
      setLoading(false)
    }
  }, [sessionId, currentGuess, status, loading])

  const handleKey = useCallback((key) => {
    if (status !== 'playing') return
    if (currentGuess.length < 5) {
      setCurrentGuess(prev => prev + key)
    }
  }, [currentGuess, status])

  const handleBackspace = useCallback(() => {
    setCurrentGuess(prev => prev.slice(0, -1))
  }, [])

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return
      if (e.key === 'Enter') {
        handleSubmit()
      } else if (e.key === 'Backspace') {
        handleBackspace()
      } else if (/^[a-zA-Z]$/.test(e.key)) {
        handleKey(e.key.toUpperCase())
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handleKey, handleBackspace, handleSubmit])

  const closeModal = () => {
    setShowModal(false)
    onBack()
  }

  return (
    <div className="game-page">
      <GameModal show={showModal} type={modalType} message={modalMessage} onClose={closeModal} />

      <header className="game-page-header">
        <button className="back-btn" onClick={onBack}>← Back</button>
        <h1>Guess the Word</h1>
        <span className="pill game-pill">{currentUser.username}</span>
      </header>

      {message && <div className="game-message">{message}</div>}

      <GameGrid guesses={guesses} currentGuess={currentGuess} maxGuesses={5} />

      <Keyboard
        onKey={handleKey}
        onEnter={handleSubmit}
        onBackspace={handleBackspace}
        usedLetters={usedLetters}
        disabled={status !== 'playing' || loading}
      />
    </div>
  )
}

export default GamePage
