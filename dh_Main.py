from flask import Flask, jsonify, request, g, send_from_directory
import logging
from collections import defaultdict
import time
from dh_plugins.dh_OCRProcessorMutifile import dh_OCRProcessorMutifile
from dh_plugins.dh_QRProcessor import dh_QRProcessor

import tempfile
from PIL import Image
import io
import os

app = Flask(__name__, static_folder='ui-project/dist', static_url_path='')

# Configure logging
logging.basicConfig(filename='api.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

 #flask-cors
from flask_cors import CORS

CORS(app)
# Initialize counters for statistics
stats = defaultdict(lambda: {'success': 0, 'failure': 0})

@app.before_request
def before_request():
    g.start_time = time.time()
    g.client_ip = request.remote_addr

@app.after_request
def after_request(response):
    processing_time = time.time() - g.start_time
    logging.info(f'{request.method} {request.path} from {g.client_ip} processed in {processing_time:.4f} seconds')
    return response

@app.route('/api', methods=['GET'])
def get_data():
    try:
        data = {"message": "Hello, World!"}
        stats[request.path]['success'] += 1
        logging.info(f'GET {request.path} success')
        return jsonify(data)
    except Exception as e:
        stats[request.path]['failure'] += 1
        logging.error(f'GET {request.path} failure: {e}')
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api', methods=['POST'])
def post_data():
    try:
        data = request.get_json()
        response = {"received_data": data}
        stats[request.path]['success'] += 1
        logging.info(f'POST {request.path} success')
        return jsonify(response), 201
    except Exception as e:
        stats[request.path]['failure'] += 1
        logging.error(f'POST {request.path} failure: {e}')
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(stats)

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Add any specific checks for your services here
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

        # Reduce file size
        if file_type in ['jpg', 'jpeg', 'png']:
            image = Image.open(io.BytesIO(file_bytes))
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=50)
            file_bytes = output.getvalue()
        elif file_type in ['pdf']:
            # Implement PDF compression logic here if needed
            pass

        ocr_processor = dh_OCRProcessorMutifile(use_gpu=False, vietocr_model="vgg_seq2seq")
        text = ocr_processor.process_image(file_bytes, file_type)
        
        stats[request.path]['success'] += 1
        logging.info(f'POST {request.path} success')
        return jsonify({"text": text}), 200
    except Exception as e:
        stats[request.path]['failure'] += 1
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
    app.run(host='0.0.0.0', port=5000, debug=True)