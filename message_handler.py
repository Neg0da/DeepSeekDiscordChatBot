# message_handler.py

def process_response(response, max_length=1000):
    start_tag = "<think>"
    end_tag = "</think>"
    
    # Видалення тегів <think>...</think>
    while start_tag in response and end_tag in response:
        start_index = response.find(start_tag)
        end_index = response.find(end_tag) + len(end_tag)
        response = response[:start_index] + response[end_index:]

    # Обрізаємо відповідь за максимальну довжину
    if len(response) > max_length:
        response = response[:max_length] + "..."  # Додаємо три крапки, якщо текст обрізається

    return response.strip()  # Повертаємо оброблений текст

async def send_long_message(channel, text, max_length=2000):
    """
    Розбиває довге повідомлення на частини і відправляє їх по черзі в канал
    """
    for i in range(0, len(text), max_length):
        await channel.send(text[i:i + max_length])
