#!/usr/bin/env python3
"""
GDork — Google Dork Automation Tool
====================================
Ethical use only. Use only on systems you own or have written permission to test.
Run:  python3 gdork.py
Deps: pip install requests beautifulsoup4 rich
"""

import time
import json
import random
import urllib.parse
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.syntax import Syntax
    from rich import box
    from rich.text import Text
    from rich.columns import Columns
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("[!] Missing dependencies. Run: pip install requests beautifulsoup4 rich")
    exit(1)

console = Console()

# ─── Dork Categories ──────────────────────────────────────────────────────────

DORK_CATEGORIES = {
    "1": {
        "name": "Exposed Files & Directories",
        "color": "red",
        "icon": "📂",
        "dorks": [
            ('intitle:"index of" "parent directory"',         "Open directory listing"),
            ('intitle:"index of" passwd',                     "Exposed passwd files"),
            ('intitle:"index of" ".git"',                     "Exposed .git directories"),
            ('intitle:"index of" "wp-config.php"',            "WordPress config exposed"),
            ('filetype:env "DB_PASSWORD"',                    "Exposed .env files"),
            ('filetype:sql "INSERT INTO"',                    "Exposed SQL dumps"),
            ('filetype:log "error" inurl:log',                "Exposed log files"),
            ('filetype:bak inurl:backup',                     "Backup files"),
            ('filetype:conf inurl:nginx OR inurl:apache',     "Server config files"),
            ('filetype:pem "PRIVATE KEY"',                    "Exposed private keys"),
            ('filetype:xml "connectionString"',               "DB connection strings in XML"),
            ('intitle:"index of" "id_rsa"',                   "SSH private keys"),
            ('filetype:yml "password:" OR "secret:"',         "Secrets in YAML files"),
            ('intitle:"index of" ".aws"',                     "AWS credential directories"),
            ('filetype:txt "password"',                       "Passwords in text files"),
        ]
    },
    "2": {
        "name": "Login Pages & Admin Panels",
        "color": "yellow",
        "icon": "🔑",
        "dorks": [
            ('inurl:admin intitle:login',                     "Generic admin login"),
            ('inurl:wp-admin intitle:"WordPress"',            "WordPress admin panel"),
            ('inurl:phpmyadmin intitle:"phpMyAdmin"',         "phpMyAdmin panel"),
            ('inurl:"/admin/login"',                          "Admin login endpoint"),
            ('inurl:controlpanel intitle:login',              "Control panel login"),
            ('intitle:"Plesk" inurl:login',                   "Plesk hosting panel"),
            ('intitle:"cPanel" inurl:2083',                   "cPanel login"),
            ('inurl:webmail intitle:login',                   "Webmail login"),
            ('intitle:"Cisco" inurl:login.html',              "Cisco device login"),
            ('intitle:"Fortinet" inurl:logincheck',           "Fortinet VPN login"),
            ('inurl:"/wp-login.php"',                         "WordPress login page"),
            ('intitle:"Joomla" inurl:administrator',          "Joomla admin panel"),
            ('inurl:":8080/manager" intitle:"Tomcat"',        "Apache Tomcat manager"),
            ('inurl:"/panel" intitle:login',                  "Generic panel login"),
            ('inurl:"/user/login" intitle:login',             "User login pages"),
        ]
    },
    "3": {
        "name": "Sensitive Documents",
        "color": "magenta",
        "icon": "📄",
        "dorks": [
            ('filetype:pdf "confidential" site:.gov',         "Confidential govt PDFs"),
            ('filetype:xlsx "salary" OR "payroll"',           "Salary spreadsheets"),
            ('filetype:docx "internal use only"',             "Internal documents"),
            ('filetype:pdf "password" "username"',            "PDFs with credentials"),
            ('filetype:csv "email" "password"',               "CSV credential files"),
            ('filetype:pdf inurl:report "quarterly"',         "Quarterly reports"),
            ('filetype:xls "username" "password"',            "Excel credential files"),
            ('filetype:doc "ssn" OR "social security"',       "SSN documents"),
            ('filetype:pdf "api_key" OR "apikey"',            "API keys in PDFs"),
            ('filetype:txt inurl:password',                   "Password text files"),
        ]
    },
    "4": {
        "name": "Vulnerable Systems & Technologies",
        "color": "red",
        "icon": "⚠️",
        "dorks": [
            ('inurl:".php?id=" intext:"mysql_fetch"',         "Potential SQLi (PHP)"),
            ('inurl:"search.php?q="',                         "Search param (XSS test)"),
            ('inurl:".asp?id="',                              "ASP param injection"),
            ('intitle:"phpinfo()" "PHP Version"',             "Exposed phpinfo()"),
            ('inurl:"/cgi-bin/" filetype:cgi',                "Exposed CGI scripts"),
            ('intitle:"test page" inurl:test.php',            "Test pages left online"),
            ('inurl:"/.svn/entries"',                         "Exposed SVN repos"),
            ('intitle:"Welcome to IIS" inurl:iis',            "Default IIS pages"),
            ('intitle:"Apache2 Ubuntu Default Page"',         "Default Apache pages"),
            ('inurl:"wp-content/uploads" filetype:php',       "PHP shells in WP uploads"),
            ('inurl:"config.php" filetype:php',               "Exposed PHP configs"),
            ('intext:"Warning: mysql_connect()"',             "MySQL connection errors"),
            ('intext:"Fatal error" "on line" filetype:php',   "PHP error disclosure"),
            ('inurl:".git/config" "url ="',                   "Exposed git config"),
            ('inurl:"actuator/env" intext:"propertySources"', "Spring Boot actuator"),
        ]
    },
    "5": {
        "name": "Network Devices & IoT",
        "color": "cyan",
        "icon": "🌐",
        "dorks": [
            ('intitle:"router" inurl:admin inurl:login',      "Router admin panels"),
            ('intitle:"webcamXP" inurl:8080',                 "Exposed webcams"),
            ('inurl:"/viewer/live/index.html"',               "IP camera streams"),
            ('intitle:"SCADA" inurl:login',                   "SCADA systems"),
            ('inurl:":10000" intitle:Webmin',                 "Webmin panels"),
            ('inurl:":8888" intitle:jupyter',                 "Exposed Jupyter notebooks"),
            ('intitle:"Grafana" inurl:3000',                  "Exposed Grafana dashboards"),
            ('intitle:"Kibana" inurl:5601',                   "Exposed Kibana"),
            ('intitle:"RabbitMQ" inurl:15672',                "RabbitMQ management"),
            ('inurl:":9200" intitle:elasticsearch',           "Exposed Elasticsearch"),
            ('inurl:":8080" intitle:"Jenkins"',               "Exposed Jenkins CI"),
            ('intitle:"MongoDB" inurl:27017',                 "Exposed MongoDB"),
            ('inurl:":6379" intitle:"Redis"',                 "Exposed Redis"),
            ('intitle:"Hadoop" inurl:50070',                  "Exposed Hadoop"),
            ('inurl:":5000" intitle:docker',                  "Exposed Docker registries"),
        ]
    },
    "6": {
        "name": "Cloud & API Exposure",
        "color": "blue",
        "icon": "☁️",
        "dorks": [
            ('site:s3.amazonaws.com "index"',                 "Public S3 buckets"),
            ('site:blob.core.windows.net',                    "Public Azure blobs"),
            ('site:storage.googleapis.com',                   "Public GCS buckets"),
            ('inurl:pastebin.com "api_key"',                  "API keys on Pastebin"),
            ('inurl:github.com "password" filetype:json',     "Passwords in GitHub"),
            ('site:trello.com "password"',                    "Sensitive Trello boards"),
            ('inurl:".json" "firebase.io" "rules"',           "Firebase misconfig"),
            ('"AKIA" filetype:txt',                           "AWS access keys"),
            ('inurl:swagger.json OR inurl:swagger.yaml',      "Exposed Swagger docs"),
            ('inurl:".well-known/openid-configuration"',      "OIDC endpoints"),
        ]
    },
    "7": {
        "name": "Custom Dork Builder",
        "color": "green",
        "icon": "🛠️",
        "dorks": []
    }
}

# ─── Dork Engine ──────────────────────────────────────────────────────────────

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0",
]

@dataclass
class DorkResult:
    dork:        str
    description: str
    url:         str
    title:       str
    snippet:     str
    category:    str
    timestamp:   str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))


def build_google_url(dork: str, target: Optional[str] = None, num: int = 10) -> str:
    query = dork
    if target:
        query = f"site:{target} {dork}"
    params = urllib.parse.urlencode({"q": query, "num": num, "hl": "en"})
    return f"https://www.google.com/search?{params}"


def search_dork(dork: str, description: str, category: str,
                target: Optional[str], delay: float, num: int) -> List[DorkResult]:
    results = []
    url = build_google_url(dork, target, num)
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 429:
            console.print("[yellow]  ⚠ Rate limited by Google — increase delay[/]")
            return results
        if resp.status_code != 200:
            console.print(f"[red]  ✗ HTTP {resp.status_code} for dork: {dork[:50]}[/]")
            return results

        soup = BeautifulSoup(resp.text, "html.parser")

        # Parse Google result divs
        for g in soup.select("div.g, div[data-sokoban-container]"):
            a_tag = g.find("a", href=True)
            if not a_tag:
                continue
            link = a_tag["href"]
            if not link.startswith("http"):
                continue
            title_el = g.find("h3")
            title = title_el.get_text(strip=True) if title_el else "(no title)"
            snippet_el = g.find("div", {"data-sncf": True}) or g.find("span", class_="aCOpRe")
            snippet = snippet_el.get_text(strip=True)[:200] if snippet_el else ""
            results.append(DorkResult(
                dork=dork, description=description,
                url=link, title=title, snippet=snippet, category=category
            ))
    except requests.exceptions.ConnectionError:
        console.print("[red]  ✗ Network error — are you connected to the internet?[/]")
    except Exception as e:
        console.print(f"[red]  ✗ Error: {e}[/]")

    time.sleep(delay + random.uniform(0.5, 1.5))
    return results


# ─── UI ───────────────────────────────────────────────────────────────────────

def print_banner():
    console.clear()
    banner = """
 ██████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗
██╔════╝ ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝
██║  ███╗██║  ██║██║   ██║██████╔╝█████╔╝ 
██║   ██║██║  ██║██║   ██║██╔══██╗██╔═██╗ 
╚██████╔╝██████╔╝╚██████╔╝██║  ██║██║  ██╗
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝"""
    console.print(f"[bold red]{banner}[/]")
    console.print("[bold white]         Google Dork Automation Tool[/]")
    console.print("[dim]         Ethical use only · Your own systems only[/]\n")


def print_categories():
    table = Table(box=box.ROUNDED, border_style="dim", show_header=True,
                  header_style="bold white")
    table.add_column("ID",       style="bold cyan",    width=4)
    table.add_column("Category", style="bold",         width=32)
    table.add_column("Dorks",    style="dim",          width=8)
    table.add_column("Targets",  style="dim",          width=35)

    descriptions = {
        "1": "Open dirs, .git, .env, SQL dumps, SSH keys",
        "2": "Admin panels, phpMyAdmin, cPanel, Cisco",
        "3": "PDFs, XLS, CSV with credentials / PII",
        "4": "SQLi params, phpinfo, error disclosure",
        "5": "Routers, cameras, Jupyter, Kibana, Redis",
        "6": "S3 buckets, Azure blobs, Firebase, AWS keys",
        "7": "Write your own Google dork query",
    }
    colors = {"1":"red","2":"yellow","3":"magenta","4":"red","5":"cyan","6":"blue","7":"green"}

    for cid, cat in DORK_CATEGORIES.items():
        count = str(len(cat["dorks"])) if cat["dorks"] else "∞"
        table.add_row(
            cid,
            f"[{colors[cid]}]{cat['icon']}  {cat['name']}[/]",
            count,
            descriptions[cid]
        )
    console.print(table)


def print_results_table(results: List[DorkResult]):
    if not results:
        console.print("\n[yellow]  No results found for this dork.[/]")
        return

    table = Table(box=box.SIMPLE_HEAVY, border_style="dim",
                  show_header=True, header_style="bold cyan",
                  expand=True)
    table.add_column("#",         style="dim",       width=4)
    table.add_column("Title",     style="bold white", width=30)
    table.add_column("URL",       style="cyan",       width=45)
    table.add_column("Snippet",   style="dim",        width=40)
    table.add_column("Time",      style="dim",        width=9)

    for i, r in enumerate(results, 1):
        url_short = r.url[:43] + "…" if len(r.url) > 44 else r.url
        snippet   = r.snippet[:38] + "…" if len(r.snippet) > 39 else r.snippet
        table.add_row(str(i), r.title[:28], url_short, snippet, r.timestamp)
    console.print(table)


def save_results(results: List[DorkResult], fmt: str = "json"):
    if not results:
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if fmt == "json":
        fname = f"gdork_results_{ts}.json"
        data = [
            {"dork": r.dork, "description": r.description, "category": r.category,
             "url": r.url, "title": r.title, "snippet": r.snippet, "time": r.timestamp}
            for r in results
        ]
        with open(fname, "w") as f:
            json.dump(data, f, indent=2)
    else:
        fname = f"gdork_results_{ts}.txt"
        with open(fname, "w") as f:
            for r in results:
                f.write(f"[{r.category}] {r.description}\n")
                f.write(f"Dork:    {r.dork}\n")
                f.write(f"URL:     {r.url}\n")
                f.write(f"Title:   {r.title}\n")
                f.write(f"Snippet: {r.snippet}\n")
                f.write("-" * 60 + "\n")
    console.print(f"\n[green]  ✔ Results saved → [bold]{fname}[/][/]")
    return fname


def run_dork_scan(dorks: List[tuple], category_name: str,
                  target: Optional[str], delay: float, num: int) -> List[DorkResult]:
    all_results = []

    with Progress(
        SpinnerColumn(style="red"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=30, style="red", complete_style="green"),
        TextColumn("[dim]{task.completed}/{task.total}"),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task(f"Scanning {category_name}...", total=len(dorks))
        for dork, desc in dorks:
            progress.update(task, description=f"[dim]{desc[:45]}[/]")
            results = search_dork(dork, desc, category_name, target, delay, num)
            all_results.extend(results)
            if results:
                progress.console.print(
                    f"  [green]✔[/] [white]{desc}[/] — [cyan]{len(results)} results[/]"
                )
            else:
                progress.console.print(f"  [dim]✗ {desc} — 0 results[/]")
            progress.advance(task)

    return all_results


# ─── Custom Dork Builder ──────────────────────────────────────────────────────

def custom_dork_builder() -> List[tuple]:
    console.print("\n[bold cyan]Custom Dork Builder[/]\n")
    console.print("[dim]Common operators:[/]")
    operators = [
        ("site:",        "Limit to a domain",             "site:example.com"),
        ("inurl:",       "URL must contain term",         "inurl:admin"),
        ("intitle:",     "Page title must contain",       "intitle:login"),
        ("filetype:",    "Specific file extension",       "filetype:pdf"),
        ("intext:",      "Body text must contain",        "intext:password"),
        ("cache:",       "Google's cached version",       "cache:example.com"),
        ('"..."',        "Exact phrase match",            '"confidential document"'),
        ("-term",        "Exclude a term",                "-inurl:https"),
        ("OR",           "Either term",                   "admin OR login"),
    ]
    for op, desc, example in operators:
        console.print(f"  [cyan]{op:<14}[/] [dim]{desc:<30}[/] [white]{example}[/]")

    console.print()
    dorks = []
    while True:
        dork = Prompt.ask("[bold green]Enter dork query[/] [dim](or blank to finish)[/]",
                          default="").strip()
        if not dork:
            break
        desc = Prompt.ask("[dim]Short description[/]", default="Custom dork").strip()
        dorks.append((dork, desc))
        console.print(f"[green]  ✔ Added:[/] {dork}\n")

    return dorks


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print_banner()

    # Ethical agreement
    console.print(Panel(
        "[bold yellow]⚠  ETHICAL USE AGREEMENT[/]\n\n"
        "This tool is for [bold]security research, CTF challenges, and testing systems "
        "you own or have written permission to test[/].\n\n"
        "Unauthorised scanning of third-party systems may be [bold red]illegal[/] "
        "in your jurisdiction.\n\n"
        "By continuing you confirm you have permission to test the target.",
        border_style="yellow", expand=False
    ))

    if not Confirm.ask("[bold]I agree to use this ethically", default=False):
        console.print("[red]Exiting.[/]")
        return

    console.print()

    # Target domain (optional)
    target = Prompt.ask(
        "\n[bold]Target domain[/] [dim](leave blank for global search)[/]",
        default=""
    ).strip().lstrip("https://").lstrip("http://").rstrip("/") or None

    if target:
        console.print(f"[green]  ✔ Target locked:[/] [bold cyan]{target}[/]\n")
    else:
        console.print("[yellow]  ⚠ No target — global Google search[/]\n")

    # Settings
    delay = float(Prompt.ask(
        "[bold]Delay between requests (seconds)[/] [dim]higher = safer[/]",
        default="3.0"
    ))
    num = int(Prompt.ask(
        "[bold]Results per dork[/] [dim]1-10[/]",
        default="5"
    ))

    # Category selection
    console.print("\n[bold white]Select dork category:[/]\n")
    print_categories()
    choice = Prompt.ask("\n[bold]Category ID[/]", choices=list(DORK_CATEGORIES.keys()))

    cat = DORK_CATEGORIES[choice]
    dorks_to_run = cat["dorks"] if choice != "7" else custom_dork_builder()

    if not dorks_to_run:
        console.print("[red]No dorks to run. Exiting.[/]")
        return

    # Sub-selection for large categories
    if len(dorks_to_run) > 5 and choice != "7":
        console.print(f"\n[bold]Category has {len(dorks_to_run)} dorks.[/]")
        run_all = Confirm.ask("Run all dorks?", default=True)
        if not run_all:
            console.print("\n[dim]Available dorks:[/]")
            for i, (d, desc) in enumerate(dorks_to_run, 1):
                console.print(f"  [cyan]{i:>2}.[/] [white]{desc}[/]")
                console.print(f"      [dim]{d}[/]")
            selection = Prompt.ask(
                "\nEnter dork numbers to run [dim](e.g. 1,3,5 or 1-5)[/]"
            )
            selected = []
            for part in selection.split(","):
                part = part.strip()
                if "-" in part:
                    a, b = part.split("-")
                    selected.extend(range(int(a)-1, int(b)))
                else:
                    selected.append(int(part)-1)
            dorks_to_run = [dorks_to_run[i] for i in selected if 0 <= i < len(dorks_to_run)]

    # Run
    console.print(f"\n[bold red]▶ Starting scan[/] — {len(dorks_to_run)} dork(s) · "
                  f"delay={delay}s · {num} results each\n")

    all_results = run_dork_scan(dorks_to_run, cat["name"], target, delay, num)

    # Summary
    console.print(f"\n[bold]Scan complete.[/] "
                  f"[green]{len(all_results)} total results[/] from "
                  f"[cyan]{len(dorks_to_run)} dork(s)[/]\n")

    if all_results:
        print_results_table(all_results)

        # Save
        if Confirm.ask("\n[bold]Save results?[/]", default=True):
            fmt = Prompt.ask("Format", choices=["json", "txt"], default="json")
            save_results(all_results, fmt)

    # Loop
    if Confirm.ask("\n[bold]Run another scan?[/]", default=False):
        main()
    else:
        console.print("\n[bold red]GDork[/] [dim]— stay ethical, stay legal.[/]\n")


if __name__ == "__main__":
    main()
