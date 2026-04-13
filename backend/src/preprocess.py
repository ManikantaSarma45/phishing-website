from urllib import parse
import ipaddress


def is_valid_url(parsed: parse.ParseResult) -> bool:
    if not parsed.hostname:
        return False

    try:
        if ipaddress.ip_address(parsed.hostname):
            return True

    except ValueError:
        pass

    if "@" in parsed.netloc:
        return False

    if "." in parsed.hostname:
        return True
    return False


def preprocess(url: str) -> str:
    url = url
    url = url.strip().lower()
    url = parse.unquote(url)

    if url.startswith("//"):
        url = "http:" + url
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = parse.urlparse(url)
    # print(is_valid_url())
    if not is_valid_url(parsed):
        return None

    return url
