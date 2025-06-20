# reconx/cli/subdomain_cli.py

import os
from reconx.core import (
    subfinder_py, amass_py, assetfinder_py, sublister_py, bruteforce_py,
    dnsx_py, web_analysis, screenshot, nuclei_scan, export
)
from colorama import Fore

def run(args):
    domain = args.domain
    wordlist = args.wordlist
    verbose = args.verbose
    output = f"{domain}_reconx_results.txt"

    def vprint(msg):
        if verbose and not args.silent:
            print(Fore.YELLOW + msg)

    print(Fore.CYAN + f"[+] Starting subdomain enumeration for {domain}\n")

    subdomains = set()

    vprint("[*] Using subfinder_py...")
    subdomains.update(subfinder_py.run(domain))

    vprint("[*] Using amass_py...")
    subdomains.update(amass_py.run(domain, silent=args.silent, verbose=args.verbose))

    vprint("[*] Using assetfinder_py...")
    subdomains.update(assetfinder_py.run(domain, silent=args.silent, verbose=args.verbose))

    vprint("[*] Using sublister_py...")
    subdomains.update(sublister_py.run(domain))

    vprint("[*] Running brute-force with wordlist...")
    subdomains.update(bruteforce_py.bruteforce(domain, wordlist, silent=args.silent, verbose=args.verbose))

    vprint("[*] Probing with dnsx_py to find live subdomains...")
    live_subs = dnsx_py.probe(subdomains, silent=args.silent, verbose=args.verbose)

    print(Fore.GREEN + f"\n[+] {len(live_subs)} live subdomains found.\n")
    for sub in live_subs:
        print(sub)

    # --- Auto-Chaining ---
    # 1. Screenshotting
    vprint("\n[*] Taking screenshots of live subdomains...")
    screenshot_paths = screenshot.capture(live_subs)

    # 2. Technology Detection
    vprint("[*] Detecting tech stack for each subdomain...")
    tech_data = web_analysis.detect(live_subs)

    # 3. Vulnerability Scan using Nuclei
    vprint("[*] Running vulnerability scan on live subdomains...")
    vuln_results = nuclei_scan.scan(live_subs)

    # 4. Export Results
    vprint(f"[*] Exporting all results to {output}")
    export.save_results(domain, live_subs, tech_data, vuln_results, screenshot_paths, output)

    print(Fore.GREEN + f"\n[\u2714] ReconX scan completed and saved to: {output}")
