# Deployment and Source Control Guide

## 1. Pushing to GitHub (For Team Collaboration)
I have already initialized the Git repository and committed all the code locally on your machine. However, the repository at `https://github.com/syfr512/Project-Veritas` is empty because we haven't *pushed* the code to the remote server yet. 

To push the code and make it visible to your team:
1. Open your terminal (PowerShell or Command Prompt).
2. Navigate to your project folder: `cd "D:\Project Veritas"`
3. Run the following command:
   ```bash
   git push -u origin main
   ```
4. A browser window or command prompt will appear asking you to log into GitHub. Once you authenticate, all the code (including the new Document Forensics, Video Forensics, and Auth logic) will be uploaded to your repository!

## 2. Live Server Deployment (For Final Presentation)
To test the platform live or deploy it for your final presentation, I recommend using **Render.com** (which has a free tier) or **DigitalOcean**. 

I have already created the `.github/workflows/deploy.yml` which can be used alongside these services.

### Option A: Render (Easiest, Free Tier Available)
1. Go to [Render.com](https://render.com) and connect your GitHub account.
2. Click **New +** -> **Web Service**.
3. Select your `syfr512/Project-Veritas` repository.
4. Set the **Root Directory** to `backend/`.
5. Set the **Build Command** to: `pip install -r requirements.txt`
6. Set the **Start Command** to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. In the **Environment Variables** section, add your `OPENAI_API_KEY`.
8. *Repeat the process for the Frontend (Root Directory: `frontend/`, Build: `npm run build`, Start: `npm run start`).*

### Option B: VPS Deployment via Docker
For the final production deployment in Semester 8, we can easily containerize the application. Simply ask me to generate a `docker-compose.yml` file, and you will be able to run the entire backend, frontend, and database on any $5 Linux server with a single command:
`docker-compose up -d`
