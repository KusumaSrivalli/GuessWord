import { useState, useEffect } from 'react'
import AuthCard from '../Auth/AuthCard'
import './LandingPage.css'

const DEMO_ROWS = [
  { guess: "CRANE", colors: ["grey", "grey", "green", "orange", "grey"] },
  { guess: "SLATE", colors: ["grey", "green", "green", "orange", "grey"] },
  { guess: "PLAIN", colors: ["green", "green", "green", "grey", "orange"] },
  { guess: "PLANT", colors: ["green", "green", "green", "green", "green"] },
  { guess: "", colors: ["empty", "empty", "empty", "empty", "empty"] }
]

function HeroWordleCard() {
  const [step, setStep] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setStep(prev => (prev >= 32 ? 0 : prev + 1))
    }, 220)

    return () => clearInterval(timer)
  }, [])

  // Calculate row typing & reveal state
  // Row 0: typing steps 0..4 (letters 1..5), reveal at step >= 5
  // Row 1: typing steps 6..10 (letters 1..5), reveal at step >= 11
  // Row 2: typing steps 12..16 (letters 1..5), reveal at step >= 17
  // Row 3: typing steps 18..22 (letters 1..5), reveal at step >= 23
  // Victory pause: steps 24..32

  const activeRowIndex = Math.min(4, Math.floor(step / 6))
  const typedInActiveRow = step % 6

  return (
    <div className="wordle-card-preview">
      <div className="wordle-card-badge">
        <span className="live-pulse-dot">●</span> Target Word: <strong>PLANT</strong>
      </div>
      <div className="wordle-grid-container">
        {DEMO_ROWS.map((rowObj, rIdx) => {
          const isRowRevealed = rIdx < activeRowIndex || (rIdx === activeRowIndex && typedInActiveRow >= 5)
          const isRowTyping = rIdx === activeRowIndex && typedInActiveRow < 5

          return (
            <div key={rIdx} className="wordle-row">
              {Array.from({ length: 5 }).map((_, cIdx) => {
                let letter = ''
                let styleClass = 'empty'

                if (isRowRevealed && rowObj.guess) {
                  letter = rowObj.guess[cIdx] || ''
                  styleClass = rowObj.colors[cIdx] || 'empty'
                } else if (isRowTyping && rowObj.guess) {
                  if (cIdx < typedInActiveRow) {
                    letter = rowObj.guess[cIdx] || ''
                    styleClass = 'typing-active'
                  }
                }

                const isJustRevealed = rIdx === activeRowIndex - 1 && typedInActiveRow === 0

                return (
                  <span
                    key={cIdx}
                    className={`w-tile ${styleClass} ${isJustRevealed ? 'tile-flip-reveal' : ''}`}
                    style={{ animationDelay: `${cIdx * 0.08}s` }}
                  >
                    {letter}
                  </span>
                )
              })}
            </div>
          )
        })}
      </div>
    </div>
  )
}

function LandingPage({ onAuthSuccess }) {
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [initialMode, setInitialMode] = useState('login')

  const openAuth = (mode) => {
    setInitialMode(mode)
    setShowAuthModal(true)
    const authElem = document.getElementById('auth-section')
    if (authElem) {
      authElem.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <div className="landing-container">
      {/* Navbar Header */}
      <header className="landing-navbar">
        <div className="landing-logo">
          <div className="logo-badge">abc</div>
          <span className="logo-text">GUESS <span className="logo-accent">THE WORD</span></span>
        </div>

        <div className="landing-nav-links">
          <a href="#features">Features</a>
          <a href="#how-to-play">How to Play</a>
          <a href="#auth-section">Login / Register</a>
        </div>

        <div className="landing-nav-actions">
          <button className="nav-btn-secondary" onClick={() => openAuth('login')}>Log In</button>
          <button className="nav-btn-primary" onClick={() => openAuth('register')}>Sign Up Free</button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <h1 className="hero-headline">
          Master the <span className="highlight-text">5-Letter Word</span> Challenge Daily.
        </h1>
        <p className="hero-subtext">
          Train your brain, expand your vocabulary, and track your consistency with our modern Wordle-style puzzle game. 3 games per day, unlimited fun.
        </p>
        <div className="hero-cta-group">
          <button className="hero-primary-btn" onClick={() => openAuth('login')}>
            🎮 Play Now — It's Free
          </button>
          <a href="#how-to-play" className="hero-secondary-btn">
            📖 See How to Play
          </a>
        </div>

        {/* Hero Interactive 5x5 Animated Card Preview */}
        <HeroWordleCard />
      </section>

      {/* Features Showcase */}
      <section id="features" className="features-section">
        <div className="section-header">
          <h2>Why Players Love Guess The Word</h2>
          <p>Everything you need for an engaging daily word puzzle experience.</p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎮</div>
            <h3>3 Games Daily Limit</h3>
            <p>Quality over quantity. Enjoy 3 carefully curated 5-letter word puzzles every 24 hours.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI & LLM Word Verification</h3>
            <p>Powered by live Gemini LLM & Dictionary APIs. Validates real English words while rejecting gibberish instantly.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔥</div>
            <h3>Consistency Heatmap</h3>
            <p>Track your 30-day activity grid, maintain your daily win streaks, and monitor your progress over time.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Detailed Admin Analytics</h3>
            <p>Comprehensive admin reports tracking active players, daily guess accuracy, and global statistics.</p>
          </div>
        </div>
      </section>

      {/* How to Play Section */}
      <section id="how-to-play" className="rules-section">
        <div className="section-header">
          <h2>How to Play</h2>
          <p>Simple rules, endless brain-teasing excitement!</p>
        </div>

        <div className="rules-cards">
          <div className="rule-card">
            <div className="rule-badge green">GREEN</div>
            <h4>Correct Position</h4>
            <p>The letter is in the target word and in the exact right spot.</p>
          </div>

          <div className="rule-card">
            <div className="rule-badge orange">ORANGE</div>
            <h4>Wrong Position</h4>
            <p>The letter is in the word, but currently in the wrong spot.</p>
          </div>

          <div className="rule-card">
            <div className="rule-badge grey">GREY</div>
            <h4>Not in Word</h4>
            <p>The letter does not appear anywhere in the target word.</p>
          </div>
        </div>
      </section>

      {/* Auth Section */}
      <section id="auth-section" className="auth-landing-section">
        <div className="section-header">
          <h2>Ready to Test Your Vocabulary?</h2>
          <p>Sign up or log in below to start playing your 3 daily games!</p>
        </div>
        <div className="embedded-auth-box">
          <AuthCard onAuthSuccess={onAuthSuccess} initialTab={initialMode} />
        </div>
      </section>
    </div>
  )
}

export default LandingPage
