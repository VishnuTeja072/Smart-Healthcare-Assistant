# 🩺 SmartHealth – AI Healthcare Assistant

SmartHealth is a full-stack AI-powered healthcare assistant that provides **preliminary physical and mental health assessments**, along with **nearby hospital recommendations** using real-time location data.

⚠️ This project is intended for **educational and assistive purposes only** and does not replace professional medical advice.

---

## 🚀 Features

- 🤖 AI-driven health assessment using **Gemini AI**
- 🧠 Mental wellness analysis
- 🩺 Physical symptom triage
- 📍 Nearby hospitals & clinics using **OpenStreetMap**
- 🗺 Interactive maps with **Leaflet**
- 🔐 Secure authentication (JWT-based)
- ⚡ Fast & responsive UI (React + Tailwind)
- 🌐 Deployment-ready architecture

---

## 🛠 Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS
- Axios
- Leaflet + OpenStreetMap

### Backend
- FastAPI
- Gemini AI (Google Generative AI)
- Python
- JWT Authentication

---

### Project Structure
AI-Health-Assistant/
│
├── AI/ # Frontend (React + Vite)
│ ├── public/
│ │ └── logo.png
│ ├── src/
│ │ ├── components/
│ │ ├── App.jsx
│ │ └── main.jsx
│ ├── index.html
│ └── package.json
│
├── backend/ # Backend (FastAPI)
│ ├── app.py
│ ├── ai_service.py
│ ├── maps_service.py
│ ├── requirements.txt
│ └── .env.example
│
├── .gitignore
└── README.md

---

## ⚙️ Environment Variables

### Frontend(`AI/.env`)
VITE_BACKEND_URL=http://localhost:8000

### Backend (`backend/.env`)
env:
GEMINI_API_KEY=your_api_key_here

---

### ▶️ Running the Project Locally
## 1️⃣ Backend Setup

cd backend
pip install -r requirements.txt
uvicorn app:app --reload

## Backend runs at:
http://localhost:8000

## 2️⃣ Frontend Setup
cd AI
npm install
npm run dev

## Frontend runs at:
http://localhost:5173

## 📂 Project Structure

