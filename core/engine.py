import aiohttp
import ssl
from typing import Dict, Any, Optional

class HTTPEngine:
    def __init__(self, timeout: int = 15, verify_ssl: bool = False, proxy: Optional[str] = None, user_agent: str = "SSRFForge/1.0"):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.verify_ssl = verify_ssl
        self.proxy = proxy
        self.headers = {"User-Agent": user_agent}
        self.connector = aiohttp.TCPConnector(ssl=False if not verify_ssl else None)

    async def request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        if "headers" not in kwargs:
            kwargs["headers"] = self.headers
        else:
            kwargs["headers"].update(self.headers)

        async with aiohttp.ClientSession(timeout=self.timeout, connector=self.connector) as session:
            try:
                async with session.request(method, url, proxy=self.proxy, **kwargs) as response:
                    return {
                        "status": response.status,
                        "headers": dict(response.headers),
                        "body": await response.text(),
                        "url": str(response.url)
                    }
            except Exception as e:
                return {"error": str(e)}

    async def get(self, url: str, **kwargs):
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs):
        return await self.request("POST", url, **kwargs)
