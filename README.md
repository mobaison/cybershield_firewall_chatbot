git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**Since your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    Since your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    ```env
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

4.  **Run the App:**
    Since your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    ```env
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

4.  **Run the App:**
    ```bash
    python app.py
    ```
    Navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)Since your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    ```env
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

4.  **Run the App:**
    ```bash
    python app.py
    ```
    Navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)` in your browser.

---

## 📊 Directory Overview (Inside `hospital_chatbot/`)

| Folder/File | Description |
| :--- |Since your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    ```env
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

4.  **Run the App:**
    ```bash
    python app.py
    ```
    Navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)` in your browser.

---

## 📊 Directory Overview (Inside `hospital_chatbot/`)

| Folder/File | Description |
| :--- | :--- |
| `firewall/` | Contains the 7 individual security layer scripts. |
| `rag/` | Core logic for FASince your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    ```env
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

4.  **Run the App:**
    ```bash
    python app.py
    ```
    Navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)` in your browser.

---

## 📊 Directory Overview (Inside `hospital_chatbot/`)

| Folder/File | Description |
| :--- | :--- |
| `firewall/` | Contains the 7 individual security layer scripts. |
| `rag/` | Core logic for FAISS, BM25, Re-ranking, and Memory. |
| `data/` | The curated hospital knowledge base (166 chunks). |
| `templatesSince your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    ```env
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

4.  **Run the App:**
    ```bash
    python app.py
    ```
    Navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)` in your browser.

---

## 📊 Directory Overview (Inside `hospital_chatbot/`)

| Folder/File | Description |
| :--- | :--- |
| `firewall/` | Contains the 7 individual security layer scripts. |
| `rag/` | Core logic for FAISS, BM25, Re-ranking, and Memory. |
| `data/` | The curated hospital knowledge base (166 chunks). |
| `templates/` | The frontend Chat UI and Triage Card display. |
| `app.py` | The main Flask entry point. |

---

##Since your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    ```env
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

4.  **Run the App:**
    ```bash
    python app.py
    ```
    Navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)` in your browser.

---

## 📊 Directory Overview (Inside `hospital_chatbot/`)

| Folder/File | Description |
| :--- | :--- |
| `firewall/` | Contains the 7 individual security layer scripts. |
| `rag/` | Core logic for FAISS, BM25, Re-ranking, and Memory. |
| `data/` | The curated hospital knowledge base (166 chunks). |
| `templates/` | The frontend Chat UI and Triage Card display. |
| `app.py` | The main Flask entry point. |

---

## 🛡️ Safety & Triage
If a user input is identified as a medical symptom, the system triggers the **Symptom Checker (Triage Engine)**,Since your GitHub repository currently has the main logic nested inside a subfolder, this `README.md` is designed to act as a high-level guide that points users directly to the `hospital_chatbot` directory while explaining the "CyberShield" architecture.

---

# 🛡️ CyberShield: Medical RAG Chatbot with 7-Layer Firewall

Welcome to the **CyberShield Firewall Chatbot** repository. This project implements a secure, medical-grade Retrieval-Augmented Generation (RAG) system powered by **Groq** and **Gemini**, featuring a robust multi-layer security prompt firewall.

## 📂 Project Structure Note
> [!IMPORTANT]  
> **All source code, logic, and implementation files are located in the [`hospital_chatbot/`](./hospital_chatbot) directory.** 
> Please navigate to that folder to view the application code, RAG pipeline, and firewall layers.

---

## 🚀 System Architecture

This system is built to handle sensitive medical queries with high reliability and safety.

### 1. The 7-Layer Prompt Firewall
Before a user query ever reaches the LLM, it passes through a rigorous security stack:
*   **Input Sanitizer:** Validates basic input quality.
*   **Rate Limiter:** Prevents API abuse and controls quotas.
*   **Injection Detector:** Scans for prompt injection attacks (Regex + Base64).
*   **Semantic Guard:** A binary classifier (Groq) to detect malicious intent.
*   **Topic Guard:** Ensures the query is relevant to hospital services.
*   **Content Filter:** Detects harmful or crisis-related language.
*   **Conversation Analyzer:** Monitors multi-turn patterns for suspicious behavior.

### 2. Hybrid RAG Pipeline
*   **Embeddings:** Gemini REST API.
*   **Retrieval:** Hybrid search using **FAISS** (Semantic) and **BM25** (Keyword).
*   **Ranking:** Reciprocal Rank Fusion (RRF) followed by a **Groq-powered Re-ranker** for the top 4 most relevant context chunks.

### 3. Generation & Fallback
*   **Primary:** Groq (High-speed generation).
*   **Fallback:** Gemini (Ensures uptime if Groq fails).
*   **Smart Memory:** Stores entity-extracted summaries to maintain context over long conversations.

---

## 🛠️ Quick Start

### Prerequisites
*   Python 3.9+
*   Google AI Studio API Key (Gemini)
*   Groq Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mobaison/cybershield_firewall_chatbot.git
    cd cybershield_firewall_chatbot/hospital_chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file inside the `hospital_chatbot/` folder:
    ```env
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

4.  **Run the App:**
    ```bash
    python app.py
    ```
    Navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)` in your browser.

---

## 📊 Directory Overview (Inside `hospital_chatbot/`)

| Folder/File | Description |
| :--- | :--- |
| `firewall/` | Contains the 7 individual security layer scripts. |
| `rag/` | Core logic for FAISS, BM25, Re-ranking, and Memory. |
| `data/` | The curated hospital knowledge base (166 chunks). |
| `templates/` | The frontend Chat UI and Triage Card display. |
| `app.py` | The main Flask entry point. |

---

## 🛡️ Safety & Triage
If a user input is identified as a medical symptom, the system triggers the **Symptom Checker (Triage Engine)**, providing a RED/YELLOW/GREEN urgency card instead of standard advice, ensuring patient safety.
