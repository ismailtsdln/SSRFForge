from modules.exploit_manager import BaseModule
from utils.logger import Logger

class BlindSSRF(BaseModule):
    async def run(self, target_url: str, **kwargs):
        callback_url = kwargs.get("callback")
        if not callback_url:
            Logger.error("Callback URL is required for Blind SSRF testing.")
            return

        Logger.info(f"Testing Blind SSRF using callback: {callback_url}")
        res = await self.engine.get(target_url.replace("SSRF", callback_url))
        
        if res.get("status"):
            Logger.info(f"Request sent to target. Check your listener at {callback_url}")
        
        return {"callback_sent": True}
