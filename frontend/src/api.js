const API_BASE = '/api'

function getToken() { return localStorage.getItem('guessword-token') }
function setToken(token) { localStorage.setItem('guessword-token', token) }
function clearToken() { localStorage.removeItem('guessword-token') }

async function apiFetch(path, options = {}) {
  const token = getToken()
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  const data = await res.json()
  if (!res.ok) throw { status: res.status, ...data }
  return data
}

export async function register(username, password, role) {
  return apiFetch('/auth/register', { method: 'POST', body: JSON.stringify({ username, password, role }) })
}

export async function login(username, password) {
  const data = await apiFetch('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) })
  setToken(data.token)
  return data
}

export function logout() { clearToken() }

export async function startGame(mode = 'easy') {
  return apiFetch('/game/start', { method: 'POST', body: JSON.stringify({ mode }) })
}

export async function submitGuess(sessionId, guess) {
  return apiFetch('/game/guess', { method: 'POST', body: JSON.stringify({ session_id: sessionId, guess }) })
}

export async function getDailyReport() {
  return apiFetch('/reports/daily')
}

export async function getUserReport() {
  return apiFetch('/reports/user')
}

export async function getUserStats(targetUser) {
  const query = targetUser ? `?target_user=${encodeURIComponent(targetUser)}` : ''
  return apiFetch(`/game/user-stats${query}`)
}

export async function getAdminOverview() {
  return apiFetch('/admin/overview')
}

export { getToken, clearToken }
