import re
from typing import Dict, Any, Optional

class RequestParser:
    @staticmethod
    def parse_raw(raw_request: str) -> Dict[str, Any]:
        lines = raw_request.strip().splitlines()
        if not lines:
            return {}

        # Parse Request Line
        request_line = lines[0]
        match = re.match(r"^(?P<method>\w+)\s+(?P<path>\S+)\s+(?P<version>HTTP/\d\.\d)", request_line)
        if not match:
            return {}

        method = match.group("method")
        path = match.group("path")
        
        headers = {}
        body = ""
        is_body = False
        
        for line in lines[1:]:
            if line == "":
                is_body = True
                continue
            
            if not is_body:
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip()] = value.strip()
            else:
                body += line + "\n"

        return {
            "method": method,
            "path": path,
            "headers": headers,
            "body": body.strip()
        }

    @staticmethod
    def construct_url(headers: Dict[str, str], path: str, ssl: bool = False) -> str:
        host = headers.get("Host", "")
        protocol = "https" if ssl else "http"
        return f"{protocol}://{host}{path}"
