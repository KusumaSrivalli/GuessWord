function UserReport({ data }) {
  if (!data || data.length === 0) {
    return <p className="helper-text">No user data available.</p>
  }

  return (
    <div className="report-block">
      {data.map((user, i) => (
        <div key={i} className="user-report">
          <h4>{user.username}</h4>
          {user.rows && user.rows.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Words Tried</th>
                  <th>Correct Guesses</th>
                </tr>
              </thead>
              <tbody>
                {user.rows.map((row, j) => (
                  <tr key={j}>
                    <td>{row.date}</td>
                    <td>{row.words_tried}</td>
                    <td>{row.correct_guesses}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="helper-text">No games played yet.</p>
          )}
        </div>
      ))}
    </div>
  )
}

export default UserReport
