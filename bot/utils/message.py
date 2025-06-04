from config import MESSAGES, BUTTONS, IMAGES, URLS


def msg(section: str, number: str):
    return MESSAGES[section][number]


def btn(section: str, number: str):
    return BUTTONS[section][number]


def img(section: str):
    return IMAGES[section]


def url(section: str):
    return URLS["url"][section]
