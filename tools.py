import requests
import json
import re
from config import PUSHOVER_USER, PUSHOVER_TOKEN, PUSHOVER_URL, is_pushover_configured

# -------------------- SIMPLE LOGGER --------------------
def log(message):
    print(f"[TOOLS] {message}")


# -------------------- VALIDATION --------------------
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


# -------------------- PUSH FUNCTION --------------------
def push(message):
    if not is_pushover_configured():
        log("Pushover not configured. Skipping push.")
        return {"status": "skipped"}

    payload = {
        "user": PUSHOVER_USER,
        "token": PUSHOVER_TOKEN,
        "message": message
    }

    try:
        response = requests.post(PUSHOVER_URL, data=payload, timeout=5)

        if response.status_code != 200:
            log(f"Pushover failed: {response.text}")
            return {"status": "failed"}

        return {"status": "sent"}

    except Exception as e:
        log(f"Pushover error: {e}")
        return {"status": "error"}


# -------------------- TOOL FUNCTIONS --------------------
def record_user_details(email, name="Name not provided", notes="not provided"):
    if not is_valid_email(email):
        return {"error": "Invalid email format"}

    message = f"Lead captured: {name}, Email: {email}, Notes: {notes}"
    push_result = push(message)

    return {
        "recorded": "ok",
        "push_status": push_result
    }


def record_unknown_question(question):
    if not question or len(question.strip()) == 0:
        return {"error": "Empty question"}

    message = f"Unknown question: {question}"
    push_result = push(message)

    return {
        "recorded": "ok",
        "push_status": push_result
    }


# -------------------- TOOL SCHEMAS --------------------
record_user_details_json = {
    "name": "record_user_details",
    "description": "Record user contact details",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string"},
            "name": {"type": "string"},
            "notes": {"type": "string"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}


record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "CRITICAL: Call this tool IMMEDIATELY if the user asks about personal preferences (e.g., music, hobbies), out-of-domain topics, or anything not explicitly stated in your provided data.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string"}
        },
        "required": ["question"],
        "additionalProperties": False
    }
}


tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]


# -------------------- SAFE TOOL REGISTRY --------------------
TOOL_REGISTRY = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question
}


# -------------------- TOOL HANDLER --------------------
def handle_tool_calls(tool_calls):
    results = []

    for tool_call in tool_calls:
        try:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments or "{}")

            log(f"Tool called: {tool_name}")

            tool = TOOL_REGISTRY.get(tool_name)

            if not tool:
                result = {"error": f"Unknown tool: {tool_name}"}
            else:
                result = tool(**arguments)

        except json.JSONDecodeError:
            result = {"error": "Invalid JSON arguments"}

        except Exception as e:
            result = {"error": str(e)}

        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })

    return results