#pip install pandas nltk spacy scikit-learn
#python -m spacy download en_core_web_sm

#making automated resume screener

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

# Ensure stopwords are downloaded
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    """Cleans and preprocesses the input text."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\n+', ' ', text)  # Remove newlines
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # Remove special characters
    text = text.lower().strip()  # Convert to lowercase and strip spaces
    words = [word for word in text.split() if word not in stop_words]  # Remove stopwords
    return ' '.join(words)

def extract_skills(text: str) -> set:
    """Extracts potential skills (nouns and proper nouns) from text using TextBlob."""
    blob = TextBlob(text)
    return {word for word, tag in blob.tags if tag in {"NN", "NNP"}}

def calculate_match_score(resume: str, job_description: str) -> float:
    """Computes a similarity score between a resume and a job description."""
    if not resume or not job_description:
        return 0.0
    
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([resume, job_description]).toarray()
    cosine_sim = cosine_similarity(vectors)
    return round(cosine_sim[0, 1] * 100, 2)  # Convert to percentage

def main():
    try:
        # Load resumes from CSV
        resumes_df = pd.read_csv("resumes.csv")
        
        if "resume" not in resumes_df.columns:
            raise ValueError("CSV must contain a 'resume' column.")
        
        job_description = "Looking for a Data Scientist with experience in Python, Machine Learning, and Deep Learning."
        
        # Process resumes
        resumes_df["cleaned_resume"] = resumes_df["resume"].apply(clean_text)
        resumes_df["skills"] = resumes_df["cleaned_resume"].apply(extract_skills)
        resumes_df["match_score"] = resumes_df["cleaned_resume"].apply(lambda x: calculate_match_score(x, job_description))
        
        # Display results
        print(resumes_df[["resume", "skills", "match_score"]])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()