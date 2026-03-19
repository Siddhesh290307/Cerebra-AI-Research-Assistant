# 🚀 Cerebra Deployment Guide

This guide provides step-by-step instructions on how to get the Cerebra RAG Assistant online using completely free tiers from **Render** (for the backend) and **Vercel** (for the frontend).

## Prerequisites

Before starting, ensure you have:
1. A **GitHub account**.
2. **Pushed all this code** to a GitHub repository.
3. Your **Groq API Key**.

---

## Part 1: Backend Deployment (Render)

Render is an excellent platform for hosting FastAPI/Python applications. 

1. **Sign Up / Log In**: Go to [Render](https://render.com) and log in using your GitHub account.
2. **Create New Web Service**:
   - Click the **"New +"** button in the dashboard and select **"Web Service"**.
   - Choose **"Build and deploy from a Git repository"** and select your Cerebra repository.
3. **Configure the Service**:
   Fill out the form with these exact values:
   - **Name**: `cerebra-backend` (or similar)
   - **Region**: Pick whichever is closest to you.
   - **Branch**: `main`
   - **Root Directory**: `backend` *(This is extremely important. If you leave it blank, the deployment will fail!)*
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. **Environment Variables**:
   - Scroll down to the **Advanced** section.
   - Click **Add Environment Variable**.
   - Add `GROQ_API_KEY` as the key, and paste your actual Groq API Key as the value.
   - Add `PYTHON_VERSION` as the key, and set it to `3.10.13` (to avoid dependency conflicts).
5. **Deploy**:
   - Scroll down and click **Create Web Service**. 
   - Render will now start building your Python backend. This might take 3-5 minutes.
6. **Get Your URL**:
   - Once it says *Live* or *Deployed*, look near the top left under your service name. There will be a URL like `https://cerebra-backend-abcd.onrender.com`.
   - **Copy this URL**. You will need it for the frontend!

*(Note about Render Free Tier: If the service receives no traffic for 15 minutes, it will spin down. The next request taking up to a minute to process as it wakes up. Additionally, files saved to the local disk during runtime like your `papers/` and `vector_store/` folders will reset down on a new deploy. This is normal for serverless.)*

---

## Part 2: Frontend `.env` Configuration

Now that your backend is up, your React frontend needs to know where it lives! Right now, the React code looks for `http://localhost:8000`.

1. In the `frontend/` folder, create a file named exactly `.env`.
2. Inside `.env`, add the following line using the backend URL you just copied from Render:
   ```env
   REACT_APP_API_URL=https://cerebra-backend-abcd.onrender.com
   ```
3. In your React source code files (like `Login.jsx` and `MainChat.jsx`), make sure any `axios.post` or `axios.get` call uses this environment variable:
   ```javascript
   const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
   
   // So change something like:
   // axios.post("http://localhost:8000/login", ...)
   // to:
   // axios.post(`${API_URL}/login`, ...)
   ```
*(If you haven't made those Javascript updates yet, do it now and commit those changes to GitHub before proceeding!)*

---

## Part 3: Frontend Deployment (Vercel)

Vercel is the creator of Next.js and the absolute best and easiest place to host a React application.

1. **Sign Up / Log In**: Go to [Vercel](https://vercel.com) and log in with your GitHub account.
2. **Import Project**:
   - Click **Add New Project**.
   - Find your Cerebra repository on GitHub and click **Import**.
3. **Configure Project**:
   - **Project Name**: `cerebra-app` (or similar)
   - **Root Directory**: Click the *Edit* button here and select the `frontend` folder! *(If you leave this blank, it fails).*
   - **Framework Preset**: Vercel should automatically detect **Create React App**. Leave it as is.
   - **Build Command**: Leave as default (`npm run build`).
4. **Environment Variables**:
   - Expand the **Environment Variables** section.
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://cerebra-backend-abcd.onrender.com` *(Your Render URL)*
   - Click **Add**.
5. **Deploy**:
   - Click the massive **Deploy** button.
   - Vercel will install Node modules and build your static assets. It takes about 1-2 minutes.

## Part 4: Success! 🎉

Vercel will give you a final production URL (e.g., `https://cerebra-app.vercel.app`).

You can now use this website anywhere on the internet. Login, search for new papers, let the backend fetch/parse them, and run advanced LLM queries!

---

### Troubleshooting Note: Local Errors
If you were trying to run `uvicorn main:app` locally and hit `"ModuleNotFoundError"` (like for `arxiv`), that means you forgot to ACTIVATE your Python environment or install the `requirements.txt` file locally! 

To fix it locally, run this in your terminal:
```bash
# Windows
cd backend
.\myenv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 10000
```
