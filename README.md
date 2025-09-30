# SAS RAG Chatbot (FastAPI + Flask UI, Azure Integrated)

This repo provides a **Retrieval-Augmented Generation (RAG) chatbot** for SAS docs.

- **Backend**: FastAPI, integrates **Azure OpenAI + Cognitive Search + Vision OCR**
- **Frontend**: Flask UI with Bootstrap
- **Deployment**: Codespaces-ready, App Service-ready

## 🚀 Running in GitHub Codespaces

1. Open repo in **Codespaces**.
2. Configure environment:
   ```bash
   cd backend
   cp .env.example .env
   # Fill in your Azure endpoints and keys
   ```
3. Run backend and frontend:
   ```bash
   # Terminal 1
   cd backend
   uvicorn main:app --reload --port=8000

   # Terminal 2
   cd frontend
   python app.py
   ```
4. Forward ports **8000** (API) and **5001** (UI).

## 📥 Indexing Docs

- Run once:
  ```bash
  cd backend
  python scripts/create_index.py
  ```

- Run ingestion when docs change:
  ```bash
  cd backend
  python scripts/ingest_docs.py
  ```
