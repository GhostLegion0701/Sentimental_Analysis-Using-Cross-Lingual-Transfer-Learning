import streamlit as st
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from langdetect import detect

# Initialize translator & sentiment analyzer
translator = Translator()
sia = SentimentIntensityAnalyzer()
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Mapping language codes to full names
LANGUAGE_MAP = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "nl": "Dutch",
}

def detect_language(text):
    """Detects the language of the input text and returns its full name."""
    try:
        lang_code = detect(text)
        return LANGUAGE_MAP.get(lang_code, lang_code)  # Return full name if available, else return code
    except Exception as e:
        return f"Detection Error: {e}"
    
def translate_text(text, target_lang='en'):
    """Translates text to English."""
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        return f"Translation Error: {e}"

def analyze_sentiment_vader(text):
    """Performs sentiment analysis using VADER (for simple sentiment)."""
    scores = sia.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "Positive"
    elif scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def analyze_sentiment_bert(text):
    """Performs sentiment analysis using a deep learning BERT model."""
    result = sentiment_model(text)
    return result[0]['label']

# Streamlit UI
st.title("🌍 Cross-Lingual Sentiment Analysis")
st.write("Enter text in any language, and we'll translate & analyze its sentiment!")

user_input = st.text_area("Enter your sentence:")
if st.button("Analyze Sentiment"):
    if user_input:
        detected_language = detect_language(user_input)
        translated_text = translate_text(user_input)
        sentiment_vader = analyze_sentiment_vader(translated_text)
        sentiment_bert = analyze_sentiment_bert(translated_text)
        
        st.subheader("Results")
        st.write(f"**Detected Language:** {detected_language}")
        st.write(f"**Translated Text:** {translated_text}")
        st.write(f"**VADER Sentiment:** {sentiment_vader}")
        st.write(f"**BERT Sentiment:** {sentiment_bert}")
    else:
        st.warning("Please enter some text!")

st.write("💡 This model supports multilingual sentiment analysis using **Google Translate + NLP Models**.")
