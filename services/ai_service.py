import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

SUPPORTED_MODELS = [
    "llama3:latest",
    "llama3:instruct",
    "mistral:latest",
    "phi3:latest"
]

def generate_linkedin_post(topic, model="llama3:instruct"):

    if model not in SUPPORTED_MODELS:
        return f"Invalid model. Supported: {SUPPORTED_MODELS}"

    prompt = f"""
    Act as a top LinkedIn content creator.

    Topic: {topic}

    Write a high-quality LinkedIn post with:
    - Strong hook
    - Engaging content
    - Short paragraphs
    - Call to action
    - 5 hashtags

    Tone: Professional and impactful
    """

    try:
        print(f"[INFO] Generating post using model: {model}")

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=600
        )

        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip().replace("**", "")

    except requests.exceptions.Timeout:
        return "Error: Ollama request timed out"

    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Is it running?"

    except Exception as e:
        return f"Error: {str(e)}"