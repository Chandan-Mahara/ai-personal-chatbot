# 🤖 AI Personal Chatbot with Self-Evaluation & Lead Capture

## 📌 Overview

This project is an AI-powered personal chatbot that represents an individual professionally by answering questions based on their LinkedIn profile and summary. 

What makes this system unique is its advanced agentic architecture. It features a **self-evaluation mechanism (LLM-as-a-Judge)** that critically reviews its own responses before delivering them, and an **Intelligent Tool-Calling system** that captures user leads and unanswerable questions, instantly routing them to the project owner via mobile notifications.

---

## 🚀 Key Features

* 🧠 **Persona-Based RAG System**
  * Responds professionally as a specific individual using parsed LinkedIn and summary data.
* 🧪 **LLM-as-a-Judge (Evaluation System)**
  * A secondary LLM agent evaluates the generated response for accuracy, professional tone, and relevance.
* 🔁 **Automatic Self-Correction**
  * If a response fails the judge's evaluation, it is automatically regenerated with specific feedback before the user ever sees it.
* 🛠️ **Intelligent Tool Calling (OpenAI Functions)**
  * Automatically detects when a user wants to collaborate, hire, or asks an out-of-bounds question, seamlessly triggering background Python functions.
* 📱 **Real-Time Mobile Notifications**
  * Integrates the Pushover API to instantly ping the repository owner's phone when a new lead provides their email or asks a question the bot couldn't answer.
* 📄 **Dynamic Document Processing**
  * Extracts text from uploaded PDF profiles using `pypdf`.
* 🌐 **Interactive UI**
  * Built using Gradio for a seamless, real-time chat interface.

---

## 🏗️ Architecture Flow

User Input 
⬇
LLM (Response Generator / Tool Caller) 
 ├── 🛠️ If Lead/Unknown → Trigger Pushover Notification 
 └── 💬 If Standard Question → Generate Text 
⬇
LLM (Evaluator / Judge) 
⬇
✔ Accept → Show response 
❌ Reject → Retry with feedback loop

---

## 🛠️ Tech Stack

* **Language:** Python
* **AI/ML:** OpenAI API (`gpt-4o-mini`), Pydantic
* **Web UI:** Gradio
* **Integrations:** Pushover API, `requests`
* **Data Processing:** PyPDF
* **Environment:** `python-dotenv`

---

## 📂 Project Structure

```text
AI-Personal-Chatbot/
│── app.py                 # Gradio UI & App Entry Point
│── agent.py               # Main LLM routing & Evaluator Judge
│── tools.py               # OpenAI Tool definitions & Pushover integration
│── prompts.py             # System prompts & behavioral guidelines
│── config.py              # Environment & API Key management
│── data_loader.py         # PDF parsing & text extraction
│── me/
│   ├── linkedin_profile.pdf
│   ├── summary.txt
│── .env                   # Secrets (Not committed)
│── requirements.txt
│── README.md