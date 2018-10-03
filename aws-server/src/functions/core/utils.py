"""This is python3.6 program."""


from datetime import datetime, timezone, timedelta
import decimal
import json
import hashlib
import string


def epoc_second_now():
    return epoc_by_second_precision(datetime.now())


def epoc_millisecond_now():
    return decimal.Decimal(datetime.now().timestamp())


def epoc_by_second_precision(time: datetime):
    return decimal.Decimal(time.replace(microsecond=0).timestamp())


def unixtime_to_yyymm(unixtime_second: int):
    return datetime.fromtimestamp(unixtime_second).strftime('%Y%m')


def unixtime_to_jst_string(unixtime_second: int):
    return unixtime_to_jst(unixtime_second).strftime('%Y-%m-%d %H:%M:%S%z')


def unixtime_to_jst(unixtime_second: int):
    jst = timezone(timedelta(hours=+9), 'JST')
    return datetime.fromtimestamp(unixtime_second, jst)


def sha256_digest(source_string) -> string:
    if source_string:
        return hashlib.sha256(source_string.encode('utf-8')).hexdigest()
    else:
        return source_string


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
