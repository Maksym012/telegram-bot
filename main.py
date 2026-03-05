import re
import os
import time
from telethon import TelegramClient, events, Button

# --- ДАННЫЕ АВТОРИЗАЦИИ ---
api_id = 26094109 
api_hash = '889bc451951f5d886544b55dfb0e4c53'

SOURCE_CHANNEL = 'https://t.me/+X-ZZt9-I-sM1MjAy' 
TARGET_CHANNEL = 'bratvadaily' 

# Картинки
BINGX_IMG = "bingx_new.png"    
WEEX_IMG = "weex_new.png"      
VIP_IMG = "vip_new.png"       
ITOGI_IMG = "itogi_new.png"    

# Ссылки для кнопок
URL_WEEX = "https://weex.com/register?vipCode=6ultl"
URL_BINGX = "https://bingxdao.com/invite/FCS8N1/"    

# Словарь замен (добавили Trustee сюда для порядка)
LINKS_MAP = {
    'https://t.me/tribute/app?startapp=sp5Q': 'https://t.me/tribute/app?startapp=sxAX',
    'https://bingxdao.com/invite/P8XF2F': URL_BINGX,
    'https://t.me/+MTQNJMUsSiowOWU6': 'https://t.me/bratvadaily',
    'trusteeglobal.com/ru/?r=OXvE1XQ90Bb': 'https://trusteeglobal.com/?r=0aTeQwzM9Bb'
}

# Шаблон кнопок
MY_BUTTONS = [[Button.url("WEEX ↗️", URL_WEEX), Button.url("BINGX ↗️", URL_BINGX)]]

# Тексты
NEW_WEEX_TEXT = """🔥 Забирай халявные монеты WEEX🔥 

По моей ссылке будут минимальные комиссии на спотовую и фьючерсную торговлю отличные условия для трейдеров.

🌟 Ссылка на регистрацию:
👉 Присоединиться к WEEX
💥 Регистрируйтесь сейчас по коду: 6ultl

Зарегистрируйтесь, чтобы получить денежное вознаграждение по моей ссылке ⤵️
https://weex.com/register?vipCode=6ultl"""

NEW_EDUCATION_TEXT = """Доступ к обучению :

📈PNL за декабрь: +15%
📈 PNL за январь: +20%
📈 PNL за февраль: +14,59%

👉 Вход здесь:
https://t.me/tribute/app?startapp=sxAX"""

client = TelegramClient('my_session', api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    # 1. Получаем текст сообщения
    text = event.message.text or ""
    if "googleusercontent.com" in text.lower(): return

    # 2. Очистка рекламы и ребрендинг (SHARKINEWS и SHARK|NEWS)
    text = re.split(r'\n?\s*РЕКЛАМА', text, flags=re.IGNORECASE)[0].strip()
    text = re.sub(r'SHARKINEWS', 'BRATVA|DAILY', text, flags=re.IGNORECASE)
    text = text.replace("SHARK|NEWS", "BRATVA|DAILY")

    # 3. Замена всех ссылок (включая Trustee Plus)
    for old, new in LINKS_MAP.items():
        text = text.replace(old, new)

    if not text and not event.message.media: return

    try:
        # 4. Логика пересылки с учетом разных типов постов
        # Используем parse_mode='md' чтобы убрать звездочки
        
        if "Доступ в лучший сигнальный канал" in text or "Доступ к обучению" in text:
            await client.send_file(TARGET_CHANNEL, VIP_IMG, caption=NEW_EDUCATION_TEXT, parse_mode='md')
        
        elif "300 халявных альткоинов" in text or "WEEX" in text:
            await client.send_file(TARGET_CHANNEL, WEEX_IMG, caption=NEW_WEEX_TEXT, parse_mode='md')
        
        elif "bingxdao.com" in text:
            await client.send_file(TARGET_CHANNEL, BINGX_IMG, caption=text, parse_mode='md')
        
        elif "#Итоги_Дня" in text:
            # Здесь меняем SHARK на BRATVA (если вдруг регекс пропустил)
            text = text.replace("SHARK|NEWS", "BRATVA|DAILY")
            await client.send_file(TARGET_CHANNEL, ITOGI_IMG, caption=text, buttons=MY_BUTTONS, parse_mode='md')
        
        elif "Доброе утро" in text:
            await client.send_file(TARGET_CHANNEL, event.message.media if event.message.media else None, caption=text, buttons=MY_BUTTONS, parse_mode='md')
        
        else:
            # Универсальная отправка: и фото, и видео, и просто текст
            # event.message.media подхватит и видео, и фото автоматически
            if event.message.media:
                await client.send_file(TARGET_CHANNEL, event.message.media, caption=text, parse_mode='md')
            else:
                await client.send_message(TARGET_CHANNEL, text, parse_mode='md')
                
        print("Пост успешно обработан и переслан!")
    except Exception as e:
        print(f"Ошибка при обработке поста: {e}")

# Цикл запуска
while True:
    try:
        print("Попытка запуска бота...")
        client.start()
        print("Бот успешно запущен и работает!")
        client.run_until_disconnected()
    except Exception as e:
        print(f"Ошибка: {e}. Перезапуск через 10 секунд...")
        time.sleep(10)
