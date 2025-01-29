import discord
import logging
import psutil  # Для перевірки навантаження
import config
import api_handler
from message_handler import process_response, send_long_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Глобальна змінна для зберігання поточної моделі
current_model = "deepseek-r1:1.5b"  # За замовчуванням модель

# Функція для зміни моделі
async def switch_model(message, model_type):
    global current_model
    if model_type == "low":
        current_model = "deepseek-r1:1.5b"
        await message.channel.send(f"Модель успішно змінено на {current_model}")
    elif model_type == "high":
        current_model = "deepseek-r1:8b"
        await message.channel.send(f"Модель успішно змінено на {current_model}")
    else:
        await message.channel.send("Будь ласка, використовуйте один з аргументів: `low` або `high`")

# Функція для перевірки системного статусу
async def system_status(message):
    # Отримуємо інформацію про використання процесора
    cpu_usage = psutil.cpu_percent(interval=1)  # Відсоток використання процесора за 1 секунду
    # Отримуємо інформацію про використання пам'яті
    memory = psutil.virtual_memory()
    memory_usage = memory.percent  # Відсоток використання пам'яті
    # Отримуємо інформацію про вільне місце на диску
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent  # Відсоток використання диска

    # Формуємо відповідь
    status_message = (
        f"💻 **Система**:\n"
        f"🔹 **Процесор**: {cpu_usage}%\n"
        f"🔹 **Пам'ять**: {memory_usage}%\n"
        f"🔹 **Диск**: {disk_usage}%\n"
    )
    
    # Відправляємо повідомлення
    await message.channel.send(status_message)

# Обробка повідомлень
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ігнорувати повідомлення від самого бота

    # Обробка команди !switch для зміни моделі
    if message.content.startswith("!switch"):
        parts = message.content.split()
        if len(parts) == 2:
            await switch_model(message, parts[1])
        else:
            await message.channel.send("Будь ласка, введіть аргумент: `!switch low` або `!switch high`")
        return

    # Обробка команди !systemstatus для перевірки системного навантаження
    if message.content.startswith("!systemstatus"):
        await system_status(message)
        return

    # Якщо це не команда для зміни моделі чи перевірки системного статусу, обробляємо інші повідомлення
    prompt = message.content.strip()

    # Запитуємо відповідь у моделі
    response = api_handler.ask_ollama(prompt, current_model)

    # Обробляємо відповідь (видаляємо <think>...</think>)
    processed_response = process_response(response)

    # Відправляємо оброблену відповідь
    if processed_response:  # Якщо щось залишилося після обробки
        await send_long_message(message.channel, processed_response)

# Подія при запуску бота
@client.event
async def on_ready():
    logging.info(f"Бот увійшов у систему як {client.user}")

# Запуск бота
client.run(config.DISCORD_API_KEY)
