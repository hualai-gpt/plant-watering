def time_to_cron(time_str: str, frequency_days: int = 1) -> str:
    """
    将时间字符串（如 "08:00"）转换为 cron 表达式（如 "0 8 */1 * *"）。
    
    Args:
        time_str: 时间字符串，格式为 "HH:MM"
        frequency_days: 频率天数，默认为 1（每天）
        
    Returns:
        str: cron 表达式
    """
    try:
        parts = time_str.split(':')
        if len(parts) == 2:
            hour = int(parts[0])
            minute = int(parts[1])
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                day_part = f"*/{frequency_days}" if frequency_days > 1 else "*"
                return f"{minute} {hour} {day_part} * *"
    except (ValueError, IndexError):
        pass
    
    raise ValueError(f"Invalid time format: '{time_str}'. Expected 'HH:MM'.")
