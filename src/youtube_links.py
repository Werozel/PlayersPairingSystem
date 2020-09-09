import re
from typing import Optional


def parse_id(link: str) -> Optional[str]:
    try:
        if re.match("^https://www.youtube.com/watch.*$", link):
            return __parse_id_from_raw_url(link)
        elif re.match("^https://youtu.be/.*$", link):
            return __parse_id_from_copied_url(link)
        else:
            return None
    except Exception:
        return None


def __parse_id_from_raw_url(link: str) -> Optional[str]:
    start_i = link.find('v=') + 2
    if start_i == -1:
        return None
    end_i = link.find('&', start_i)
    end_i = end_i if end_i != -1 else len(link)
    return link[start_i: end_i]


def __parse_id_from_copied_url(link: str) -> str:
    args = link.split('/')[-1]
    end_i = args.find('?')
    end_i = end_i if end_i != -1 else len(args)
    return args[: end_i]
