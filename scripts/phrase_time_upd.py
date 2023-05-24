from datetime import datetime

def hello_phrase() -> str:
    date = datetime.now()
    hour = date.hour
    if hour >= 0 and hour < 6:
        return ("Доброй ночи, пользователь.")
    
    if hour >= 6 and hour < 12:
        return ("Доброе утро, пользователь.")

    if hour >= 12 and hour < 18:
        return ("Добрый день, пользователь.")

    if hour >= 18 and hour < 24:
        return ("Добрый вечер, пользователь.")
