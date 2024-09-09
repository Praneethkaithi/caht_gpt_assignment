from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Load CLIP model and processor
model_name = "openai/clip-vit-base-patch16"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_screenshot(screenshot_path, text_context=None):
    # Load screenshot image
    image = Image.open(screenshot_path)
    
    # Process image and text context for CLIP model
    inputs = processor(text=text_context, images=image, return_tensors="pt", padding=True)
    
    # Get the model's outputs
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Process and return the output
    logits_per_image = outputs.logits_per_image
    result = logits_per_image.argmax().item()  # Modify according to your specific use case
    return result

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    context = request.form.get('context')
    files = request.files.getlist('screenshots')  # Getting multiple files
    
    if len(files) == 0:
        return jsonify({'error': 'No screenshots uploaded'}), 400

    processed_results = []
    saved_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            unique_id = uuid.uuid4().hex
            filename = secure_filename(file.filename)
            filename_with_id = f"{unique_id}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_id)
            file.save(file_path)
            saved_files.append(filename_with_id)
            
            # Process screenshot using the CLIP model
            result = process_screenshot(file_path, context)
            processed_results.append(result)
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    return jsonify({
        'message': 'Files uploaded and processed successfully',
        'context': context,
        'saved_files': saved_files,
        'processed_results': processed_results  # Return results from the CLIP model
    })

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    app.run(debug=True)
