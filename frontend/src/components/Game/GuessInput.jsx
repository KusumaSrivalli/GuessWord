function GuessInput({ value, onChange, onSubmit, disabled, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit()
  }

  return (
    <form className="form-stack" onSubmit={handleSubmit}>
      <label>
        Enter 5-letter guess:
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value.toUpperCase())}
          maxLength={5}
          placeholder="ENTER"
          disabled={disabled}
          autoFocus
        />
      </label>
      <button
        type="submit"
        className="primary-btn"
        disabled={disabled || value.length !== 5}
      >
        {loading && <span className="loading-spinner" />}
        Submit Guess
      </button>
    </form>
  )
}

export default GuessInput
