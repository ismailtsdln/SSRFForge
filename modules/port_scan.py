from modules.exploit_manager import BaseModule
from utils.logger import Logger

class PortScan(BaseModule):
    COMMON_PORTS = [80, 443, 8080, 8443, 22, 21, 23, 25, 53, 3306, 5432, 6379, 27017]

    async def run(self, target_url: str, **kwargs):
        network = kwargs.get("network", "127.0.0.1")
        results = []
        
        Logger.info(f"Scanning common ports on {network}...")
        for port in self.COMMON_PORTS:
            # We assume the target_url has 'SSRF' as a placeholder
            payload = f"http://{network}:{port}"
            res = await self.engine.get(target_url.replace("SSRF", payload))
            
            # Very basic heuristic for port scanning via SSRF
            if res.get("status") and res["status"] != 404:
                Logger.success(f"Port {port} appears to be OPEN or responding.")
                results.append(port)
        
        return results
