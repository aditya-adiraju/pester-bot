# Module to enable timestamped logs
from datetime import datetime
from pytz import utc, timezone

class LOG_LEVEL:
    ERROR = 'ERR'
    INFO  = 'INF'
    DEBUG = 'DBG'

def _generate_timestamp() -> str:
    date_format = "%d-%b-%Y %H:%M:%S"
    date = datetime.now(tz=utc)
    date = date.astimezone(timezone('US/Pacific'))
    return date.strftime(date_format)

def _log(log_level: str, *values: object, sep: str | None = " ", end: str | None = "\n") -> str | None:
    print(f"[{log_level}][{_generate_timestamp()}]", *values, sep=sep, end=end)
    log_file_name = 'debug_log.txt' if log_level == LOG_LEVEL.DEBUG else 'log.txt'
    with open(log_file_name, 'a') as log_file:
        print(f"[{log_level}] [{_generate_timestamp()}]", *values, sep=sep, end=end, file=log_file)
    
    if log_level == LOG_LEVEL.ERROR:
        from io import StringIO
        s = StringIO()
        print(f"[{log_level}] [{_generate_timestamp()}]", *values, sep=sep, end=end, file=s)
        result = s.getvalue()
        return result


def error(*values: object, sep: str | None = " ", end: str | None = "\n") -> str | None:
    return _log(LOG_LEVEL.ERROR, *values, sep=sep, end=end)

def info(*values: object, sep: str | None = " ", end: str | None = "\n") -> str | None:
    return _log(LOG_LEVEL.INFO, *values, sep=sep, end=end)

def debug(*values: object, sep: str | None = " ", end: str | None = "\n") -> str | None:
    return _log(LOG_LEVEL.DEBUG, *values, sep=sep, end=end)
