# ReconX - Automated Recon Tool

A comprehensive web-based reconnaissance tool for domain enumeration and OSINT gathering. ReconX provides an intuitive web interface for running various reconnaissance modules including subdomain enumeration, OSINT collection, live host detection, and web reconnaissance.

## Features

- **OSINT Module**: Performs WHOIS lookups, certificate transparency checks, and gathers open-source intelligence
- **Subdomain Enumeration**: Discovers subdomains using certificate transparency, DNS enumeration, and brute-force techniques
- **Live Hosts Detection**: Checks DNS resolution and HTTP availability to identify active hosts
- **Web Reconnaissance**: Analyzes web technologies, extracts forms and links, and discovers directories

## Quick Start

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements-deploy.txt
   ```
3. Set environment variable:
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. Open your browser to `http://localhost:5000`

### Deploy to Render

#### Option 1: Using render.yaml (Recommended)
1. Fork this repository to your GitHub account
2. Connect your GitHub repository to Render
3. Create a new Web Service and select your repository
4. Render will automatically detect the `render.yaml` file and configure the deployment
5. The application will be available at your assigned Render URL

#### Option 2: Manual Configuration
1. Fork this repository to your GitHub account
2. Create a new Web Service on Render
3. Connect your repository
4. Configure the following settings:
   - **Build Command**: `pip install -r requirements-deploy.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
   - **Environment Variables**: 
     - `SESSION_SECRET`: Generate a random secret key
5. Deploy the service

## Usage

1. Navigate to the web interface
2. Click "Start Scanning"
3. Enter a target domain (e.g., `example.com`)
4. Select one or more reconnaissance modules
5. Click "Start Scan" to begin reconnaissance
6. View detailed results with formatted CLI output

## Security Notice

This tool is intended for authorized security testing and research purposes only. Always ensure you have proper permission before scanning any domain or network. Unauthorized scanning may violate terms of service or local laws.

## Project Structure

```
reconx-automated-recon-tool/
├── app.py                 # Flask application setup
├── main.py               # Application entry point
├── routes.py             # Web routes and scan execution
├── validators.py         # Input validation and sanitization
├── reconx.py            # CLI reconnaissance tool
├── modules/             # Reconnaissance modules
│   ├── osint.py         # OSINT intelligence gathering
│   ├── subdomain.py     # Subdomain enumeration
│   ├── hosts.py         # Live host detection
│   └── web.py           # Web reconnaissance
├── templates/           # HTML templates
├── static/              # CSS and static assets
├── requirements-deploy.txt  # Production dependencies
├── Procfile            # Process file for deployment
├── render.yaml         # Render deployment configuration
└── README.md           # This file
```

## Dependencies

- Flask - Web framework
- Gunicorn - WSGI HTTP Server
- Requests - HTTP library for reconnaissance modules
- Werkzeug - WSGI utilities

## License

Use responsibly and only on authorized targets.