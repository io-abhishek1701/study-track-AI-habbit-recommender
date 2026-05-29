import os
from google import genai
import streamlit as st

MODEL_NAME = "gemini-2.5-flash"
_client = None


def get_gemini_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key

    try:
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def get_client():
    global _client
    if _client is None:
        api_key = get_gemini_api_key()
        if not api_key:
            return None
        _client = genai.Client(api_key=api_key)
    return _client

def generate_student_feedback(study, work, play, sleep, marks, cluster, cluster_desc=None):
    # Map the cluster ID to a readable word for the AI
    cluster_map = {0: "Average", 1: "Poor", 2: "Excellent"}
    cluster_desc = cluster_desc or cluster_map.get(cluster, "Unknown")

    prompt = f"""
    You are a friendly academic mentor.
    Student Details:
    - Study Hours: {study}, Work Hours: {work}, Play: {play}, Sleep: {sleep}
    - Predicted Marks: {marks}, Performance Cluster: {cluster_desc}

    Write a short (4-6 lines) personalized, encouraging feedback. 
    Include one improvement and one practical suggestion.
    """

    try:
        client = get_client()
        if client is None:
            return "Gemini feedback is unavailable because GEMINI_API_KEY is not configured."

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error generating feedback: {e}"
