# Guess the Word

A full-stack word guessing game built with React (Vite) and Flask (MongoDB).

## Project Structure

```
├── backend/          # Flask REST API + MongoDB
│   ├── app.py        # API endpoints
│   ├── models.py     # Database operations
│   ├── seed.py       # Seed 20 words + default users
│   └── .env          # MongoDB URI + JWT secret
│
├── frontend/         # React (Vite) UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/       # Login & Register
│   │   │   ├── Game/       # Game board, guess input, letter rows
│   │   │   ├── Modal/      # Win/loss modals
│   │   │   ├── Reports/    # Admin daily & user reports
│   │   │   └── Header/     # App header
│   │   ├── App.jsx         # Root component
│   │   └── api.js          # API utility
│   ├── api/                # Vercel serverless functions
│   └── vercel.json         # Vercel deployment config
│
├── .gitignore
└── README.md
```

## Features

- **User Registration** — Username (5+ letters, mixed case) + password validation
- **Wordle-style Gameplay** — 5 guesses, green/orange/grey feedback
- **3 Games Per Day** limit per user
- **Admin Reports** — Daily summary & per-user stats
- **MongoDB** storage for users, words, and game sessions

## Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB (local or Atlas)

### Backend
```bash
cd backend
pip install -r requirements.txt
python seed.py        # Seeds 20 words + default users
python app.py         # Starts Flask on port 5000
```

### Frontend
```bash
cd frontend
npm install
npm run dev           # Starts Vite on port 5173
```

### Default Logins
| Username | Password | Role   |
|----------|----------|--------|
| Admin1   | Admin1$  | Admin  |
| Player1  | Player1$ | Player |

## Deployment (Vercel)
1. Push to GitHub
2. Import repo on Vercel, set **Root Directory** to `frontend`
3. Add environment variables: `MONGO_URI`, `JWT_SECRET_KEY`
4. Deploy
