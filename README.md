# JanSeva AI - Government Scheme Recommender

**JanSeva AI** is an intelligent, AI-powered platform designed to bridge the gap between complex government schemes and the common citizen. Using advanced Natural Language Processing (NLP), it allows users to discover relevant schemes by describing their situation in plain language—Hindi, Hinglish, or English.

## Features

- **AI-Powered Semantic Search**: Uses `sentence-transformers` to understand user intent rather than just keywords.
- **Multilingual Recognition**: Describe your needs in **Hindi**, **Hinglish**, or **English**.
- **Cross-Browser Voice Search**: 
  - Native **Web Speech API** for Chrome, Edge, and Safari.
  - Custom **MediaRecorder Fallback** for Firefox (Audio recording → Backend Transcription).
- **Professional Dashboard**:
  - **Dark Mode** support for better accessibility.
  - Interactive **Carousel** for featured schemes.
  - **Category-based** discovery (Farmers, Students, Women, etc.).
- **Smart NLP Pipeline**:
  - Entity Extraction (Age, Income, Occupation, Gender).
  - Intent Detection to filter relevant schemes.
  - Strict Eligibility Filtering.

## Tech Stack

- **Frontend**: HTML5, Vanilla CSS, Modern JavaScript (ES6+), Lucide Icons.
- **Backend**: Python, Flask.
- **AI/NLP**: 
  - `Sentence-Transformers` (`all-MiniLM-L6-v2`) for semantic matching.
  - `SpeechRecognition` & `pydub` for voice transcription.
  - `Pandas` for data management and filtering.

## Project Structure

```text
india_schemes_project/
├── api.py                 # Flask Server & Search API
├── data/                  # Dataset (Processed CSVs)
├── frontend-html/         # UI Files (HTML, CSS, JS)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── src/
│   ├── nlp/               # Semantic search & entity extraction
│   └── recommender/       # Core recommendation logic
└── venv/                  # Virtual environment
```

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/vaibhavagnihotri1911-sketch/JanSeva-AI---Govt-scheme-recommender.git
cd india_schemes_project
```

### 2. Set up Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install flask pandas sentence-transformers SpeechRecognition pydub
```
*(Note: For Firefox voice support, ensure `ffmpeg` is installed on your system for pydub).*

### 4. Run the Application
```powershell
python api.py
```
Open `http://localhost:5000` in your browser.

## How to Use

1. **Text Search**: Type "main ek poor student hoon scholarship chahiye" in the search bar.
2. **Voice Search**: Click the mic icon and speak your query in Hindi or English.
3. **Categories**: Click on "Farmers" or "Women" cards to see industry-specific schemes.
4. **Theme**: Toggle between Light and Dark mode using the theme icon in the navbar.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
**Developed by Vaibhav Agnihotri - Bridging the gap with AI.**
