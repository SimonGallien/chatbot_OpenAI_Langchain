# 🧠 Chatbot Summarizer with OpenAI & LangChain

This project was developed as part of the **Machine Learnia** training program.  
It demonstrates how to build an **AI-powered application** using **OpenAI**, **LangChain**, and **Streamlit** with a clean Python environment managed by **pyenv** and **Poetry**.  

The app provides two main features:
1. **Text Summarization** – Upload a `.txt` file in any language, and the model will generate a summary **in English**.
2. **Chatbot Interface** – After summarization, continue interacting with the text via a conversational chatbot.

---

## 🚀 Features
- 🌍 Summarize text files in any language → output in English  
- 💬 Chat with the summarized content  
- 🎨 User-friendly web interface built with **Streamlit**  
- ⚡ Backend served with **FastAPI** and **Uvicorn**  
- 🛠️ Project dependencies managed with **Poetry** and **pyenv**

---

## 📦 Install dependencies with Poetry

```bash
poetry install
```

## Configure environment variables
Create a .env file in the project root and add :
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL_API =your_openai_model
TEMPERATURE =your_temperature_choice (I use 0.2 by default)
```

## ▶️ Running the Application

### 1. Start the backend (FastAPI with Uvicorn)
```bash
poetry run uvicorn backend.main:app --reload
```
This will launch the API server on http://localhost:8000.


### 2. Start the frontend (Streamlit)
```bash
poetry run streamlit run streamlit/app.py
```
This will open the Streamlit interface in your browser at http://localhost:8501.

🐧 Note for WSL Users

When running under WSL, the backend is exposed on the WSL network interface (not directly localhost).
To simplify development, I created a custom alias in my ~/.zshrc:

```bash
nano ~/.zshrc
```
```bash
alias wslip="ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'"
```
This will return your WSL IP address (e.g. 172.25.187.172).
🚨 Use this IP when calling the backend from your Streamlit frontend

## 🗂️ Project Structure
```bash
.
├── api/               # FastAPI backend (summarization, chatbot logic)
├── streamlit/             # Streamlit frontend interface
├── pyproject.toml         # Poetry dependencies
├── .env                   # Environment variables (not tracked in git)
└── README.md              # Project documentation
```

## 📝 Notes

- Summarization always returns English output, even if the source text is in another language.
- The chatbot is powered by LangChain and OpenAI models.
- Both backend and frontend must be running simultaneously.

## 🎯 Future Improvements

- Add PDF and DOCX support in addition to TXT
- Provide multi-language summarization output (not only English)
- Enance conversation memory and context management

## 👨‍💻 Author

This project is part of the Machine Learnia ML Pro program.
Built with ❤️ using Python, LangChain, and OpenAI.