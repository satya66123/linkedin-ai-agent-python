import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

DEFAULT_MODEL = "phi3:latest"  # 🔥 fast model

def call_ollama(prompt, model=DEFAULT_MODEL):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 200  # 🔥 speed optimization
                }
            },
            timeout=120
        )

        response.raise_for_status()
        return response.json().get("response", "").strip()

    except Exception as e:
        return f"Error: {str(e)}"


# 🔹 Generate Post
def generate_post(topic, model=DEFAULT_MODEL, style="professional"):

    if style == "viral":
        prompt = f"""
        Write a viral LinkedIn post about {topic}.
        Use short punchy lines, strong hook, CTA, and hashtags.
        """
    elif style == "story":
        prompt = f"""
        Tell a short personal story about {topic} for LinkedIn.
        Include lesson and CTA.
        """
    else:
        prompt = f"""
        Write a professional LinkedIn post about {topic}.
        Include hook, content, CTA, and hashtags.
        """

    return call_ollama(prompt, model)


# 🔹 Generate Comment
def generate_comment(content, model=DEFAULT_MODEL):
    prompt = f"Write a professional LinkedIn comment for:\n{content}"
    return call_ollama(prompt, model)


# 🔹 Generate Hashtags
def generate_hashtags(topic, model=DEFAULT_MODEL):
    prompt = f"Generate 8 LinkedIn hashtags for {topic}"
    return call_ollama(prompt, model)

def score_post(content, model="phi3:latest"):
    prompt = f"""
    Rate the following LinkedIn post out of 10 based on:
    - Clarity
    - Engagement
    - Professional tone

    Post:
    {content}

    Return only score and short reason.
    """

    return call_ollama(prompt, model)

from services.rag_service import retrieve_context

def generate_post_with_rag(topic):
    context = retrieve_context(topic)

    context_text = "\n".join(context)

    prompt = f"""
    Use this context:
    {context_text}

    Topic: {topic}
    """

    return call_ollama(prompt)