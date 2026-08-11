import { useState, useEffect } from 'react'
import { getDailyReport, getUserReport } from '../../api'
import DailyReport from './DailyReport'
import UserReport from './UserReport'
import './AdminReports.css'

function AdminReports() {
  const [dailyData, setDailyData] = useState([])
  const [userData, setUserData] = useState([])
  const [activeTab, setActiveTab] = useState('daily')
  const [loading, setLoading] = useState(false)

  const fetchReports = async () => {
    setLoading(true)
    try {
      const [daily, user] = await Promise.all([getDailyReport(), getUserReport()])
      setDailyData(daily.report || [])
      setUserData(user.report || [])
    } catch (err) {
      console.error('Failed to fetch reports:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchReports()
  }, [])

  return (
    <section className="card report-card">
      <div className="report-header">
        <h2>Admin Reports</h2>
        <button className="refresh-btn" onClick={fetchReports} disabled={loading}>
          {loading && <span className="loading-spinner" />}
          Refresh
        </button>
      </div>

      <div className="report-tabs">
        <button
          className={`tab-btn ${activeTab === 'daily' ? 'active' : ''}`}
          onClick={() => setActiveTab('daily')}
        >
          Daily Summary
        </button>
        <button
          className={`tab-btn ${activeTab === 'user' ? 'active' : ''}`}
          onClick={() => setActiveTab('user')}
        >
          User Progress
        </button>
      </div>

      {activeTab === 'daily' && <DailyReport data={dailyData} />}
      {activeTab === 'user' && <UserReport data={userData} />}
    </section>
  )
}

export default AdminReports
