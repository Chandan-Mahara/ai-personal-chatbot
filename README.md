# AI Personal Chatbot 🤖

An AI-powered chatbot that answers questions about my career, skills, and experience using my LinkedIn profile as a knowledge base.

---

## 🚀 Overview

This project creates a personalized chatbot using my **LinkedIn profile (PDF)** and a structured summary. It simulates how I would respond in a professional conversation.

---

## 💡 Features

- 🔹 Personalized responses based on LinkedIn data  
- 🔹 Chat interface using Gradio  
- 🔹 Context-aware answers using OpenAI GPT  
- 🔹 Real-time interaction  

---

## 🧠 How it Works

1. Extracts text from LinkedIn PDF using PyPDF  
2. Combines it with a custom summary  
3. Sends context to OpenAI GPT model  
4. Generates responses  
5. Displays via Gradio UI  

---

## 🛠 Tech Stack

- Python  
- OpenAI API  
- Gradio  
- PyPDF  
- python-dotenv  

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/Chandan-Mahara/ai-personal-chatbot.git
cd ai-personal-chatbot

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt