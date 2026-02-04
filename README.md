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

---

### OUTPUTS
<img width="488" height="593" alt="Screenshot 2026-02-04 124921" src="https://github.com/user-attachments/assets/89e2cb10-6f6f-4413-ad61-287c76ba32ad" />

<img width="476" height="629" alt="Screenshot 2026-02-04 124931" src="https://github.com/user-attachments/assets/4c02d9fd-e5fc-4d91-bcdd-626d9badddac" />

<img width="1791" height="929" alt="Screenshot 2026-02-03 233036" src="https://github.com/user-attachments/assets/c3bf3d0a-7888-4563-8b4b-130c472d6a77" />

<img width="1919" height="868" alt="Screenshot 2026-02-03 233045" src="https://github.com/user-attachments/assets/7ae25d70-bbb7-408d-ab41-860dd70027ff" />

<img width="1897" height="801" alt="Screenshot 2026-02-03 233203" src="https://github.com/user-attachments/assets/d6c26ea3-1b15-4fc6-beea-949e77169c1f" />

<img width="1901" height="868" alt="Screenshot 2026-02-03 233337" src="https://github.com/user-attachments/assets/3097958b-d194-4841-9e20-7315ab2da3c9" />

---

### Live Link:

https://smart-healthcare-assistant-two.vercel.app/

---

## 📄 License

This project is licensed under the **Creative Commons BY-NC-ND 4.0** License.

- You may view and study the code
- You may NOT use it commercially
- You may NOT redistribute or modify without permission

© 2026 Vishnu Teja. All rights reserved.
