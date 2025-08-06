# 🤖 Minesweeper with Inference Logic

A inference logic visualizer that demonstrates classic inference algorithms like **Truth Table**, **Forward Chaining**,and **Backward Chaining** — with a modern user interface powered by **Vite + React + TypeScript** and a **FastAPI** backend.

You can run it locally, use the CLI, or try it online via the deployed web app.

---

## 🔗 Live Demo

Explore the visualizer here:  
👉 [https://minesweeper-ai-frontend.vercel.app](https://minesweeper-ai-frontend.vercel.app/)

- ✅ **Frontend** hosted on Vercel  
- ✅ **Backend** deployed via Render

---

## ⚙️ Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/minesweeper-ai.git
cd minesweeper-ai
```
## 🖥️ Running Locally (Frontend + Backend)

### ✅ Backend (FastAPI) 

In one terminal:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### ✅ Frontend (React)

In second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open your browser and go to: [http://localhost:3000]

---

## Run Via CLI

You can also execute search algorithms directly using the command line interface.

### 📌 Syntax:

```bash
cd backend
python iengine.py .\test_cases\<filename> <method>
```
filename = your test case file (e.g., test_superhard_genericKB1.txt)
method = algorithm name (e.g., TT, FC, BC)

### 🧪 Example:

```bash
cd backend
python iengine.py .\test_cases\test_superhard_genericKB1.txt TT
```

---

## 📄 License

This project is licensed under the MIT License.
Feel free to fork and build upon it!

---

Let me know your GitHub repo link if you'd like me to insert it into the clone command (`git clone ...`). I can also help you add algorithm documentation or test case guidelines if needed.

