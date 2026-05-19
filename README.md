# 🏥 Medical Report Bot

**Medical Report Bot** is a Streamlit application that helps users understand medical reports in plain English. Upload a PDF or image of your medical report, and the app will generate a summary, highlight critical findings, and allow interactive Q&A with an AI assistant. It also supports exporting structured PDF summaries.

---

# ✨ Features

* 📄 Upload medical reports (PDF, JPG, PNG)
* 🧾 Plain-English summary of test results and findings
* ❓ Interactive Q&A chatbot to explain medical terminology and results
* 📊 Session tracking with conversation history
* 💾 Export summary as PDF with structured tables
* 🌙 Dark mode support for better readability

---

# 🚀 Getting Started

## 📌 Prerequisites

Make sure the following are installed:

* Python 3.9+
* Streamlit
* FPDF

---

# ⚙️ Installation

```bash
git clone https://github.com/yourusername/medical-report-bot.git
cd medical-report-bot
pip install -r requirements.txt
```

---

# ▶️ Run the App

```bash
streamlit run app.py
```

After running the command, open the local URL shown in the terminal.

---

# 📂 Project Structure

```bash
medical-report-bot/
│── app.py                     # Main Streamlit app
│── modules/
│   ├── pipeline.py            # Document processing pipeline
│   ├── extractor.py           # Extracts text from reports
│   ├── summarizer.py          # Generates report summaries
│   ├── chatbot.py             # AI-powered Q&A assistant
│   └── pdf_export.py          # PDF export functionality
│── uploads/                   # Temporary uploaded files
│── exports/                   # Generated PDF summaries
│── requirements.txt           # Project dependencies
│── README.md                  # Project documentation
│── .env                       # Environment variables
```

---

# 📦 requirements.txt

```txt
streamlit
fpdf
pandas
numpy
Pillow
pdfplumber
python-dotenv
google-generativeai
```

---

# 🧠 How It Works

1. Upload a medical report
2. Extract text from the document
3. Analyze report using AI
4. Generate simplified summaries
5. Ask questions through chatbot
6. Export final summary as PDF

---

# 📸 Screenshot

*Add a screenshot or demo GIF here*

Example:

```markdown
![App Screenshot](screenshot.png)
```

---

# ⚠️ Disclaimer

This project is for educational and informational purposes only.

It helps users understand medical reports but is **NOT** a substitute for:

* Professional medical advice
* Diagnosis
* Treatment
* Emergency healthcare services

Always consult a qualified healthcare professional for medical decisions.

---

# 🤝 Contributing

Pull requests are welcome!

For major changes:

1. Open an issue
2. Discuss proposed updates
3. Submit a pull request

---

# 📜 License

MIT License

Feel free to use, modify, and distribute this project.

---

# 🌟 Future Improvements

* OCR support for handwritten reports
* Multi-language medical explanations
* Voice assistant integration
* User authentication
* Cloud database support
* Doctor recommendation system

---

# 👨‍💻 Built With

* Python
* Streamlit
* Gemini AI
* FPDF

---

# ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork the project
* 🛠️ Contribute improvements

---

> “Making medical reports easier to understand for everyone.”
