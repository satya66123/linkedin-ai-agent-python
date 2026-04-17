from repository.post_repository import insert_post
from services.ai_service import generate_post_with_ollama, generate_post_with_ollam

def generate_post(topic, style, model):
    return generate_post_with_ollama(topic, style, model)

def generate_post2(topic, style, model):
    return generate_post_with_ollam(topic, style, model)

def save_post(user_id, topic, content, model):
    insert_post(user_id, topic, content, model)