function DailyReport({ data }) {
  if (!data || data.length === 0) {
    return <p className="helper-text">No daily data available.</p>
  }

  return (
    <div className="report-block">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Number of Users</th>
            <th>Correct Guesses</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              <td>{row.date}</td>
              <td>{row.num_users}</td>
              <td>{row.correct_guesses}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default DailyReport
