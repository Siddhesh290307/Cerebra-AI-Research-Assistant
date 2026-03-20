# Cerebra Research RAG Assistant 🧠

Cerebra is a powerful, full-stack Retrieval-Augmented Generation (RAG) assistant specifically designed for research papers. It allows users to search for topics, fetch relevant academic papers, process their content into a vector store, and ask complex questions based on the retrieved data. 

Powered by **Groq** and the `llama-3.3-70b-versatile` model, Cerebra can differentiate between direct queries (directly answerable by context) and open-ended queries (requiring broader ML reasoning), while also automatically generating novel research ideas and hypotheses based on the context.

## 🚀 Key Features

- **Document Fetching & Processing**: Automatically fetches and parses academic papers based on a specified topic.
- **Intelligent Chunking & Embeddings**: Splits papers into logical sections and chunks for semantic search.
- **High-Performance Vector Store**: Custom vector store implemented for fast and accurate context retrieval.
- **Adaptive LLM Generation**: Uses the cutting-edge `llama-3.3-70b-versatile` model via Groq. Categorizes questions internally dynamically to alter its reasoning style (speculative vs grounded).
- **Research Insights Generation**: Automatically deduces high-quality research ideas (hypotheses, mechanisms, metrics, experiments) from the papers.
- **JWT Authentication**: Simple token-based authentication securing the API endpoints.
- **Modern Dashboard**: An interactive, minimal, and beautiful React frontend.

---

## 📸 App Screenshots

### 1. Login Page
Users can log in with demo credentials to access their research workspace.

![Cerebra Login Page](https://raw.githubusercontent.com/Siddhesh290307/Cerebra-AI-Research-Assistant/main/docs/login.png)

**Demo Credentials:**
- **Email:** sidnad@gmail.com
- **Password:** 1234

---

### 2. Signup Page
Create a new account to join the Cerebra research network.

![Cerebra Signup Page](https://raw.githubusercontent.com/Siddhesh290307/Cerebra-AI-Research-Assistant/main/docs/signup.png)

---

### 3. Main Dashboard - Papers Section
View and manage your indexed research papers. The dashboard shows paper metadata, authors, and summaries for quick reference.

![Cerebra Main Dashboard](https://raw.githubusercontent.com/Siddhesh290307/Cerebra-AI-Research-Assistant/main/docs/dashboard.png)

---

### 4. Research Query & AI Synthesis
Ask intelligent questions about your research papers. Cerebra analyzes the papers and provides AI-synthesized answers with citations from source material.

![Cerebra Research Query](https://raw.githubusercontent.com/Siddhesh290307/Cerebra-AI-Research-Assistant/main/docs/research_query.png)

**Features:**
- Semantic search across all indexed papers
- AI synthesis with source attribution
- Session telemetry tracking
- Multi-paper reasoning

---


## 🛠️ Technology Stack

- **Frontend**: React.js, React Router, Axios, CSS (Vanilla)
- **Backend**: Python, FastAPI, Uvicorn
- **AI / LLM API**: Groq API (`llama-3.3-70b-versatile`)
- **Vector Store**: Custom local vector store 
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **PDF Processing**: PyMuPDF, PyPDF2
- **Authentication**: JWT (Python-Jose)

---

## 📂 Project Structure

```text
Cerebra-Research RAG Assisstant/
├── backend/
│   ├── main.py               # FastAPI application entry point
│   ├── llm.py                # Groq integration & RAG prompt logic
│   ├── fetch_papers.py       # Paper fetching logic
│   ├── process_papers.py     # Document processing pipeline
│   ├── retriever.py          # Vector retrieval 
│   ├── vector_store.py       # Custom Local Vector Store
│   ├── simple_auth.py        # JWT-based Auth
│   ├── section_splitter.py   # Splitting papers by semantic sections
│   ├── chunk_model.py        # Chunk schema definition
│   ├── chunker.py            # Logic to chunk text
│   ├── embeddings.py         # Embedding generation
│   ├── pdf_parser.py         # Parsing uploaded/fetched PDFs
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   ├── MainChat.jsx
│   │   │   ├── MyPapers.jsx
│   │   │   ├── SavedSummaries.jsx
│   │   │   └── Sidebar.jsx
│   │   └── App.js
│   ├── public/
│   ├── package.json
│   └── ... 
└── README.md
```

---

## ⚙️ Setup & Installation

Follow these steps to get the project up and running locally.

### 1. Prerequisites
- Python 3.9+
- Node.js (v16+)
- A Groq API Key (get one at https://console.groq.com)

### 2. Environment Variables
Create a `.env` file in the root of the project to add your API credentials:

```ini
GROQ_API_KEY="your_groq_api_key_here"
```

### 3. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Set up your virtual environment (Optional but Recommended):
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you have libraries like `fastapi`, `uvicorn`, `groq`, `pydantic`, `python-dotenv` installed)*

4. Run the FastAPI Development Server:
   ```bash
   python main.py
   # Or directly: uvicorn main:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`. You can explore the Swagger UI documentation at `http://localhost:8000/docs`.

### 4. Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node modules:
   ```bash
   npm install
   ```
3. Run the React Development Server:
   ```bash
   npm start
   ```
   The frontend application will start and be available at `http://localhost:3000`.

---

## 🧠 How it Works (RAG Pipeline)

1. **User requests a Topic**: Through the React dashboard, you enter an academic topic.
2. **Retrieve Papers**: FastAPI backend uses `fetch_papers.py` to get relevant academic PDFs from arXiv.
3. **Parse & Chunk**: PDFs are parsed using `pdf_parser.py`, split semantically via `section_splitter.py`, and chunked with `chunker.py`.
4. **Vector Database**: Chunks are embedded using Sentence Transformers and stored in a custom local vector store via `vector_store.py`.
5. **Question Asking**: When a user queries their research base, `retriever.py` extracts the most semantically relevant text blocks. 
6. **Smart Generation**: `llm.py` takes the prompt against Groq (`llama-3.3-70b-versatile`) and decides whether it is a `known` or `unknown` factor, adjusting its prompt strictness and generating fresh insights concurrently!

### Data Flow Diagram

```
User Query
    ↓
Vector Store Search
    ↓
Retrieve Relevant Chunks
    ↓
Context + Query → Groq LLM
    ↓
AI Synthesis & Response
    ↓
Display with Citations
```

---

## 🚀 Deployment

### Frontend (Vercel)
- **Status:** ✅ LIVE
- **URL:** https://cerebra-ai-research-assistant.vercel.app
- **Cost:** FREE

### Backend (Render)
- **Status:** 🔄 IN PROGRESS
- **Plan:** Starter ($7/month, 2GB RAM)
- **URL:** https://cerebra-backend.onrender.com

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

---

## 🔐 Security

- **JWT Authentication**: All API endpoints (except `/login` and `/health`) require valid JWT tokens.
- **Environment Variables**: Sensitive data (API keys, secrets) are stored in `.env` files.
- **CORS Configuration**: Restricted to authorized frontend URLs.

---

## 📊 API Endpoints

### Public Endpoints

```
GET  /health              # Health check
POST /login               # User login (returns JWT token)
```

### Protected Endpoints (Require Authorization Header)

```
POST /fetch_papers        # Fetch and process papers for a topic
POST /research_query      # Ask questions about indexed papers
```

---

## 🛡️ License

This project is licensed under the MIT License.

This project is intended for research and educational purposes, serving as a reference implementation for learning, experimentation, and academic exploration. However, the software is provided under the terms of the MIT License, which permits use, modification, and distribution, including for commercial purposes, provided that proper attribution is given to the original author.
