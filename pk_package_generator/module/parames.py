from enum import Enum


class payload_location(Enum):
    PATH = "path"
    FILE_NAME = "file_name"
    URL_PARAME = "url_parame"
    USER_AGETN = "user_agent"
    COOKIE = "cookie"
    OTHER_HEAD = "other_head"
    BODY_PARAME = "body_parame"
