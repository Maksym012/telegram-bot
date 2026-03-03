import re
import os
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
    'https://t.me/+MTQNJMUsSiowOWU6': 'https://t.me/bratvadaily'
}

# Шаблон кнопок
MY_BUTTONS = [[Button.url("WEEX ↗️", URL_WEEX), Button.url("BINGX ↗️", URL_BINGX)]]

# Тексты
NEW_WEEX_TEXT = """🔥 Забирай халявные монеты WEEX🔥 
По моей ссылке будут минимальные комиссии на спотовую торговлю и фьючерсную отличные условия для трейдеров.
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
    text = event.message.text or ""
    if "googleusercontent.com" in text.lower(): return

    # Очистка рекламы и ребрендинг
    text = re.split(r'\n?\s*РЕКЛАМА', text, flags=re.IGNORECASE)[0].strip()
    text = re.sub(r'SHARKINEWS', 'BRATVA|DAILY', text, flags=re.IGNORECASE)
    for old, new in LINKS_MAP.items():
        text = text.replace(old, new)

    if not text: return

    try:
        if "Доступ в лучший сигнальный канал" in text or "Доступ к обучению" in text:
            await client.send_file(TARGET_CHANNEL, VIP_IMG, caption=NEW_EDUCATION_TEXT, parse_mode='html')
        elif "300 халявных альткоинов" in text or "WEEX" in text:
            await client.send_file(TARGET_CHANNEL, WEEX_IMG, caption=NEW_WEEX_TEXT, parse_mode='html')
        elif "bingxdao.com" in text:
            await client.send_file(TARGET_CHANNEL, BINGX_IMG, caption=text, parse_mode='html')
        elif "#Итоги_Дня" in text:
            await client.send_file(TARGET_CHANNEL, ITOGI_IMG, caption=text, buttons=MY_BUTTONS, parse_mode='html')
        elif "Доброе утро" in text:
            await client.send_file(TARGET_CHANNEL, event.message.photo if event.message.photo else None, caption=text, buttons=MY_BUTTONS, parse_mode='html')
        else:
            if event.message.photo:
                await client.send_file(TARGET_CHANNEL, event.message.photo, caption=text, parse_mode='html')
            else:
                await client.send_message(TARGET_CHANNEL, text, parse_mode='html')
        print("Пост переслан!")
    except Exception as e:
        print(f"Ошибка: {e}")

print("Бот успешно запущен!")
client.start()
client.run_until_disconnected()