# 🔍 ReconX – Automated Recon Tool

![ReconX](https://img.shields.io/badge/ReconX-Automated%20Reconnaissance%20Tool-blue)
![Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

## 📌 Project Description

**ReconX** is a modular, automated reconnaissance tool built using **Python** and **Flask**, designed for cybersecurity professionals and bug bounty hunters. It supports both CLI and Web UI interfaces to conduct vital recon tasks such as:

* Subdomain Enumeration
* Live Host Detection
* Web Crawling
* Parameter Extraction
* Tech Stack Detection

> Supports flexible plugin-based architecture for easy expansion of recon modules.

---

## ⚙️ Features

* ✅ CLI-based commands for specific tasks (e.g., subdomains, crawling)
* ✅ Fast and parallelized recon operations
* ✅ Web-based UI built with Flask
* ✅ Extendable module system
* ✅ API integration (Shodan, Censys, etc.)
* ✅ Clean and readable terminal outputs

---

## 🚀 Installation

### ✅ Prerequisites

* Python 3.10+
* Git
* `pip`, `venv`

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
```

> Optionally, create a `.env` file to store your API keys:

```ini
SHODAN_API_KEY=your_key_here
CENSYS_API_ID=your_id
CENSYS_API_SECRET=your_secret
```

---

## ⚡ Usage

### 📌 CLI Mode

```bash
reconx subdomain --domain example.com
```

### 📌 Other CLI Commands (Example)

```bash
reconx livehosts --domain example.com
reconx crawl --domain example.com
reconx techdetect --domain example.com
```

### 🌐 Web UI Mode (if available)

```bash
python app.py
# Open browser at http://localhost:5000
```

---

## 📁 Project Structure

```
reconx-/
├── reconx/              # Core modules
│   ├── subdomain.py
│   ├── livehosts.py
│   ├── crawler.py
│   ├── techdetect.py
│   └── __main__.py
├── webapp/              # Flask UI
├── setup.py
├── requirements.txt
├── README.md
└── .env (optional)
```

---

## 🧪 Example Output

```bash
$ reconx subdomain --domain example.com

[+] Found 12 subdomains:
- api.example.com
- blog.example.com
- ...
```

---

## 👥 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push and open a pull request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
You're free to use, modify, and distribute this project with proper attribution.

```
MIT License

Copyright (c) 2025 Tanveer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
