import requests
import config

# Функція для запиту до моделі
def ask_ollama(prompt, model):
    data = {
        "model": model,  # Використовуємо передану модель
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(config.AI_API_KEY, json=data)
        response.raise_for_status()
        return response.json().get("response", "Не вдалося отримати відповідь.")
    except requests.exceptions.RequestException as e:
        return f"Помилка під час звернення до моделі: {e}"
