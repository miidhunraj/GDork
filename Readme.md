# GDork — Google Dork Automation Tool

<div align="center">

```
 ██████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗
██╔════╝ ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝
██║  ███╗██║  ██║██║   ██║██████╔╝█████╔╝ 
██║   ██║██║  ██║██║   ██║██╔══██╗██╔═██╗ 
╚██████╔╝██████╔╝╚██████╔╝██║  ██║██║  ██╗
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
```

**A powerful Google Dork automation tool for security researchers and ethical hackers.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Ethics](https://img.shields.io/badge/Use-Ethical%20Only-red?style=flat-square)

</div>

---

> ⚠️ **For educational and ethical security research only. Only use on systems you own or have written permission to test. Unauthorised scanning may be illegal in your jurisdiction.**

---

## 📖 Table of Contents

- [What is GDork?](#-what-is-gdork)
- [Features](#-features)
- [Dork Categories](#-dork-categories)
- [Installation](#-installation)
- [Usage](#-usage)
- [Demo Walkthrough](#-demo-walkthrough)
- [Output Formats](#-output-formats)
- [Google Dork Operators](#-google-dork-operators)
- [Pro Tips](#-pro-tips)
- [Legal Disclaimer](#-legal-disclaimer)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 What is GDork?

**GDork** is a Python-based command-line tool that automates Google dorking — the technique of using advanced Google search operators to find exposed files, misconfigured services, login panels, sensitive documents, and vulnerable systems that are publicly indexed by Google.

Security researchers use Google dorks during the **reconnaissance phase** of a penetration test to discover:

- Exposed configuration files with credentials
- Open directory listings containing sensitive data
- Admin and login panels that shouldn't be public
- Misconfigured cloud storage buckets
- Vulnerable or outdated web technologies

GDork automates this process with **80+ pre-built dorks** across 6 categories, a live progress tracker, random user-agent rotation, configurable delays to avoid rate limiting, and JSON/TXT export.

---

## ✨ Features

| Feature | Description |
|---|---|
| **80+ Built-in Dorks** | Pre-loaded across 6 security categories |
| **Custom Dork Builder** | Write and run your own Google dork queries |
| **Target Locking** | Prefix all dorks with `site:target.com` automatically |
| **Smart Rate Limiting** | Configurable delay + random jitter between requests |
| **User-Agent Rotation** | Rotates 4 real browser User-Agent strings |
| **Live Progress Bar** | Real-time scan progress with per-dork results |
| **Sub-selection** | Choose specific dorks from a category to run |
| **Export Results** | Save findings to JSON or plain text |
| **Ethical Gate** | Forces ethical use agreement before scanning |
| **Rich Terminal UI** | Coloured tables, panels, and spinners via `rich` |
| **Loop Mode** | Run multiple scans in a single session |

---

## 📂 Dork Categories

### `1` — Exposed Files & Directories (15 dorks)
Find open directory listings, exposed `.git` repos, `.env` files, SQL dumps, SSH private keys, AWS credential directories, and server config files.

```
intitle:"index of" "parent directory"
filetype:env "DB_PASSWORD"
filetype:sql "INSERT INTO"
filetype:pem "PRIVATE KEY"
intitle:"index of" "id_rsa"
```

### `2` — Login Pages & Admin Panels (15 dorks)
Discover admin panels, phpMyAdmin, cPanel, WordPress login pages, Joomla admin, Apache Tomcat managers, Cisco and Fortinet device logins.

```
inurl:admin intitle:login
inurl:wp-admin intitle:"WordPress"
inurl:phpmyadmin intitle:"phpMyAdmin"
inurl:":8080/manager" intitle:"Tomcat"
intitle:"Plesk" inurl:login
```

### `3` — Sensitive Documents (10 dorks)
Find salary spreadsheets, internal documents, CSV credential files, PDFs containing API keys, SSN documents, and confidential government PDFs.

```
filetype:xlsx "salary" OR "payroll"
filetype:csv "email" "password"
filetype:pdf "api_key" OR "apikey"
filetype:xls "username" "password"
```

### `4` — Vulnerable Systems & Technologies (15 dorks)
Detect exposed `phpinfo()`, MySQL error disclosures, PHP fatal errors, exposed `.svn` repos, default server pages, Spring Boot actuator endpoints, and potential SQL injection parameters.

```
intitle:"phpinfo()" "PHP Version"
intext:"Warning: mysql_connect()"
inurl:"actuator/env" intext:"propertySources"
inurl:".git/config" "url ="
```

### `5` — Network Devices & IoT (15 dorks)
Find exposed Jupyter notebooks, Grafana dashboards, Kibana, Jenkins CI, Elasticsearch, Redis, MongoDB, Docker registries, Hadoop, RabbitMQ, and IP cameras.

```
inurl:":8888" intitle:jupyter
intitle:"Grafana" inurl:3000
inurl:":9200" intitle:elasticsearch
inurl:":8080" intitle:"Jenkins"
```

### `6` — Cloud & API Exposure (10 dorks)
Discover public S3 buckets, Azure blobs, GCS buckets, Firebase misconfigurations, exposed Swagger API docs, AWS access keys, and API keys leaked on Pastebin.

```
site:s3.amazonaws.com "index"
site:blob.core.windows.net
"AKIA" filetype:txt
inurl:swagger.json OR inurl:swagger.yaml
```

### `7` — Custom Dork Builder
Write your own dork queries with an interactive prompt. Built-in operator reference guide included.

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/gdork.git
cd gdork
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4 rich
```

### requirements.txt

```
requests>=2.28.0
beautifulsoup4>=4.11.0
rich>=13.0.0
```

---

## 🚀 Usage

### Basic run

```bash
python3 gdork.py
```

### First launch flow

```
1. Agree to the ethical use terms
2. Enter a target domain (optional — leave blank for global search)
3. Set delay between requests (default: 3.0 seconds)
4. Set number of results per dork (default: 5)
5. Choose a dork category (1–7)
6. Choose to run all dorks or select specific ones
7. View results live in the terminal
8. Export to JSON or TXT
```

### Example session

```
Target domain: example.com          ← locks all dorks to site:example.com
Delay: 3.0                          ← 3 seconds between requests
Results per dork: 5                 ← 5 Google results per dork
Category: 1                         ← Exposed Files & Directories
Run all dorks? Yes
```

### Scan output example

```
  ✔ Open directory listing       — 3 results
  ✔ Exposed .env files           — 1 results
  ✗ Exposed SQL dumps            — 0 results
  ✔ Exposed private keys         — 2 results

Scan complete. 6 total results from 15 dork(s)
```

---

## 📺 Demo Walkthrough

```
┌─────────────────────────────────────────────────────┐
│  ⚠  ETHICAL USE AGREEMENT                          │
│                                                     │
│  This tool is for security research, CTF            │
│  challenges, and testing systems you own or         │
│  have written permission to test.                   │
│                                                     │
│  By continuing you confirm you have permission      │
│  to test the target.                                │
└─────────────────────────────────────────────────────┘

I agree to use this ethically [y/n]: y

Target domain (leave blank for global): testphp.vulnweb.com
  ✔ Target locked: testphp.vulnweb.com

Delay between requests: 3.0
Results per dork [1-10]: 5

Select dork category:
 ┌───┬──────────────────────────────────┬───────┐
 │ 1 │ 📂  Exposed Files & Directories  │  15   │
 │ 2 │ 🔑  Login Pages & Admin Panels   │  15   │
 │ 3 │ 📄  Sensitive Documents          │  10   │
 │ 4 │ ⚠️   Vulnerable Systems           │  15   │
 │ 5 │ 🌐  Network Devices & IoT        │  15   │
 │ 6 │ ☁️   Cloud & API Exposure         │  10   │
 │ 7 │ 🛠️   Custom Dork Builder          │   ∞   │
 └───┴──────────────────────────────────┴───────┘

▶ Starting scan — 15 dork(s) · delay=3.0s · 5 results each

  ✔ Open directory listing       — 4 results
  ✔ Exposed .git directories     — 1 results
  ...

Save results? [y/n]: y
Format [json/txt]: json
  ✔ Results saved → gdork_results_20240318_142035.json
```

---

## 📤 Output Formats

### JSON output (`gdork_results_TIMESTAMP.json`)

```json
[
  {
    "dork": "intitle:\"index of\" \"parent directory\"",
    "description": "Open directory listing",
    "category": "Exposed Files & Directories",
    "url": "http://example.com/backup/",
    "title": "Index of /backup",
    "snippet": "Parent Directory  -  database.sql  config.bak",
    "time": "14:20:35"
  }
]
```

### TXT output (`gdork_results_TIMESTAMP.txt`)

```
[Exposed Files & Directories] Open directory listing
Dork:    intitle:"index of" "parent directory"
URL:     http://example.com/backup/
Title:   Index of /backup
Snippet: Parent Directory  -  database.sql  config.bak
------------------------------------------------------------
```

---

## 🔧 Google Dork Operators

| Operator | Description | Example |
|---|---|---|
| `site:` | Restrict to a domain | `site:example.com` |
| `inurl:` | URL must contain term | `inurl:admin` |
| `intitle:` | Page title contains term | `intitle:"index of"` |
| `filetype:` | Filter by file extension | `filetype:sql` |
| `intext:` | Body text contains term | `intext:"DB_PASSWORD"` |
| `cache:` | Google's cached version | `cache:example.com` |
| `"..."` | Exact phrase match | `"index of /backup"` |
| `-term` | Exclude a term | `-inurl:https` |
| `OR` | Match either term | `admin OR login` |
| `*` | Wildcard any word | `"password * admin"` |

---

## 💡 Pro Tips

1. **Avoid rate limiting** — Use delay ≥ 3 seconds. Google returns HTTP 429 on fast requests. Increase to 5–10 seconds for large scans.

2. **Use a VPN** — Google tracks IPs. Run behind a VPN or Tor to rotate your exit node between scans.

3. **Start targeted** — Always provide a target domain for security research. Global searches return too much noise.

4. **Combine with other tools** — Use results with Shodan (probe open ports), Nuclei (vulnerability templates), or ffuf (endpoint fuzzing).

5. **Verify before reporting** — Google indexes historical snapshots. Always verify a finding is live before reporting it as a vulnerability.

6. **Custom dorks** — Use category 7 to build targeted dorks. Combine operators for precision:
   ```
   site:target.com filetype:env "DB_PASSWORD"
   site:target.com inurl:admin -inurl:https
   ```

7. **Check GHDB** — The Exploit-DB Google Hacking Database (ghdb) has 7000+ community dorks. Use them in custom mode.

---

## 📁 Project Structure

```
gdork/
├── gdork.py              ← Main tool
├── gdork_reference.html  ← Interactive dork reference (open in browser)
├── requirements.txt      ← Python dependencies
├── README.md             ← This file
└── results/              ← Scan output directory (auto-created)
    ├── gdork_results_*.json
    └── gdork_results_*.txt
```

---

## 🤝 Contributing

Contributions are welcome! Here are some ways to improve GDork:

- Add more dork categories (e.g. healthcare, finance, industrial)
- Add Bing and DuckDuckGo search engine support
- Add proxy/Tor rotation support
- Add Shodan integration for found IPs
- Add automatic screenshot capture of results
- Add HTML report generation
- Add GitHub Actions CI/CD

### How to contribute

```bash
# Fork the repo
git clone https://github.com/yourusername/gdork.git
cd gdork

# Create a feature branch
git checkout -b feature/my-new-feature

# Make your changes and commit
git add .
git commit -m "feat: add DuckDuckGo search engine support"

# Push and open a pull request
git push origin feature/my-new-feature
```

---

## ⚖️ Legal Disclaimer

> This tool is intended **strictly** for:
> - Security research on systems you own
> - CTF (Capture The Flag) challenges
> - Penetration testing with **written permission** from the target
> - Bug bounty programs within their defined scope
> - Educational and academic research
>
> **Unauthorised use of this tool against systems you do not own or have explicit permission to test may violate the Computer Fraud and Abuse Act (CFAA), the Computer Misuse Act (UK), the IT Act (India), and equivalent laws in your country.**
>
> The author assumes no liability for misuse of this tool. Use responsibly.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🌟 Star History

If GDork helped you in your security research, consider giving it a ⭐ on GitHub!

---

<div align="center">

**Made for ethical hackers, security researchers, and CTF players.**

`stay ethical · stay legal · hack the planet`

</div>
