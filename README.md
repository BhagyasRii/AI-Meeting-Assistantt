# AI Meeting Intelligence System

An AI-powered Meeting Intelligence System that analyzes meeting transcripts, audio, and video files to generate summaries, action items, decisions, chatbot responses, PDF reports, and email reports.

---

## 🚀 Features

- 🎙 Audio & Video Transcription using OpenAI Whisper
- 📋 AI Meeting Summarization using BART
- ✅ Action Item Extraction
- 🔑 Decision Extraction
- 🤖 AI Chatbot for Meeting Q&A
- 📄 PDF Report Generation
- 📧 Email Sharing using SendGrid
- 🧠 Intelligent NLP Pipeline

---

## 🛠 Tech Stack

### Backend
- Python
- Flask

### AI & NLP
- OpenAI Whisper
- Hugging Face Transformers
- Facebook BART Large CNN
- PyTorch

### Audio/Video Processing
- FFmpeg

### PDF & APIs
- ReportLab
- SendGrid API

### UI
- Flask Templates
- Gradio

---

## 📂 Project Structure

```bash
AI-Meeting-Assistant/
│
├── app.py
├── model.py
├── pipeline.py
├── prompts.py
├── chatbot_utils.py
├── email_utils.py
├── pdf_utils.py
├── ui.py
├── requirements.txt
│
├── templates/
├── uploads/
└── static/
```

---

## ⚙ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI-Meeting-Assistant.git
cd AI-Meeting-Assistant
```

### 2️⃣ Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Additional Packages

```bash
pip install openai-whisper gradio ffmpeg-python
```

---

## 🎬 Install FFmpeg

### Windows
Download:
https://ffmpeg.org/download.html

Add FFmpeg `bin` folder to system PATH.

Verify:

```bash
ffmpeg -version
```

### Ubuntu / Linux

```bash
sudo apt install ffmpeg
```

### MacOS

```bash
brew install ffmpeg
```

---

## 🔥 Install PyTorch

```bash
pip install torch torchvision torchaudio
```

---

## 📧 Configure Email API

Open `email_utils.py` and add:

```python
SENDGRID_API_KEY = "YOUR_API_KEY"
SENDER_EMAIL = "YOUR_EMAIL"
```

---

## ▶ Run Application

```bash
python app.py
```

Open in browser:

```bash
http://127.0.0.1:5000
```

---

## 📦 Requirements

```txt
flask
transformers
torch
sentencepiece
reportlab
requests
openai-whisper
gradio
ffmpeg-python
```

---

## 💡 Future Enhancements

- 🌐 Multi-language Support
- ☁ Cloud Deployment
- 📊 Analytics Dashboard
- 👥 Speaker Identification
- 🧠 LLM Integration

---

## 👩‍💻 Author

**Bhagyasree Sunkara**

---

## ⭐ Support

If you found this project useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 🛠 Contribute improvements
