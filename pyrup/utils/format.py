import datetime
from uuid import uuid4


def generate_unique_str():
    d = datetime.datetime.today()
    return d.strftime('%Y%m%d%H%M%S') + str(uuid4())
