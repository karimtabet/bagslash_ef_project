import string
import random


def get_random_string(size=23, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_http_to_url(to_url):
    if to_url.find("http://") != 0 and to_url.find("https://") != 0:
        to_url = "http://" + to_url
    return to_url
