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

# Словарь замен
LINKS_MAP = {
    'https://t.me/tribute/app?startapp=sp5Q': 'https://t.me/tribute/app?startapp=sxAX',
    'https://bingxdao.com/invite/P8XF2F': URL_BINGX,
    'https://t.me/+MTQNJMUsSiowOWU6': 'https://t.me/bratvadaily',
    'trusteeglobal.com/ru/?r=OXvE1XQ90Bb': 'https://trusteeglobal.com/?r=0aTeQwzM9Bb',
    'https://www.weex.com/ru/register?vipCode=nftz': URL_WEEX # Новая замена
}

# Шаблон кнопок
MY_BUTTONS = [[Button.url("WEEX ↗️", URL_WEEX), Button.url("BINGX ↗️", URL_BINGX)]]

# Гиперссылка для названия
MY_CHANNEL_LINK = "[BRATVA|DAILY](https://t.me/bratvadaily)"

# Тексты
NEW_WEEX_TEXT = f"""🔥 Биржа WEEX — топ-платформа с лаунчпадами и защитой активов!

— 980+ монет, 1 579 пар
— $1.8 млрд суточного объёма
— Фонд защиты на 1 000 BTC
— Лицензии: US MSB, Canada, SVGFSA

🚀 WXT — ключ к лаунчпадам (уже 116+ проектов, 2–3 в месяц).
Держи от 1 000 WXT и участвуй! 

UAH доступно с помощью P2P
Бонус на торговлю 30 000 USDT

🔗 Регистрируйся по ссылке все бонусы здесь:
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
    text = event.message.text or ""
    if "googleusercontent.com" in text.lower(): return

    # 1. Очистка рекламы и ребрендинг в гиперссылку
    text = re.split(r'\n?\s*РЕКЛАМА', text, flags=re.IGNORECASE)[0].strip()
    text = re.sub(r'SHARKINEWS', MY_CHANNEL_LINK, text, flags=re.IGNORECASE)
    text = text.replace("SHARK|NEWS", MY_CHANNEL_LINK)

    # 2. Замена всех ссылок из словаря (включая Trustee и WEEX nftz)
    for old, new in LINKS_MAP.items():
        text = text.replace(old, new)

    if not text and not event.message.media: return

    try:
        # 3. Логика пересылки
        # Проверка на WEEX (старый текст или старая ссылка nftz)
        if "300 халявных альткоинов" in text or "WEEX" in text or "vipCode=nftz" in text:
            await client.send_file(TARGET_CHANNEL, WEEX_IMG, caption=NEW_WEEX_TEXT, parse_mode='md')
        
        elif "Доступ в лучший сигнальный канал" in text or "Доступ к обучению" in text:
            await client.send_file(TARGET_CHANNEL, VIP_IMG, caption=NEW_EDUCATION_TEXT, parse_mode='md')
        
        elif "bingxdao.com" in text:
            await client.send_file(TARGET_CHANNEL, BINGX_IMG, caption=text, parse_mode='md')
        
        elif "#Итоги_Дня" in text:
            await client.send_file(TARGET_CHANNEL, ITOGI_IMG, caption=text, buttons=MY_BUTTONS, parse_mode='md')
        
        elif "Доброе утро" in text:
            media = event.message.media if event.message.media else None
            await client.send_file(TARGET_CHANNEL, media, caption=text, buttons=MY_BUTTONS, parse_mode='md')
        
        else:
            if event.message.media:
                await client.send_file(TARGET_CHANNEL, event.message.media, caption=text, parse_mode='md')
            else:
                await client.send_message(TARGET_CHANNEL, text, parse_mode='md')
        
        print("Пост переслан!")
    except Exception as e:
        print(f"Ошибка: {e}")

# Бесконечный цикл работы
while True:
    try:
        print("Запуск бота...")
        client.start()
        print("Бот в сети!")
        client.run_until_disconnected()
    except Exception as e:
        print(f"Сбой: {e}. Рестарт через 10 сек...")
        time.sleep(10)
