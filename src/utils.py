from datetime import datetime

def current_time() -> str:
    # Generate current time
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")