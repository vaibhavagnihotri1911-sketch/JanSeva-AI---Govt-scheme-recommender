# JanSeva AI — Government Scheme Recommender

**JanSeva AI** is an intelligent government-scheme discovery platform designed to help citizens find relevant government schemes based on their needs and personal circumstances.

Instead of requiring users to know the exact name of a government scheme, the platform allows them to describe their requirement in natural language using **Hindi, Hinglish, or English**.

The application combines **Natural Language Processing (NLP), rule-based information extraction, intent detection, eligibility-aware filtering, and TF-IDF-based text relevance ranking** to retrieve relevant schemes.

---

## Features

### 🔎 Natural-Language Scheme Search

Users can describe their requirement in their own words instead of searching only by an exact scheme name.

Example:

> "main ek poor student hoon scholarship chahiye"

The system processes the query and identifies relevant information before retrieving matching government schemes.

### 🧠 NLP-Based Processing

The application uses a lightweight NLP pipeline that includes:

* Text normalization
* Rule-based entity extraction
* Age extraction
* Income-related information extraction
* Occupation detection
* Gender detection
* State detection
* Intent/category detection
* Query expansion using related terms

### 📊 TF-IDF-Based Relevance Ranking

The recommendation pipeline uses:

**TF-IDF Vectorization + Cosine Similarity**

to represent user queries and scheme information as numerical vectors and rank schemes according to their textual relevance.

This is a lightweight information-retrieval approach and does not require a large language model or a deep-learning embedding model.

### 🌐 Hindi, Hinglish and English Input

The system supports natural-language queries in:

* English
* Hindi
* Hinglish / transliterated Hindi

Hindi input can be normalized into an English representation before downstream NLP processing.

### 🎙️ Voice Search

The application supports voice-based queries through two approaches:

* Browser-supported Web Speech API
* MediaRecorder-based fallback for browsers where native speech recognition is unavailable

For the backend fallback, recorded audio is processed using speech-recognition and audio-conversion libraries.

### 🎨 Interactive Web Interface

The frontend provides:

* Responsive dashboard
* Dark mode
* Featured scheme carousel
* Category-based discovery
* Search interface
* Voice-search interface
* Dynamically rendered recommendation results

---

## How the Recommendation Pipeline Works

The overall flow is:

```text
User Query
    ↓
Frontend
    ↓
Flask API
    ↓
Text Normalization
    ↓
Entity Extraction
    ↓
Intent / Category Detection
    ↓
Eligibility / Candidate Filtering
    ↓
Query Expansion
    ↓
TF-IDF Vectorization
    ↓
Cosine Similarity
    ↓
Ranking
    ↓
Top Relevant Schemes
    ↓
Frontend Results
```

### 1. User Input

The user enters a text query or provides a voice query.

Example:

```text
I am a farmer from Uttar Pradesh and need crop insurance.
```

### 2. Text Normalization

The input is normalized so that variations in language and representation can be processed consistently.

### 3. Entity Extraction

The NLP layer identifies useful attributes from the query, such as:

```text
Occupation → Farmer
State → Uttar Pradesh
```

Other supported attributes include age, gender and income-related information.

### 4. Intent Detection

The system determines the broad purpose of the query.

Examples include:

```text
Student / Education
Farmer / Agriculture
Health
Women
Business
Senior Citizen
Pension
```

### 5. Candidate / Eligibility Filtering

The available user information is used to reduce irrelevant schemes before relevance ranking.

Depending on the information provided by the user, filtering can consider attributes such as:

* Age
* Gender
* Income
* Occupation
* State
* Category / Intent

Unknown attributes are not treated as explicit user-provided values.

### 6. Query Expansion

The original query can be expanded with related domain terms.

For example:

```text
student scholarship
```

can be associated with terms such as:

```text
education
study
college
scholarship
student
```

This improves the chances of retrieving schemes whose descriptions use related terminology.

### 7. TF-IDF Vectorization

The user's query and scheme text are converted into numerical TF-IDF vectors.

TF-IDF gives greater importance to terms that are informative for distinguishing documents.

### 8. Cosine Similarity

Cosine similarity is used to compare the query vector with scheme vectors.

Higher similarity indicates stronger textual relevance.

### 9. Ranking

Schemes are ranked according to their relevance score and the most relevant results are returned to the frontend.

---

## Tech Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript (ES6+)
* Lucide Icons

### Backend

* Python
* Flask
* REST-style JSON API

### NLP / Information Retrieval

* Scikit-learn
* TF-IDF Vectorization
* Cosine Similarity
* Rule-based entity extraction
* Rule-based intent detection
* Query expansion
* Pandas

### Language Processing

* `deep-translator` for translation
* `indic-transliteration` for transliteration

### Voice Processing

* Web Speech API
* MediaRecorder API
* `SpeechRecognition`
* `pydub`
* FFmpeg for audio conversion where required

---

## Project Structure

```text
JanSeva-AI---Govt-scheme-recommender/
│
├── api.py
├── requirements.txt
├── Procfile
├── README.md
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── frontend-html/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── src/
    ├── cleaning/
    ├── eda/
    ├── features/
    ├── nlp/
    └── recommender/
```

> The `venv/` directory is intentionally not part of the project source structure. It is a local virtual environment created during setup.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/vaibhavagnihotri1911-sketch/JanSeva-AI---Govt-scheme-recommender.git
cd JanSeva-AI---Govt-scheme-recommender
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

Install the dependencies from the project's requirements file:

```powershell
pip install -r requirements.txt
```

### 4. Run the Application

```powershell
python api.py
```

The application runs locally on:

```text
http://localhost:5000
```

Open the URL in a web browser to access the JanSeva AI interface.

---

## Voice Search Requirements

The browser-based voice functionality depends on browser support for the Web Speech API.

For the backend audio-processing fallback, `pydub` may require **FFmpeg** to be installed separately on the system.

After installing FFmpeg, make sure it is available through the system PATH.

---

## How to Use

### Text Search

Enter a natural-language requirement in the search bar.

Example:

```text
main ek poor student hoon scholarship chahiye
```

The system processes the query and returns relevant government schemes.

### Voice Search

1. Click the microphone button.
2. Speak your requirement.
3. The application converts the speech into text.
4. The resulting query is processed by the recommendation pipeline.

### Category Discovery

Use the available category sections to explore schemes related to areas such as:

* Farmers
* Students
* Women
* Health
* Business
* Senior Citizens

### Dark Mode

Use the theme control in the navigation bar to switch between light and dark modes.

---

## Data Processing Pipeline

The project includes a data-processing workflow for preparing government scheme information.

The pipeline includes:

```text
Raw Data
   ↓
Data Cleaning
   ↓
Standardization
   ↓
Dataset Merging
   ↓
Feature Engineering
   ↓
Processed Dataset
   ↓
Recommendation System
```

The preprocessing stage handles tasks such as:

* Column standardization
* Duplicate removal
* Missing-value handling
* Text normalization
* Dataset merging
* Feature creation

---

## Recommendation Approach

JanSeva AI uses a **content/query-based recommendation approach**.

The system does not depend on collaborative filtering or user-rating history.

Instead, recommendations are based on:

```text
User Query
+
Extracted User Information
+
Scheme Information
+
Text Relevance
```

The current relevance-ranking approach uses:

```text
TF-IDF
    +
Cosine Similarity
```

This makes the system lightweight and relatively easy to deploy compared with large neural retrieval models.

---

## Limitations

The current system is designed as a lightweight recommendation platform and has some limitations:

* Entity extraction is primarily rule-based.
* Intent detection relies on predefined patterns and categories.
* TF-IDF provides lexical relevance rather than deep semantic understanding.
* Government scheme information depends on the quality and freshness of the underlying dataset.
* Eligibility information may be incomplete when users do not provide all required details.
* The system should be treated as a scheme-discovery tool rather than a final legal or eligibility authority.
* Users should verify the final eligibility criteria and application requirements through the relevant official government source.

---

## Future Improvements

Potential improvements include:

* Transformer-based sentence embeddings for stronger semantic retrieval
* Vector databases / approximate nearest-neighbor search for larger datasets
* ML-based intent classification
* More robust multilingual NLP
* Improved named-entity recognition
* More comprehensive state and eligibility extraction
* Official scheme URLs and application links
* User authentication and personalized profiles
* Automated evaluation using Precision@K, Recall@K, MRR and NDCG
* Automated dataset updates from verified government sources

---

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.

---

## Team

Built collaboratively by **Vaibhav Agnihotri** and **Sneha Singh** as part of ongoing project work.
