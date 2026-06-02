from datetime import datetime, timezone

def format_time(ms: int) -> str:
    if ms == 0:
        return "♾️ Бессрочно"
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return dt.strftime("%d.%m.%Y %H:%M")