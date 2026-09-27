# Project Veritas
**AI-Powered Multimodal Digital Impersonation Detection and Incident Response System**

## Overview
Project Veritas is a modular, enterprise-grade incident response platform designed to detect and mitigate digital impersonation attacks (such as deepfakes, spear-phishing, and forged documents). 

Unlike traditional security tools that rely on a single vector, Veritas aggregates deterministic signals (URL reputation, email headers) and probabilistic AI signals (synthetic audio/video detection, document forensics) into a centralized **Multimodal Evidence Fusion Engine**. The result is an explainable, risk-calibrated dashboard that empowers security analysts to make rapid, informed decisions without relying on black-box autonomous blocking.

## Key Features
*   **Multimodal Evidence Fusion**: Intelligently weights risks across Email, URL, Audio, Video, and Documents to generate a unified 0-100 incident risk score.
*   **Video & Audio Deepfake Forensics**: Utilizes OpenCV and AI Vision models to extract keyframes and detect temporal inconsistencies, unnatural lighting, and synthetic artifacts.
*   **Document Forensics**: Extracts text and scans for signs of digital tampering, mismatched fonts, and suspicious wire transfer instructions in invoices and receipts.
*   **Enterprise Webhook Integration**: Simulates a corporate mail flow rule. Organizations can forward suspicious emails directly to the webhook, bypassing manual uploads, while processing occurs asynchronously via background task queues.
*   **Explainable AI Copilot**: Maps identified threats to the MITRE ATT&CK framework and provides natural language explanations of the risk score.

## Architecture
Project Veritas operates on a modern, decoupled architecture:
*   **Frontend**: Next.js 15, React, Tailwind CSS, shadcn/ui.
*   **Backend**: FastAPI, Python 3.13, SQLite (Development) / PostgreSQL (Production), SQLAlchemy.
*   **Machine Learning**: `opencv-python-headless` for media processing, `PyMuPDF` for document extraction, `scikit-learn` for evaluation, and API-based Vision/Audio inference for cost-effective deployment.

---

## Local Development Setup
To run the platform locally, follow these steps:

### 1. Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: 
   * Windows: `.\venv\Scripts\activate`
   * Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file in the `backend` folder and add your OpenAI API Key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```
6. Start the server: `uvicorn app.main:app --reload --port 8000`

### 2. Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Deployment
Project Veritas is configured for automated CI/CD via GitHub Actions.

**To deploy via Render/Vercel (Free Tier):**
1. Connect your GitHub repository to a platform like [Render](https://render.com) or Vercel.
2. For the **Backend** (Web Service):
   * Root Directory: `backend/`
   * Build Command: `pip install -r requirements.txt`
   * Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   * Add the `OPENAI_API_KEY` to the environment variables.
3. For the **Frontend** (Static Site / Next.js):
   * Root Directory: `frontend/`
   * Build Command: `npm run build`
   * Start Command: `npm run start`

---

## Contributing
We welcome contributions from group members to improve detection logic, UI responsiveness, and documentation.

1. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
2. Commit your changes: `git commit -m "Add your feature"`
3. Push to the branch: `git push origin feature/your-feature-name`
4. Open a Pull Request on GitHub for review.

### Running Thesis Evaluations
To evaluate the model's accuracy for research purposes, place your datasets in `real` and `fake` folders and run:
```bash
python backend/scripts/evaluate_models.py --dataset path/to/dataset --type video
```
This will output the ROC-AUC, Precision, Recall, and F1 scores.
