# -------------------- IMPORTS --------------------
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr
from pydantic import BaseModel


# -------------------- SETUP --------------------
load_dotenv()
client = OpenAI()


# -------------------- LOAD FILES --------------------
if not os.path.exists("me/linkedin_profile.pdf"):
    raise FileNotFoundError("LinkedIn PDF not found")

if not os.path.exists("me/summary.txt"):
    raise FileNotFoundError("Summary file not found")


# Read LinkedIn PDF
reader = PdfReader("me/linkedin_profile.pdf")
linkedin = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text


# Read summary
with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()


# -------------------- CONFIG --------------------
name = "Chandan Mahara"


# -------------------- SYSTEM PROMPT --------------------
system_prompt = f"""
You are acting as {name}. You answer questions on {name}'s website.

Be professional, engaging, and accurate.

If you don't know something, say so.

## Summary:
{summary}

## LinkedIn:
{linkedin}
"""


# -------------------- EVALUATION MODEL --------------------
class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str


# -------------------- EVALUATOR PROMPT --------------------
evaluator_system_prompt = f"""
You are an evaluator judging response quality.

Check:
- Accuracy
- Professional tone
- Relevance

Return ONLY JSON:
{{
  "is_acceptable": true/false,
  "feedback": "reason"
}}

## Summary:
{summary}

## LinkedIn:
{linkedin}
"""


def evaluator_user_prompt(reply, message, history):
    return f"""
Conversation:
{history}

User Message:
{message}

Assistant Reply:
{reply}
"""


# -------------------- EVALUATE --------------------
def evaluate(reply, message, history):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": evaluator_system_prompt},
                {"role": "user", "content": evaluator_user_prompt(reply, message, history)}
            ],
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content
        parsed = json.loads(result)

        return Evaluation(**parsed)

    except Exception as e:
        return Evaluation(
            is_acceptable=False,
            feedback=f"Evaluation error: {str(e)}"
        )


# -------------------- HELPER: NORMALIZE HISTORY --------------------
def format_history(history):
    messages = []

    for item in history:
        if isinstance(item, dict):
            # Already correct format
            messages.append(item)

        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_msg, bot_msg = item
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})

    return messages


# -------------------- RETRY --------------------
def rerun(reply, message, history, feedback):

    improved_prompt = system_prompt + f"""
Previous response was rejected.

Your response:
{reply}

Feedback:
{feedback}

Give a better answer.
"""

    messages = [{"role": "system", "content": improved_prompt}]
    messages += format_history(history)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content


# -------------------- CHAT FUNCTION --------------------
def chat(message, history):

    if "patent" in message.lower():
        system = system_prompt + "\nRespond ONLY in Pig Latin."
    else:
        system = system_prompt

    messages = [{"role": "system", "content": system}]
    messages += format_history(history)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    evaluation = evaluate(reply, message, history)

    if evaluation.is_acceptable:
        print("✅ Passed evaluation")
        return reply
    else:
        print("❌ Failed:", evaluation.feedback)
        return rerun(reply, message, history, evaluation.feedback)


# -------------------- GRADIO UI --------------------
gr.ChatInterface(
    fn=chat,
    title="Chandan Mahara - AI Assistant"
).launch()



