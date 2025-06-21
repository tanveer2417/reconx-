import os
from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import Wordlist
from validators import sanitize_input
import logging

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'list', 'wordlist'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/wordlists')
@login_required
def wordlists():
    """Display user's wordlists"""
    user_wordlists = Wordlist.query.filter_by(user_id=current_user.id, is_active=True)\
                                  .order_by(Wordlist.created_at.desc()).all()
    
    # Group by type
    subdomain_wordlists = [w for w in user_wordlists if w.wordlist_type == 'subdomain']
    directory_wordlists = [w for w in user_wordlists if w.wordlist_type == 'directory']
    
    return render_template('wordlists/index.html', 
                         subdomain_wordlists=subdomain_wordlists,
                         directory_wordlists=directory_wordlists)

@app.route('/wordlists/upload', methods=['GET', 'POST'])
@login_required
def upload_wordlist():
    """Upload a new wordlist"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'wordlist_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['wordlist_file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        # Get form data
        wordlist_name = sanitize_input(request.form.get('name', '').strip())
        wordlist_type = request.form.get('type', 'subdomain')
        
        if not wordlist_name:
            flash('Wordlist name is required', 'error')
            return redirect(request.url)
        
        if wordlist_type not in ['subdomain', 'directory']:
            flash('Invalid wordlist type', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Read file content
                content = file.read().decode('utf-8')
                words = [line.strip() for line in content.splitlines() if line.strip()]
                
                if not words:
                    flash('Wordlist file is empty or invalid', 'error')
                    return redirect(request.url)
                
                if len(words) > 10000:
                    flash('Wordlist too large. Maximum 10,000 words allowed.', 'error')
                    return redirect(request.url)
                
                # Check if wordlist name already exists for this user
                existing = Wordlist.query.filter_by(
                    user_id=current_user.id,
                    name=wordlist_name,
                    wordlist_type=wordlist_type,
                    is_active=True
                ).first()
                
                if existing:
                    flash('A wordlist with this name and type already exists', 'error')
                    return redirect(request.url)
                
                # Create wordlist record
                wordlist = Wordlist(
                    user_id=current_user.id,
                    name=wordlist_name,
                    wordlist_type=wordlist_type,
                    filename=secure_filename(file.filename),
                    content='\n'.join(words),
                    word_count=len(words)
                )
                
                db.session.add(wordlist)
                db.session.commit()
                
                flash(f'Wordlist "{wordlist_name}" uploaded successfully with {len(words)} words', 'success')
                return redirect(url_for('wordlists'))
                
            except UnicodeDecodeError:
                flash('Invalid file encoding. Please use UTF-8 text files.', 'error')
            except Exception as e:
                logging.error(f"Wordlist upload error: {str(e)}")
                flash('Error uploading wordlist. Please try again.', 'error')
        else:
            flash('Invalid file type. Please upload .txt, .list, or .wordlist files.', 'error')
    
    return render_template('wordlists/upload.html')

@app.route('/wordlists/<int:wordlist_id>/download')
@login_required
def download_wordlist(wordlist_id):
    """Download a wordlist"""
    wordlist = Wordlist.query.filter_by(id=wordlist_id, user_id=current_user.id, is_active=True).first_or_404()
    
    try:
        # Create temporary file
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write(wordlist.content)
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f"{wordlist.name}_{wordlist.wordlist_type}.txt",
            mimetype='text/plain'
        )
    except Exception as e:
        logging.error(f"Wordlist download error: {str(e)}")
        flash('Error downloading wordlist', 'error')
        return redirect(url_for('wordlists'))

@app.route('/wordlists/<int:wordlist_id>/delete', methods=['POST'])
@login_required
def delete_wordlist(wordlist_id):
    """Delete a wordlist"""
    wordlist = Wordlist.query.filter_by(id=wordlist_id, user_id=current_user.id, is_active=True).first_or_404()
    
    try:
        wordlist.is_active = False
        db.session.commit()
        flash(f'Wordlist "{wordlist.name}" deleted successfully', 'success')
    except Exception as e:
        logging.error(f"Wordlist deletion error: {str(e)}")
        flash('Error deleting wordlist', 'error')
    
    return redirect(url_for('wordlists'))

@app.route('/wordlists/<int:wordlist_id>/view')
@login_required
def view_wordlist(wordlist_id):
    """View wordlist details"""
    wordlist = Wordlist.query.filter_by(id=wordlist_id, user_id=current_user.id, is_active=True).first_or_404()
    
    # Get first 100 words for preview
    words = wordlist.content.splitlines()
    preview_words = words[:100]
    
    return render_template('wordlists/view.html', 
                         wordlist=wordlist, 
                         preview_words=preview_words,
                         total_words=len(words))