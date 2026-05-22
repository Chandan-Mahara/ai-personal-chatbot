import gradio as gr
from agent import chat


# -------------------- SAFE CHAT --------------------
def safe_chat(message, history):
    try:
        result = chat(message, history)

        # Ensure string output
        if not isinstance(result, str):
            result = str(result)

        return result

    except Exception as e:
        print("[ERROR]", e)
        return "❌ Something went wrong. Check terminal."


# -------------------- UI --------------------
with gr.Blocks(title="AI Personal Chatbot") as demo:

    gr.Markdown("""
    # 🤖 AI Personal Chatbot
    Ask anything about Chandan Mahara's professional background.
    """)

    # Removed `type="messages"` - Gradio will auto-detect the dictionary format
    chatbot = gr.Chatbot()

    msg = gr.Textbox(
        placeholder="Ask a question...",
        show_label=False
    )

    clear = gr.Button("Clear Chat")

    # -------------------- USER INPUT --------------------
    def user_input(user_message, history):
        history = history or []
        # Append as a standard message dictionary
        history.append({"role": "user", "content": str(user_message)})
        return "", history

    # -------------------- BOT RESPONSE --------------------
    def bot_response(history):
        try:
            # The last item is the user's message dictionary
            user_message = history[-1]["content"]

            # Exclude the latest user message to form the history for the LLM
            formatted_history = history[:-1]

            reply = safe_chat(user_message, formatted_history)

            # Append the assistant's reply as a dictionary
            history.append({"role": "assistant", "content": str(reply)})

            return history

        except Exception as e:
            print("[BOT ERROR]", e)
            history.append({"role": "assistant", "content": "❌ Internal error"})
            return history

    # -------------------- EVENTS --------------------
    msg.submit(user_input, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_response, chatbot, chatbot
    )

    clear.click(lambda: [], None, chatbot, queue=False)


# -------------------- RUN --------------------
if __name__ == "__main__":
    print("🚀 Starting app...")
    demo.launch(debug=True)