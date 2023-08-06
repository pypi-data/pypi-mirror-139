from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

def now(tz: Optional[ZoneInfo] = None):
    if tz is None:
        tz = ZoneInfo('America/Sao_Paulo')
    return datetime.now(tz=tz)