from flask import Flask, request, render_template, redirect, flash, url_for
import json
import pybedtools
import tempfile
import os
from werkzeug.utils import secure_filename
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.secret_key = os.urandom(24)  # Required for flashing messages
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'bed'}

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_database() -> List[Dict[str, Any]]:
    """Load and validate database metadata"""
    try:
        with open('database/processed/metadata.json') as f:
            database = json.load(f)
        if not isinstance(database, list):
            raise ValueError("Database must be a list of entries")
        return database
    except Exception as e:
        logger.error(f"Error loading database: {str(e)}")
        raise

DATABASE = load_database()

def calculate_jaccard(user_bed: pybedtools.BedTool, db_entry: Dict[str, Any]) -> float:
    """Calculate Jaccard index between two BED files"""
    try:
        db_bed = pybedtools.BedTool(db_entry['processed_path'])
        intersection = user_bed.intersect(db_bed, sorted=True)
        intersection_length = sum(i.length for i in intersection)
        
        user_total_length = sum(i.length for i in user_bed)
        union_length = user_total_length + db_entry['total_length'] - intersection_length
        
        return intersection_length / union_length if union_length != 0 else 0
    except Exception as e:
        logger.error(f"Error calculating Jaccard index: {str(e)}")
        return 0.0

@app.route('/', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a BED file.', 'error')
        return redirect(request.url)
    
    try:
        # Save and process uploaded file
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        user_bed = pybedtools.BedTool(temp_path).sort().merge()
        user_total_length = sum(interval.length for interval in user_bed)
        
        # Calculate similarity with all database entries
        results = []
        for db_entry in DATABASE:
            jaccard = calculate_jaccard(user_bed, db_entry)
            results.append({
                'filename': db_entry['filename'],
                'jaccard': round(jaccard, 4),
                'description': db_entry.get('description', 'No description available')
            })
        
        # Get top N results
        n = min(int(request.form.get('top_n', 5)), len(results))
        sorted_results = sorted(results, key=lambda x: x['jaccard'], reverse=True)[:n]
        
        return render_template('results.html', 
                             results=sorted_results,
                             user_length=user_total_length,
                             filename=filename)
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        flash('Error processing file. Please ensure it is a valid BED file.', 'error')
        return redirect(request.url)
    
    finally:
        # Clean up temporary file
        if 'temp_path' in locals():
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.error(f"Error removing temporary file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)