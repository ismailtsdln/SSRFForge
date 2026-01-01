import re
from urllib.parse import urlparse, parse_qs
from typing import List, Dict, Any

class Discovery:
    SUSPICIOUS_PARAMS = [
        "url", "path", "dest", "link", "uri", "redirect", "to", "out", "view",
        "dir", "show", "navigation", "open", "file", "val", "validate", "domain",
        "host", "src", "source", "u", "p"
    ]

    @staticmethod
    def find_suspicious_params(url: str) -> List[str]:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        found = []
        for param in params:
            if any(suspicious in param.lower() for suspicious in Discovery.SUSPICIOUS_PARAMS):
                found.append(param)
        return found

    @staticmethod
    def analyze_headers(headers: Dict[str, str]) -> List[str]:
        ssrf_prone_headers = [
            "X-Forwarded-For", "X-Forwarded-Host", "X-Real-IP", "Referer", "From", "Host"
        ]
        return [h for h in ssrf_prone_headers if h in headers]
