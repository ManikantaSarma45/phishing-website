from urllib import parse
import ipaddress


class Preprocessing:
    def __init__(self):
        self.url = None
        self.parsed = None

    def _is_valid_url(self) -> bool:
        if not self.parsed.hostname:
            return False

        try:
            if ipaddress.ip_address(self.parsed.hostname):
                return True

        except ValueError:
            pass

        if "@" in self.parsed.netloc:
            return False

        if "." in self.parsed.hostname:
            return True
        return False

    def preprocess(self, url: str) -> str:
        self.url = url
        self.url = self.url.strip().lower()
        self.url = parse.unquote(self.url)

        if self.url.startswith("//"):
            self.url = "http:" + self.url
        if not self.url.startswith(("http://", "https://")):
            self.url = "http://" + self.url

        self.parsed = parse.urlparse(self.url)
        print(self._is_valid_url())
        if not self._is_valid_url():
            return None

        return self.url
