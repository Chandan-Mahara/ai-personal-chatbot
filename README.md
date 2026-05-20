# 🤖 AI Personal Chatbot with Self-Evaluation (LLM-as-a-Judge)

## 📌 Overview

This project is an AI-powered personal chatbot that represents an individual professionally by answering questions based on their LinkedIn profile and summary.

What makes this system unique is the integration of a **self-evaluation mechanism**, where a second Large Language Model (LLM) evaluates the chatbot’s response before delivering it. If the response is not acceptable, the system automatically retries and improves it.

---

## 🚀 Key Features

* 🧠 **Persona-based Chatbot**

  * Responds as a specific individual using LinkedIn + summary data

* 📄 **PDF Processing**

  * Extracts content from LinkedIn profile using `pypdf`

* 🤖 **LLM Response Generation**

  * Uses OpenAI model to generate human-like responses

* 🧪 **LLM-as-a-Judge (Evaluation System)**

  * A second LLM evaluates:

    * Accuracy
    * Professional tone
    * Relevance

* 🔁 **Automatic Retry Mechanism**

  * If response fails evaluation, it is regenerated with feedback

* 🌐 **Interactive UI**

  * Built using Gradio for real-time chat interface

---

## 🏗️ Architecture

User Input
⬇
LLM (Response Generator)
⬇
LLM (Evaluator / Judge)
⬇
✔ Accept → Show response
❌ Reject → Retry with feedback

---

## 🛠️ Tech Stack

* Python
* OpenAI API
* Gradio
* PyPDF
* Pydantic
* dotenv

---

## 📂 Project Structure

```
AI-Personal-Chatbot/
│── app.py
│── me/
│   ├── linkedin_profile.pdf
│   ├── summary.txt
│── .env
│── requirements.txt
│── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-url>
cd AI-Personal-Chatbot
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Add API Key

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

### 5. Run the Application

```
python app.py
```

---

## 🌐 Usage

* Open browser at: `http://127.0.0.1:7860`
* Ask questions about the person
* System will:

  1. Generate response
  2. Evaluate response
  3. Improve if needed

---

## 💡 Example

**User:** Do you have experience in machine learning?
**System:**

* Generates answer
* Evaluates quality
* Improves response if needed
* Returns final polished answer

---

## 🧠 Key Concept

This project demonstrates:

> **LLM-as-a-Judge Architecture**

Where:

* One model generates output
* Another model evaluates it
* System self-corrects automatically

---

## 🔮 Future Improvements

* 🔍 Add FAISS for semantic search (RAG)
* ⚡ Streaming responses
* 🧠 Memory optimization
* 🌍 Deployment (Hugging Face / Render)

---

## 👨‍💻 Author

**Chandan Mahara**

---

## ⭐ If you like this project

Give it a star on GitHub!
