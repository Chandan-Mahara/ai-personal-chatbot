
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr


# Load environment variables
load_dotenv(override=True)

# Initialize OpenAI client
openai = OpenAI()


# Read LinkedIn PDF
reader = PdfReader("me/linkedin_profile.pdf")

linkedin = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text


# print(linkedin)


# Read summary file
with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()


# Define name
name = "Chandan Mahara"


# Create system prompt
system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website,
particularly questions related to {name}'s career, background, skills and experience.

Your responsibility is to represent {name} for interactions on the website as faithfully as possible.

You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions.

Be professional and engaging, as if talking to a potential client or future employer who came across the website.

If you don't know the answer, say so.
"""

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."


# Chat function
def chat(message, history):
    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": message}]
    )

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content


# Launch Gradio interface
gr.ChatInterface(chat).launch()