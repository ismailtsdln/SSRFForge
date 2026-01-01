from modules.exploit_manager import BaseModule
from utils.logger import Logger

class PortScan(BaseModule):
    COMMON_PORTS = [80, 443, 8080, 8443, 22, 21, 23, 25, 53, 3306, 5432, 6379, 27017]

    async def run(self, target_url: str, **kwargs):
        network = kwargs.get("network", "127.0.0.1")
        progress = kwargs.get("progress")
        results = []
        
        Logger.info(f"Scanning common ports on {network}...")
        
        task = None
        if progress:
            task = progress.add_task("[magenta]Scanning ports...", total=len(self.COMMON_PORTS))

        for port in self.COMMON_PORTS:
            payload = f"http://{network}:{port}"
            res = await self.engine.get(target_url.replace("SSRF", payload))
            
            if res.get("status") and res["status"] != 404:
                Logger.success(f"Port {port} is OPEN or responding.")
                results.append(port)
            
            if progress and task is not None:
                progress.update(task, advance=1)
        
        return results
