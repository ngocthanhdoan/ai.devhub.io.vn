import sqlite3
from flask import Flask, jsonify, request, g, send_from_directory
import logging
import time
import os
from flask_cors import CORS
from dh_plugins.dh_OCRProcessorMutifile import dh_OCRProcessorMutifile
from dh_plugins.dh_QRProcessor import dh_QRProcessor
from PIL import Image
import io
app = Flask(__name__, static_folder='ui-project/dist', static_url_path='')
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('api_history.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uri TEXT,
                method TEXT,
                status INTEGER,
                client_ip TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()


CORS(app)

logging.basicConfig(filename='api.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

@app.before_request
def before_request():
    g.start_time = time.time()
    g.client_ip = request.remote_addr

@app.after_request
def after_request(response):
    processing_time = time.time() - g.start_time
    logging.info(f'{request.method} {request.path} from {g.client_ip} processed in {processing_time:.4f} seconds')
    
    db = get_db()
    db.execute(
        'INSERT INTO history (uri, method, status, client_ip) VALUES (?, ?, ?, ?)',
        (request.path, request.method, response.status_code, g.client_ip)
    )
    db.commit()
    
    return response

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    date_filter = request.args.get('date')
    
    if date_filter:
        cursor = db.execute('''
            SELECT uri, method, 
                   SUM(CASE WHEN status < 400 THEN 1 ELSE 0 END) AS success,
                   SUM(CASE WHEN status >= 400 THEN 1 ELSE 0 END) AS failure
            FROM history
            WHERE DATE(timestamp) = ?
            GROUP BY uri, method
        ''', (date_filter,))
    else:
        cursor = db.execute('''
            SELECT uri, method, 
                   SUM(CASE WHEN status < 400 THEN 1 ELSE 0 END) AS success,
                   SUM(CASE WHEN status >= 400 THEN 1 ELSE 0 END) AS failure
            FROM history
            GROUP BY uri, method
        ''')
    
    stats = [dict(row) for row in cursor.fetchall()]
    return jsonify(stats)

@app.route('/api/history', methods=['GET'])
def get_history():
    db = get_db()
    cursor = db.execute('SELECT * FROM history ORDER BY timestamp DESC LIMIT 100')
    history = [dict(row) for row in cursor.fetchall()]
    return jsonify(history)

@app.route('/api/history/<int:history_id>', methods=['GET'])
def get_history_detail(history_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM history WHERE id = ?', (history_id,))
    row = cursor.fetchone()
    return jsonify(dict(row)) if row else jsonify({'error': 'Not found'}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logging.error(f'Health check {request.path} failure: {e}')
        return jsonify({"status": "unhealthy"}), 500

@app.route('/api/ocr', methods=['POST'])
def ocr():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        file_bytes = file.read()
        file_type = file.filename.split('.')[-1].lower()

        if file_type in ['jpg', 'jpeg', 'png']:
            image = Image.open(io.BytesIO(file_bytes))
            output = io.BytesIO()
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            image.save(output, format='JPEG', quality=50)
            file_bytes = output.getvalue()
        
        ocr_processor = dh_OCRProcessorMutifile(use_gpu=False, vietocr_model="vgg_transformer")
        text = ocr_processor.process_image(file_bytes, file_type)
        logging.info(f'POST {request.path} success')
        return jsonify({"text": text}), 200
    except Exception as e:
        logging.error(f'POST {request.path} failure: {e}')
        return jsonify({"error": "Internal Server Error"}), 500
# Serve the frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
