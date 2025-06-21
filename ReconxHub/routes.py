import json
import subprocess
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from models import ScanResult, Wordlist
from validators import validate_domain, sanitize_input
import logging

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/scan', methods=['GET', 'POST'])
@login_required
def scan():
    if request.method == 'POST':
        try:
            # Get and validate form data
            domain = sanitize_input(request.form.get('domain', '').strip())
            selected_modules = request.form.getlist('modules')
            subdomain_wordlist_id = request.form.get('subdomain_wordlist')
            directory_wordlist_id = request.form.get('directory_wordlist')
            
            # Validate domain
            if not validate_domain(domain):
                flash('Please enter a valid domain name.', 'error')
                return render_template('scan.html')
            
            # Validate modules
            valid_modules = ['osint', 'subdomain', 'hosts', 'web']
            selected_modules = [m for m in selected_modules if m in valid_modules]
            
            if not selected_modules:
                flash('Please select at least one scan module.', 'error')
                return render_template('scan.html')
            
            # Create scan result record
            scan_result = ScanResult()
            scan_result.user_id = current_user.id
            scan_result.domain = domain
            scan_result.modules = json.dumps(selected_modules)
            scan_result.status = 'running'
            db.session.add(scan_result)
            db.session.commit()
            
            try:
                # Execute scan with reduced timeout and custom wordlists
                results = execute_scan(domain, selected_modules, subdomain_wordlist_id, directory_wordlist_id)
                
                # Update scan result
                scan_result.results = json.dumps(results)
                scan_result.status = 'completed'
                scan_result.completed_at = datetime.utcnow()
                db.session.commit()
                
                flash('Scan completed successfully!', 'success')
                return redirect(url_for('results', scan_id=scan_result.id))
            except Exception as scan_error:
                # Update scan status to failed
                scan_result.status = 'failed'
                scan_result.results = json.dumps({'error': str(scan_error)})
                scan_result.completed_at = datetime.utcnow()
                db.session.commit()
                
                flash('Scan failed. Please try again.', 'error')
                return redirect(url_for('results', scan_id=scan_result.id))
            
        except Exception as e:
            logging.error(f"Scan error: {str(e)}")
            flash('An error occurred during the scan. Please try again.', 'error')
    
    return render_template('scan.html')

@app.route('/results/<int:scan_id>')
@login_required
def results(scan_id):
    scan_result = ScanResult.query.filter_by(id=scan_id, user_id=current_user.id).first_or_404()
    
    # Parse results if they exist
    results_data = {}
    if scan_result.results:
        try:
            results_data = json.loads(scan_result.results)
        except json.JSONDecodeError:
            results_data = {'error': 'Failed to parse scan results'}
    
    return render_template('results.html', scan_result=scan_result, results=results_data)

def execute_scan(domain, modules, subdomain_wordlist_id=None, directory_wordlist_id=None):
    """Execute the ReconX CLI tool with selected modules and custom wordlists"""
    results = {}
    
    # Get the current working directory
    import os
    current_dir = os.getcwd()
    
    # Get custom wordlists if specified
    custom_wordlists = {}
    if subdomain_wordlist_id:
        subdomain_wordlist = Wordlist.query.filter_by(
            id=subdomain_wordlist_id, 
            user_id=current_user.id, 
            wordlist_type='subdomain',
            is_active=True
        ).first()
        if subdomain_wordlist:
            custom_wordlists['subdomain'] = subdomain_wordlist.content
    
    if directory_wordlist_id:
        directory_wordlist = Wordlist.query.filter_by(
            id=directory_wordlist_id, 
            user_id=current_user.id, 
            wordlist_type='directory',
            is_active=True
        ).first()
        if directory_wordlist:
            custom_wordlists['directory'] = directory_wordlist.content
    
    for module in modules:
        try:
            # Build command using sys.executable to get the correct Python interpreter
            import sys
            cmd = [sys.executable, 'reconx.py', module, '--domain', domain]
            
            # Execute command with reduced timeout
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,  # 1 minute timeout
                cwd=current_dir
            )
            
            if result.returncode == 0:
                results[module] = {
                    'status': 'success',
                    'output': result.stdout,
                    'error': result.stderr if result.stderr else None
                }
            else:
                # Even if there's an error, show the output for debugging
                results[module] = {
                    'status': 'error',
                    'output': result.stdout if result.stdout else 'No output',
                    'error': result.stderr if result.stderr else 'Unknown error'
                }
                
        except subprocess.TimeoutExpired:
            results[module] = {
                'status': 'timeout',
                'output': '',
                'error': 'Command timed out after 1 minute'
            }
        except Exception as e:
            results[module] = {
                'status': 'error',
                'output': '',
                'error': f'Execution error: {str(e)}'
            }
    
    return results

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
