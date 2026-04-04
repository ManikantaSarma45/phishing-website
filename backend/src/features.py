from collections import Counter
from contextlib import redirect_stdout
from cryptography import x509
from datetime import datetime, timezone
import tldextract
from tranco import Tranco
from urllib import parse
import ipaddress
import math
import os
import pandas as pd
import requests
import socket
import ssl
import whois
DATAPATH= os.path.join("backend", "data")

class FeatureExtraction:
    def __init__(self):
        self.url = None
        self.parsed = None
        self.extracted = None
        self.creation_dt = None
        self.expiry_dt = None
        self.url_shorteners = set(pd.read_csv(f"{DATAPATH}/url_shorteners.csv").url)
        self.hosting_websites = set(
            pd.read_csv(f"{DATAPATH}/hosting_websites.csv").domain
        )
        self.top_1m_domains = set(
            Tranco(cache=True, cache_dir=".tranco").list().top(1000000)
        )

    def _shannon_entropy(self, s: str) -> float:
        if not s:
            return 0.0
        counts = Counter(s)
        length = len(s)
        return -sum((c / length) * math.log2(c / length) for c in counts.values())

    def url_length(self) -> int:
        return len(self.url)

    def domain_length(self) -> int:
        return len(self.extracted.domain)

    def path_length(self) -> int:
        return len(self.parsed.path)

    def path_depth(self) -> int:
        return self.parsed.path.rstrip("/").count("/")

    def num_subdomains(self) -> int:
        if not (subdomains := self.extracted.subdomain):
            return 0
        return len(subdomains.split("."))

    def num_queries(self) -> int:
        return len(parse.parse_qs(self.parsed.query))

    def url_entropy(self) -> float:
        return self._shannon_entropy(self.url)

    def domain_entropy(self) -> float:
        return self._shannon_entropy(self.extracted.domain)

    def path_entropy(self) -> float:
        return self._shannon_entropy(self.parsed.path.strip("/"))

    def url_digit_ratio(self, url: str) -> float:
        digits = sum(c.isdigit() for c in url)
        chars = sum(c.isalpha() for c in url)
        total = digits + chars
        if total == 0:
            return 0.0
        return digits / total

    def domain_digit_ratio(self, url: str) -> float:
        digits = sum(c.isdigit() for c in self.extracted.domain)
        chars = sum(c.isalpha() for c in self.extracted.domain)
        total = digits + chars
        if total == 0:
            return 0.0
        return digits / total

    def path_digit_ratio(self, url: str) -> float:
        digits = sum(c.isdigit() for c in self.parsed.path.strip("/"))
        chars = sum(c.isalpha() for c in self.parsed.path.strip("/"))
        total = digits + chars
        if total == 0:
            return 0.0
        return digits / total

    def dot_count(self) -> int:
        return self.url.count(".")

    def at_count(self) -> int:
        return self.url.count("@")

    def dollar_count(self) -> int:
        return self.url.count("$")

    def underscore_count(self) -> int:
        return self.url.count("_")

    def dash_count(self) -> int:
        return self.url.count("-")

    def question_mark_count(self) -> int:
        return self.url.count("?")

    def percent_count(self) -> int:
        return self.url.count("%")

    def ampersand_count(self) -> int:
        return self.url.count("&")

    def hash_count(self) -> int:
        return self.url.count("#")

    def has_ip(self) -> int:
        try:
            ipaddress.ip_address(self.parsed.hostname)
            return 1
        except Exception:
            return 0

    def https(self) -> int:
        return 1 if self.parsed.scheme == "https" else 0

    def num_redirects(self) -> int:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.head(
                self.url, allow_redirects=True, timeout=3, headers=headers
            )
            return len(response.history)
        except Exception:
            return -1

    def has_port_in_url(self) -> int:
        return 0 if self.parsed.port is None else 1

    def non_standard_port(self) -> int:
        STANDARD_PORTS = {80, 443, 21, 22, 25}
        try:
            port = self.parsed.port
            return 1 if port is not None and port not in STANDARD_PORTS else 0
        except ValueError:
            return 0

    def shortened_url(self) -> int:
        hostname = self.extracted.top_domain_under_public_suffix
        if hostname in self.url_shorteners:
            return 1
        return 0

    def hosted_website(self) -> int:
        hostname = self.extracted.top_domain_under_public_suffix
        if hostname in self.hosting_websites:
            return 1
        return 0

    def creation_days(self) -> int:
        try:
            # Check if domain is available for registration
            if self.creation_dt == -2:
                return -2

            # Check if creation date is None
            if self.creation_dt is None:
                return -1

            dt = self.creation_dt
            # Ensure timezone awareness
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            return (datetime.now(timezone.utc) - dt).days

        except Exception:
            return -1

    def expiry_days(self) -> int:
        try:
            # Check if domain is available for registration
            if self.expiry_dt == -2:
                return -2

            # Check if expiry date is None
            if self.expiry_dt is None:
                return -1

            dt = self.expiry_dt
            # Ensure timezone awareness
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            return (dt - datetime.now(timezone.utc)).days

        except Exception:
            return -1

    def ssl_expiry(self) -> int:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        try:
            hostname = self.parsed.hostname
            with socket.create_connection((hostname, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    data = ssock.getpeercert(True)
                    pem_data = ssl.DER_cert_to_PEM_cert(data)
                    cert_data = x509.load_pem_x509_certificate(str.encode(pem_data))
                    ssl_expiry = (
                        cert_data.not_valid_after_utc - datetime.now(timezone.utc)
                    ).days
                    return ssl_expiry
        except Exception:
            return -1

    def punycode(self) -> int:
        return int(self.extracted.domain.startswith("xn--"))

    def tranco_indexed(self) -> int:
        hostname = self.extracted.top_domain_under_public_suffix
        try:
            if hostname in self.top_1m_domains:
                return 1
            return 0
        except ConnectionError:
            return -1

    def extract_features(self, url: str) -> list:
        if url is None:
            return None
        self.url = url
        self.parsed = parse.urlparse(self.url)
        self.extracted = tldextract.extract(self.url)

        self.domain = self.extracted.top_domain_under_public_suffix
        try:
            rdap_url = (
                f"https://rdap.verisign.com/com/v1/domain/{self.domain}"
                if self.domain.endswith((".com", ".net"))
                else f"https://rdap.org/domain/{self.domain}"
            )

            r = requests.get(rdap_url, timeout=5)

            if r.status_code == 200:
                data = r.json()

                for e in data.get("events", []):
                    action = e.get("eventAction", "").lower()
                    date = e.get("eventDate")

                    if not date:
                        continue

                    try:
                        dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
                    except Exception:
                        continue

                    if (
                        "registration" in action or "create" in action
                    ) and self.creation_dt is None:
                        self.creation_dt = dt

                    elif "expir" in action and self.expiry_dt is None:
                        self.expiry_dt = dt

        except Exception:
            pass

        if self.creation_dt is None or self.expiry_dt is None:
            try:
                with open(os.devnull, "w") as f, redirect_stdout(f):
                    data = whois.whois(self.domain)

                if "available for registration" in str(data).lower():
                    self.creation_dt = -2
                    self.expiry_dt = -2
                else:
                    c = data.get("creation_date")
                    e = data.get("expiration_date")

                    if isinstance(c, list):
                        c = min([d for d in c if d is not None], default=None)
                    if isinstance(e, list):
                        e = min([d for d in e if d is not None], default=None)

                    if c and isinstance(c, datetime) and c.tzinfo is None:
                        c = c.replace(tzinfo=timezone.utc)
                    if e and isinstance(e, datetime) and e.tzinfo is None:
                        e = e.replace(tzinfo=timezone.utc)

                    self.creation_dt = self.creation_dt or c
                    self.expiry_dt = self.expiry_dt or e

            except Exception:
                pass

        url_features = []

        url_features.append(self.url_length())
        url_features.append(self.domain_length())
        url_features.append(self.path_length())
        url_features.append(self.path_depth())
        url_features.append(self.num_subdomains())
        url_features.append(self.num_queries())
        url_features.append(self.url_entropy())
        url_features.append(self.domain_entropy())
        url_features.append(self.path_entropy())
        url_features.append(self.url_digit_ratio(url))
        url_features.append(self.domain_digit_ratio(url))
        url_features.append(self.path_digit_ratio(url))
        url_features.append(self.dot_count())
        url_features.append(self.at_count())
        url_features.append(self.dollar_count())
        url_features.append(self.underscore_count())
        url_features.append(self.dash_count())
        url_features.append(self.question_mark_count())
        url_features.append(self.percent_count())
        url_features.append(self.ampersand_count())
        url_features.append(self.hash_count())
        url_features.append(self.has_ip())
        # url_features.append(self.https())
        url_features.append(self.num_redirects())
        url_features.append(self.creation_days())
        url_features.append(self.expiry_days())
        url_features.append(self.ssl_expiry())
        url_features.append(self.has_port_in_url())
        url_features.append(self.non_standard_port())
        url_features.append(self.shortened_url())
        url_features.append(self.hosted_website())
        url_features.append(self.punycode())
        url_features.append(self.tranco_indexed())

        return url_features
