import re
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def normalize_text(text):
    english = text
    hinglish = text

    # 1. Hindi → English
    try:
        english = GoogleTranslator(source='auto', target='en').translate(text)
    except:
        pass

    # 2. Hindi → Hinglish
    try:
        hinglish = transliterate(text, sanscript.DEVANAGARI, sanscript.HK)

        # CLEANING STEP (IMPORTANT)
        hinglish = hinglish.lower()  # convert to lowercase
        hinglish = hinglish.replace('.', '').replace('^', '').replace('~', '')
        hinglish = hinglish.replace('m', 'm')  # optional tweak
        hinglish = hinglish.strip()

    except:
        pass

    return english, hinglish
# TEST
if __name__ == "__main__":
    text = "मैं गरीब छात्र हूँ"

    eng, hing = normalize_text(text)

    print("English:", eng)
    print("Hinglish:", hing)