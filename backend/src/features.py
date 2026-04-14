from collections import Counter
from contextlib import redirect_stdout
from cryptography import x509
from datetime import datetime, timezone
import tldextract
import re
from urllib import parse
import pandas as pd
import ipaddress
import math
import os
import requests
import socket
import ssl
import whois

from backend.src.data_loader import (
    load_hosting_websites,
    load_url_shorteners,
    load_tranco_websites,
)
from backend.src.utils import logger


class FeatureExtraction:
    def __init__(self):
        self.url = None
        self.parsed = None
        self.extracted = None
        self.creation_dt = None
        self.expiry_dt = None
        self.url_shorteners = load_url_shorteners()
        self.hosting_websites = load_hosting_websites()
        self.top_1m_domains = load_tranco_websites()
        self.tld_suffixes = set(tldextract.TLDExtract().tlds)
        pattern = r"\.(?:%s)\b" % "|".join(map(re.escape, self.tld_suffixes))
        self.tld_regex = re.compile(pattern)
        self.SUS_WORDS = {
            'verify', 'confirm', 'validate', 'suspended', 'unlock', 'restore',
            'urgent', 'immediate', 'alert', 'warning', 'expired', 'limited',
            'webscr', 'signin', 'unusual', 'reactivate', 'action', 'required',
            'recovery', 'secured', 'update', 'billing', 'notification', 'activity',
            'resolution', 'customer', 'support'
        }

    def _shannon_entropy(self, s: str) -> float:
        if not s:
            return 0.0
        counts = Counter(s)
        length = len(s)
        return -sum((c / length) * math.log2(c / length) for c in counts.values())

    def url_length(self) -> int:
        return len(self.url)

    def domain_length(self) -> int:
        return len(self.domain) if self.domain else 0

    def path_length(self) -> int:
        return len(self.parsed.path)

    def path_depth(self) -> int:
        return self.parsed.path.rstrip("/").count("/")

    def num_subdomains(self) -> int:
        if not self.subdomain:
            return 0
        return len(self.subdomain.split("."))

    def num_queries(self) -> int:
        return len(parse.parse_qs(self.parsed.query))

    def url_entropy(self) -> float:
        return self._shannon_entropy(self.url)

    def domain_entropy(self) -> float:
        return self._shannon_entropy(self.domain or "")

    def path_entropy(self) -> float:
        return self._shannon_entropy(self.parsed.path.strip("/"))

    def url_digit_ratio(self) -> float:
        digits = sum(c.isdigit() for c in self.url)
        chars = sum(c.isalpha() for c in self.url)
        total = digits + chars
        if total == 0:
            return 0.0
        return digits / total

    def domain_digit_ratio(self) -> float:
        s = self.domain or ""
        digits = sum(c.isdigit() for c in s)
        chars = sum(c.isalpha() for c in s)
        total = digits + chars
        if total == 0:
            return 0.0
        return digits / total

    def path_digit_ratio(self) -> float:
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
        return 1 if parse.urlparse(self.final_url).scheme == "https" else 0

    def num_redirects(self) -> int:
        return self.redirects

    def has_port_in_url(self) -> int:
        return 0 if self.parsed.port is None else 1

    def non_standard_port(self) -> int:
        STANDARD_PORTS = {80, 443, 21, 22, 25}
        try:
            port = self.parsed.port
            return 1 if port is not None and port not in STANDARD_PORTS else 0
        except ValueError:
            return 0

    def prefix_suffix(self) -> int:
        return self.domain.count('-') if self.domain else 0

    def suspicious_words_url(self) -> int:
        return len([word for word in self.SUS_WORDS if word in self.url])

    def suspicious_words_domain(self) -> int:
        return len([word for word in self.SUS_WORDS if word in self.parsed.netloc])

    def suspicious_words_path(self) -> int:
        return len([word for word in self.SUS_WORDS if word in self.parsed.path])

    def suspicious_tld(self) -> int:
        return int(self.sus_tld)

    def tld_in_subdomain(self):
        return int(bool(self.tld_regex.search(self.subdomain or "")))

    def tld_in_path(self):
        return int(bool(self.tld_regex.search(self.parsed.path or "")))

    def shortened_url(self) -> int:
        hostname = self.registrable_domain
        if hostname in self.url_shorteners:
            return 1
        return 0

    def hosted_website(self) -> int:
        hostname = self.registrable_domain
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
        if self.has_ip():
            return -1
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
        return int(self.domain.startswith("xn--")) if self.domain else 0

    def tranco_indexed(self) -> int:
        hostname = self.registrable_domain
        try:
            if hostname in self.top_1m_domains:
                return 1
            return 0
        except ConnectionError:
            return -1
        
    def extract_features(self, url: str) -> list:
        if url is None:
            return None

        # url = url.strip().lower()
        # url = parse.unquote(url)

        # if url.startswith("//"):
        #     url = "http:" + url
        # if not url.startswith(("http://", "https://")):
        #     url = "http://" + url

        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.head(url, allow_redirects=True, timeout=5, headers=headers)
            self.redirects = len(response.history)
            final_url = response.url

        except:
            try:
                domain = f"{parse.urlparse(url).scheme}://{parse.urlparse(url).netloc}"
                response = requests.head(domain, allow_redirects=True, timeout=5, headers=headers)
                self.redirects = len(response.history)
                final_url = response.url
            except Exception as e:
                self.redirects = -1
                final_url = url
                pass

        self.url = url
        self.final_url = final_url
        self.parsed = parse.urlparse(url)
        self.extracted = tldextract.extract(url)
        self.hostname = self.parsed.hostname
        self.creation_dt = None
        self.expiry_dt = None

        if self.extracted.suffix:
            self.sus_tld = False
            self.registrable_domain = self.extracted.top_domain_under_public_suffix
            self.domain = self.extracted.domain
            self.subdomain = self.extracted.subdomain
        else:
            self.sus_tld = True
            self.registrable_domain = self.hostname
            self.domain = None
            self.subdomain = None


        try:
            if self.registrable_domain:
                rdap_url = (
                    f"https://rdap.verisign.com/com/v1/domain/{self.registrable_domain}"
                    if self.registrable_domain.endswith((".com", ".net"))
                    else f"https://rdap.org/domain/{self.registrable_domain}"
                )
            else:
                rdap_url = None

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
                    data = whois.whois(self.registrable_domain)

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
            
        url_features = {
        "url_length": self.url_length(),
        "domain_length": self.domain_length(),
        "path_length": self.path_length(),
        "path_depth": self.path_depth(),
        "num_subdomains": self.num_subdomains(),
        "num_queries": self.num_queries(),
        "url_entropy": self.url_entropy(),
        "domain_entropy": self.domain_entropy(),
        "path_entropy": self.path_entropy(),
        "url_digit_ratio": self.url_digit_ratio(),
        "domain_digit_ratio": self.domain_digit_ratio(),
        "path_digit_ratio": self.path_digit_ratio(),
        "dot_count": self.dot_count(),
        "at_count": self.at_count(),
        "dollar_count": self.dollar_count(),
        "underscore_count": self.underscore_count(),
        "dash_count": self.dash_count(),
        "question_mark_count": self.question_mark_count(),
        "percent_count": self.percent_count(),
        "ampersand_count": self.ampersand_count(),
        "hash_count": self.hash_count(),
        "suspicious_words_url": self.suspicious_words_url(),
        "suspicious_words_domain": self.suspicious_words_domain(),
        "suspicious_words_path": self.suspicious_words_path(),
        "prefix_suffix": self.prefix_suffix(),
        "suspicious_tld": self.suspicious_tld(),
        "tld_in_subdomain": self.tld_in_subdomain(),
        "tld_in_path": self.tld_in_path(),
        "has_ip": self.has_ip(),
        # "https": self.https(),
        "num_redirects": self.num_redirects(),
        "creation_days": self.creation_days(),
        "expiry_days": self.expiry_days(),
        "ssl_expiry": self.ssl_expiry(),
        "has_port_in_url": self.has_port_in_url(),
        "non_standard_port": self.non_standard_port(),
        "shortened_url": self.shortened_url(),
        "hosted_website": self.hosted_website(),
        "punycode": self.punycode(),
        # "tranco_indexed": self.tranco_indexed(),
        }

        features = pd.DataFrame([url_features], index=None)
        logger.info(f"Features of URL:\n{features.values}")

        return features
