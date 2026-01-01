from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from art import tprint
import sys

from core.engine import HTTPEngine
from core.parser import RequestParser
from modules.discovery import Discovery
from modules.exploit_manager import ExploitManager
from modules.cloud_metadata import CloudMetadata
from modules.port_scan import PortScan
from modules.file_read import FileRead
from modules.blind_ssrf import BlindSSRF
from modules.rce_redis import RedisExploit
from modules.rce_fastcgi import FastCGIExploit
from utils.logger import Logger, console
from utils.reporter import ReportGenerator

def display_banner():
    tprint("SSRFForge", font="slant")
    banner_text = Text.assemble(
        ("Advanced SSRF Exploitation Framework\n", "bold cyan"),
        ("Developed by ", "white"), ("Ismail Tasdelen ", "bold magenta"), ("(@ismailtsdln)", "italic white")
    )
    console.print(Panel(banner_text, border_style="bright_blue", expand=False))

async def main():
    display_banner()
    parser = argparse.ArgumentParser(description="SSRFForge - Advanced SSRF Exploitation Framework")
    parser.add_argument("-u", "--url", help="Target URL to test for SSRF")
    parser.add_argument("-r", "--request", help="Burp Suite request file")
    parser.add_argument("-m", "--module", choices=["cloud", "portscan", "fileread", "blind", "redis", "fastcgi"], help="Specific exploitation module to run")
    parser.add_argument("-p", "--proxy", help="Proxy URL (e.g., http://127.0.0.1:8080)")
    parser.add_argument("-lhost", "--lhost", help="Local host for reverse shells (Redis RCE)")
    parser.add_argument("-lport", "--lport", help="Local port for reverse shells (Redis RCE)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-o", "--output", choices=["json", "md"], help="Output report format")
    
    args = parser.parse_args()
    
    if not args.url and not args.request:
        parser.print_help()
        return

    engine = HTTPEngine(proxy=args.proxy)
    exploit_manager = ExploitManager(engine)
    
    # Register modules
    exploit_manager.register_module("cloud", CloudMetadata)
    exploit_manager.register_module("portscan", PortScan)
    exploit_manager.register_module("fileread", FileRead)
    exploit_manager.register_module("blind", BlindSSRF)
    exploit_manager.register_module("redis", RedisExploit)
    exploit_manager.register_module("fastcgi", FastCGIExploit)

    target_url = args.url
    if args.request:
        Logger.info(f"Parsing Burp request from [highlight]{args.request}[/highlight]")
        try:
            with open(args.request, "r") as f:
                parsed_req = RequestParser.parse_raw(f.read())
                target_url = RequestParser.construct_url(parsed_req["headers"], parsed_req["path"])
                Logger.info(f"Target URL constructed: [highlight]{target_url}[/highlight]")
        except FileNotFoundError:
            Logger.error(f"Request file not found: {args.request}")
            return

    reporter = ReportGenerator(target_url)
    Logger.info(f"Starting discovery on [highlight]{target_url}[/highlight]")
    
    suspicious_params = Discovery.find_suspicious_params(target_url)
    if suspicious_params:
        rows = [[p, "High"] for p in suspicious_params]
        Logger.table("Heuristic Discovery Results", ["Parameter", "SSRF Probability"], rows)
        
        if args.module:
            with Logger.get_progress() as progress:
                for param in suspicious_params:
                    Logger.info(f"Testing parameter: [highlight]{param}[/highlight]")
                    # Build test URL with placeholder
                    from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
                    parsed = urlparse(target_url)
                    query = parse_qs(parsed.query)
                    query[param] = ["SSRF"]
                    new_query = urlencode(query, doseq=True)
                    test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
                    
                    module_kwargs = {"lhost": args.lhost, "lport": args.lport, "progress": progress}
                    result = await exploit_manager.run_exploit(args.module, test_url, **module_kwargs)
                    
                    if result:
                        reporter.add_finding(args.module, result, params={param: "SSRF"})
                        
                        # Display results in a table for visual richness
                        if isinstance(result, dict):
                            rows = [[k, str(v)[:50] + "..." if len(str(v)) > 50 else str(v)] for k, v in result.items()]
                            Logger.table(f"Exploitation Results: {args.module}", ["Key/Resource", "Value/Status"], rows)
                        elif isinstance(result, list):
                            rows = [[str(r)] for r in result]
                            Logger.table(f"Exploitation Results: {args.module}", ["Found Items"], rows)

            if args.output:
                if args.output == "json":
                    path = reporter.save_json()
                else:
                    path = reporter.save_markdown()
                Logger.success(f"Report generated successfully: [highlight]{path}[/highlight]")
    else:
        Logger.warning("No suspicious parameters found via heuristics.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[error][!][/error] Interrupted by user. Exiting...")
    except Exception as e:
        Logger.error(f"An unexpected error occurred: {e}")
        if "-v" in sys.argv:
            import traceback
            traceback.print_exc()
