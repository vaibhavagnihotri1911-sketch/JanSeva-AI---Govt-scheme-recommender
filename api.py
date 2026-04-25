from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from src.nlp.text_processing import normalize_text
from src.nlp.entity_extractor import extract_entities
from src.nlp.semantic_search import semantic_search
from run_nlp_tests import detect_intent, apply_strict_filter, expand_query
import os, tempfile

app = Flask(__name__, static_folder='frontend-html')

# Load dataset once when server starts
try:
    df = pd.read_csv("data/processed/final_data.csv")
    print(f"Dataset loaded successfully. Total rows: {len(df)}")
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = pd.DataFrame()


# API Route (must be before catch-all static route)
@app.route('/api/search', methods=['POST'])
def search_schemes():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400

    text = data['query']

    # 1. Clean text
    try:
        clean, _ = normalize_text(text)
    except Exception:
        clean = text.lower()

    # 2. Extract user info
    user = extract_entities(clean)

    # 3. Detect intent
    intent = detect_intent(user, clean)

    # 4. Apply strict filter
    filtered_df = apply_strict_filter(df, intent)
    if len(filtered_df) == 0:
        filtered_df = df.copy()

    # 5. Semantic search
    expanded_query = expand_query(clean, intent)
    results = semantic_search(expanded_query, filtered_df)

    # 6. Confidence filter
    if "score" in results.columns:
        results = results[results["score"] > 0.3]

    # Prepare response — top 6
    top_results = results.head(6)

    response_data = []
    for _, row in top_results.iterrows():
        desc = str(row.get('description', 'No description available.'))
        if len(desc) > 180:
            desc = desc[:180] + "..."
        response_data.append({
            'scheme_name': str(row.get('scheme_name', 'Unknown Scheme')),
            'category':    str(row.get('category', 'General')),
            'description': desc,
            'score':       float(row.get('score', 0))
        })

    return jsonify({
        'intent':  intent,
        'results': response_data
    })


# Voice Transcription Route (Firefox / MediaRecorder fallback)
@app.route('/api/voice', methods=['POST'])
def voice_transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file received'}), 400

    audio_file = request.files['audio']
    content_type = audio_file.content_type or ''

    # Pick extension based on MIME type
    if 'webm' in content_type:
        ext = '.webm'
    elif 'ogg' in content_type:
        ext = '.ogg'
    elif 'mp4' in content_type or 'mpeg' in content_type:
        ext = '.mp4'
    else:
        ext = '.wav'

    tmp_path = wav_path = None
    try:
        import speech_recognition as sr

        # Save uploaded audio to temp file
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name

        wav_path = tmp_path.replace(ext, '_converted.wav')

        # Try pydub conversion (webm/ogg → wav)
        try:
            from pydub import AudioSegment
            seg = AudioSegment.from_file(tmp_path)
            seg.export(wav_path, format='wav')
            final_path = wav_path
        except Exception:
            final_path = tmp_path   # use as-is if pydub not available

        recognizer = sr.Recognizer()
        with sr.AudioFile(final_path) as source:
            audio_data = recognizer.record(source)

        # Try Hindi first, then English
        for lang in ['hi-IN', 'en-IN', 'en-US']:
            try:
                text = recognizer.recognize_google(audio_data, language=lang)
                return jsonify({'transcript': text, 'lang': lang})
            except sr.UnknownValueError:
                continue

        return jsonify({'error': 'Could not understand audio — please speak clearly'}), 400

    except Exception as e:
        return jsonify({'error': f'Voice processing error: {str(e)}'}), 500

    finally:
        for p in [tmp_path, wav_path]:
            if p and os.path.exists(p):
                try: os.unlink(p)
                except: pass


# Frontend Routes
@app.route('/')
def serve_index():
    return send_from_directory('frontend-html', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend-html', path)


if __name__ == '__main__':
    print("Starting MyScheme API on http://localhost:5000")
    app.run(debug=True, port=5000)
