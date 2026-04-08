# 🚀 GenAI Smart Python IDE

An AI-powered Smart Python IDE built using Django, WebSockets, and Ollama for local AI code generation


---

## ✨ Features

- 🧠 AI Code Generation (Powered by Ollama - Local LLM)
- ⚡ Real-time Code Execution
- 🔄 WebSocket-based Live Terminal
- 🖥️ Interactive Monaco Code Editor
- 🔐 Secure Environment-Based Configuration
- 💻 Fully Local AI (No Paid API Required)

---

## 🛠️ Tech Stack

- Python
- Django
- Django Channels
- WebSockets
- Ollama (Local LLM)
- HTML, CSS, JavaScript
- Monaco Editor

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

'''bash'''
git clone https://github.com/drasti-1650/genai-smart-python-ide.git
cd genai-smart-python-ide/smartide
2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
🤖 AI Setup (Required for Code Generation)

This project uses Ollama for local AI-powered code generation.

🔹 Install Ollama

Download and install from:

https://ollama.com

Verify installation:

ollama --version
🔹 Pull an AI Model

Example using Mistral:

ollama pull mistral
🔹 Run Ollama
ollama run mistral

Keep Ollama running while using the IDE.

🚀 Run the Project
python manage.py runserver

Open your browser:

http://127.0.0.1:8000

⚠️ Important Notes

If Ollama is not installed or running, AI generation will not work.

The IDE interface and code execution will still function.

This project does NOT use OpenAI API.

No paid API key is required.

All AI processing runs locally on your machine.

👩‍💻 Author

Drasti Thakkar

⭐ If you like this project, consider giving it a star!
