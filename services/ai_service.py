import requests

def generate_post_with_ollama(topic, style, model="phi3"):
    prompt = f"""
Write a LinkedIn post.

Topic: {topic}
Style: {style}

Make it engaging and professional.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    return response.json().get("response", "")

def generate_post_with_ollam(topic, style, model="phi3"):
    prompt = f"""
    Answer naturally like ChatGPT.
    
    User: {topic}
    Style: {style}
    
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    return response.json().get("response", "")