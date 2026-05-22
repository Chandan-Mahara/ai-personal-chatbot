from config import client
from tools import tools, handle_tool_calls
from prompts import get_system_prompt
from data_loader import load_data

import json

# -------------------- LOAD DATA --------------------
linkedin, summary = load_data()
name = "Chandan Mahara"

# -------------------- EVALUATOR PROMPT --------------------
evaluator_system_prompt = """
You are an expert evaluator.

Check if the assistant response is:
1. Accurate (based on provided data)
2. Professional
3. Relevant to the question

Return JSON:
{
    "is_acceptable": true/false,
    "feedback": "reason"
}
"""

def evaluate_response(reply, message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": evaluator_system_prompt},
                {
                    "role": "user",
                    "content": f"""
User Question:
{message}

Assistant Response:
{reply}

Evaluate this response.
"""
                }
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        return {"is_acceptable": True, "feedback": f"Evaluation failed: {e}"}


# -------------------- CHAT FUNCTION --------------------
def chat(message, history):

    system_prompt = get_system_prompt(name, summary, linkedin)

    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": message}]
    )

    max_iters = 5
    final_reply = None

    for _ in range(max_iters):

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools
            )

        except Exception as e:
            return f"❌ API Error: {e}"

        choice = response.choices[0]

        # -------------------- TOOL HANDLING --------------------
        if choice.finish_reason == "tool_calls":
            msg = choice.message
            tool_calls = msg.tool_calls

            results = handle_tool_calls(tool_calls)

            # FIX: Convert the Pydantic object to a dictionary before appending
            messages.append(msg.model_dump(exclude_unset=True))
            messages.extend(results)
            continue

        # -------------------- NORMAL RESPONSE --------------------
        reply = choice.message.content
        final_reply = reply

        # -------------------- EVALUATION --------------------
        evaluation = evaluate_response(reply, message)

        if evaluation.get("is_acceptable"):
            return reply

        # -------------------- RETRY WITH FEEDBACK --------------------
        feedback = evaluation.get("feedback", "Improve the response")

        messages.append({
            "role": "assistant",
            "content": reply
        })

        messages.append({
            "role": "system",
            "content": f"Improve your previous answer. Feedback: {feedback}"
        })

    # -------------------- FALLBACK --------------------
    return final_reply or "Sorry, I couldn't generate a good response."