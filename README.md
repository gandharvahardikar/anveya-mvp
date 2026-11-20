# Anveya Labs

Anveya Labs is a single-service LLM assurance web app built with FastAPI and the Google GenAI SDK (`google-genai`). It evaluates two versions of a fictional support chatbot (`AcmeSupportBot` v1 and hardened v2) across **quality**, **safety**, and **security**, combining a deterministic canary rules layer with an independent Gemini judge layer.

By default it runs **5 high-signal test cases** (2 quality, 1 safety, 2 security), with an in-memory UI and API to add custom test cases or one-click add any of 7 additional built-in presets.

## Project Structure

- `main.py` — FastAPI server, Vertex AI / Gemini API client, rules layer, independent judge layer, concurrent runner, and REST API
- `prompts.py` — `CANARY` token (`ANV-7F3K`) and system prompts for `ACME_V1` and `ACME_V2`
- `cases.py` — 5 default test cases + 7 optional preset cases
- `static/index.html` — Single-page vanilla JS interface with test suite manager
- `requirements.txt` — Python dependencies
- `Dockerfile` — `python:3.12-slim` container listening on `$PORT` (default `8080`)
- `.env.example` — Environment variable template

## Environment Variables

Copy `.env.example` to `.env`:

### Vertex AI mode (uses GCP credits via Application Default Credentials)

```env
USE_VERTEX_AI=true
GOOGLE_CLOUD_PROJECT=anveya-labs-77
GOOGLE_CLOUD_LOCATION=global
TARGET_MODEL=deepseek-ai/deepseek-v4.1-flash-maas
JUDGE_MODEL=gemini-3.1-pro-preview
```

### Gemini Developer API mode (optional fallback)

```env
USE_VERTEX_AI=false
GEMINI_API_KEY=<your-ai-studio-key>
TARGET_MODEL=<target-model-id>
JUDGE_MODEL=<independent-judge-model-id>
```

Never commit `.env` or print `GEMINI_API_KEY` to logs.

## Run Locally (Windows PowerShell)

For Vertex AI locally, authenticate Application Default Credentials once:

```powershell
gcloud auth application-default login
```

Then start the server:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

Open `http://localhost:8080` in a browser.

### API Endpoints

- `GET /` — Serves the Anveya Labs web UI
- `GET /health` — Health check
- `GET /api/config` — Non-secret runtime metadata (backend, target model, judge model, case count)
- `GET /api/cases` — List active test cases and available presets
- `POST /api/cases` — Add a custom test case (`{engine, prompt, reference}`)
- `DELETE /api/cases/{id}` — Remove a test case
- `POST /api/cases/reset` — Reset to the 5 default cases
- `POST /api/run` — Body `{"version": "v1"}` or `{"version": "v2"}`; runs all active cases concurrently (max 5 at once)
- `GET /api/compare` — Returns v1-to-v2 score deltas plus `fixed` and `regressed` case IDs once both versions have been run

## Deploy to Google Cloud Run (`asia-south1`, Vertex AI)

1. Enable Vertex AI and grant the Cloud Run default compute service account access:

```powershell
$project = (gcloud config get-value project).Trim()
$projectNumber = (gcloud projects describe $project --format="value(projectNumber)").Trim()
$computeSa = "$projectNumber-compute@developer.gserviceaccount.com"

gcloud services enable aiplatform.googleapis.com --project=$project
gcloud projects add-iam-policy-binding $project `
  --member="serviceAccount:$computeSa" `
  --role="roles/aiplatform.user"
```

2. Deploy from source to Cloud Run in `asia-south1` (reads `TARGET_MODEL`, `JUDGE_MODEL`, and `GOOGLE_CLOUD_LOCATION` from `.env`):

```powershell
gcloud run deploy anveya `
  --source . `
  --region asia-south1 `
  --allow-unauthenticated `
  --set-env-vars "USE_VERTEX_AI=true,GOOGLE_CLOUD_PROJECT=$project,GOOGLE_CLOUD_LOCATION=global,TARGET_MODEL=deepseek-ai/deepseek-v4.1-flash-maas,JUDGE_MODEL=gemini-3.1-pro-preview"
```
