from flask import Flask, render_template, request, send_file
import os

from pipeline import process_text
from email_utils import send_email
from pdf_utils import generate_pdf
from chatbot_utils import ask_question

# 🔥 NEW: Whisper for audio/video
import whisper

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model once
whisper_model = whisper.load_model("base")

# Store last results
_data = {"summary": "", "actions": "", "decisions": "", "transcript": ""}


# ── HOME ─────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html", active_page="home")


# ── ANALYZE (TEXT + AUDIO + VIDEO) ───────
@app.route("/analyze", methods=["POST"])
def analyze():

    text = request.form.get("text", "").strip()
    file = request.files.get("file")

    # 🔥 If file uploaded → convert to text
    if file and file.filename != "":
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            result = whisper_model.transcribe(filepath)
            text = result["text"]
        except Exception as e:
            return render_template(
                "index.html",
                active_page="analyse",
                error=f"Error processing file: {str(e)}"
            )

    # ❌ No input
    if not text:
        return render_template(
            "index.html",
            active_page="analyse",
            error="Please provide text or upload audio/video."
        )

    # ✅ Process text
    summary, actions, decisions = process_text(text)

    # Store
    _data["summary"] = summary
    _data["actions"] = actions
    _data["decisions"] = decisions
    _data["transcript"] = text

    return render_template(
        "index.html",
        active_page="analyse",
        summary=summary,
        actions=actions,
        decisions=decisions,
        transcript=text
    )


# ── CHATBOT ──────────────────────────────
@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question", "").strip()

    if not question:
        return render_template(
            "index.html",
            active_page="analyse",
            answer="Please type a question.",
            **_data
        )

    answer = ask_question(_data["transcript"], question)

    return render_template(
        "index.html",
        active_page="analyse",
        answer=answer,
        **_data
    )


# ── EMAIL ────────────────────────────────
@app.route("/send_email", methods=["POST"])
def email():
    recipient = request.form.get("email", "").strip()

    if not recipient:
        return render_template(
            "index.html",
            active_page="analyse",
            email_status="Error: No recipient email provided.",
            **_data
        )

    status = send_email(
        recipient,
        _data["summary"],
        _data["actions"],
        _data["decisions"]
    )

    return render_template(
        "index.html",
        active_page="analyse",
        email_status=status,
        **_data
    )


# ── PDF DOWNLOAD ─────────────────────────
@app.route("/download_pdf")
def download_pdf():
    if not _data["summary"]:
        return "No analysis available yet.", 400

    filename = generate_pdf(
        _data["summary"],
        _data["actions"],
        _data["decisions"]
    )

    return send_file(filename, as_attachment=True)


# ── RUN ──────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
