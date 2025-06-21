# 🔍 ReconX – Automated Recon Tool

![ReconX](https://img.shields.io/badge/ReconX-Automated%20Reconnaissance%20Tool-blue)
![Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

## 📌 Project Description

**ReconX** is a modular, automated reconnaissance tool built using **Python** and **Flask**, designed for cybersecurity professionals and bug bounty hunters. It supports both CLI and Web UI interfaces to conduct vital recon tasks such as:

- Subdomain Enumeration
- Live Host Detection
- Web Crawling
- Parameter Extraction
- Tech Stack Detection

> Supports flexible plugin-based architecture for easy expansion of recon modules.

---

## ⚙️ Features

- ✅ CLI-based commands for specific tasks (e.g., subdomains, crawling)
- ✅ Fast and parallelized recon operations
- ✅ Web-based UI built with Flask
- ✅ Extendable module system
- ✅ API integration (Shodan, Censys, etc.)
- ✅ Clean and readable terminal outputs

---

## 🚀 Installation

### ✅ Prerequisites

- Python 3.10+
- Git
- `pip`, `venv`

### 📦 Setup Steps

```bash
# Clone the repo
git clone https://github.com/tanveer2417/reconx-.git
cd reconx-

# Create virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install .
pip install -r requirements.txt
