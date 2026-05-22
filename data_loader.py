import os
from pypdf import PdfReader

# -------------------- LOGGER --------------------
def log(message):
    print(f"[DATA LOADER] {message}")


# -------------------- SAFE PDF LOADER --------------------
def load_pdf_text(file_path):
    if not os.path.exists(file_path):
        log(f"File not found: {file_path}")
        return ""

    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            try:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            except Exception as e:
                log(f"Error reading page: {e}")

        if not text.strip():
            log(f"No text extracted from {file_path}")

        return text

    except Exception as e:
        log(f"PDF loading failed: {e}")
        return ""


# -------------------- SAFE TEXT LOADER --------------------
def load_text_file(file_path):
    if not os.path.exists(file_path):
        log(f"File not found: {file_path}")
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        log(f"Text file loading failed: {e}")
        return ""


# -------------------- MAIN LOADER --------------------
def load_data():
    linkedin_path = "me/linkedin_profile.pdf"
    summary_path = "me/summary.txt"

    linkedin = load_pdf_text(linkedin_path)
    summary = load_text_file(summary_path)

    # -------------------- FALLBACKS --------------------
    if not linkedin:
        log("LinkedIn data missing, using fallback.")
        linkedin = "No LinkedIn data available."

    if not summary:
        log("Summary missing, using fallback.")
        summary = "No summary available."

    return linkedin, summary