import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, target: str):
        self.target = target
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data = {
            "target": target,
            "scan_time": self.timestamp,
            "findings": []
        }

    def add_finding(self, module: str, result: any, params: dict = None):
        self.data["findings"].append({
            "module": module,
            "params": params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

    def save_json(self, output_dir: str = "reports"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filename = f"report_{self.timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(self.data, f, indent=4)
        return filepath

    def save_markdown(self, output_dir: str = "reports"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filename = f"report_{self.timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w") as f:
            f.write(f"# SSRFForge Scan Report - {self.target}\n\n")
            f.write(f"Date: {self.timestamp}\n\n")
            f.write("## Findings\n\n")
            
            for finding in self.data["findings"]:
                f.write(f"### Module: {finding['module']}\n")
                f.write(f"- **Time**: {finding['timestamp']}\n")
                if finding['params']:
                    f.write(f"- **Parameters**: `{finding['params']}`\n")
                f.write("#### Result:\n")
                f.write("```json\n")
                f.write(json.dumps(finding['result'], indent=2))
                f.write("\n```\n\n")
                
        return filepath
