from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid
import openai

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('ai-testing-tool.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    context = request.form.get('context')
    files = request.files.getlist('screenshots')
    print("Context:", context)
    
    if len(files) == 0:
        return jsonify({'error': 'No screenshots uploaded'}), 400
    
    saved_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            unique_id = uuid.uuid4().hex
            filename = secure_filename(file.filename)
            filename_with_id = f"{unique_id}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_id)
            file.save(file_path)
            saved_files.append(filename_with_id)
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    
    # Query the server with the context
    result = query_server_with_context(context)
    
    return redirect(url_for('result', context=context, result=result, files=','.join(saved_files)))

def query_server_with_context(context):
    openai.api_key = "YOUR_HUGGING_FACE_TOKEN"  # Replace with your actual token
    openai.api_base = "http://localhost:1337/v1"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": context}],
            stream=False  # Changed to False for simplicity
        )
        
        # Extract the content from the response
        result = response.choices[0].message.content
        return result
    
    except Exception as e:
        return str(e)

@app.route('/result')
def result():
    context = request.args.get('context', '')
    result = request.args.get('result', '')
    files = request.args.get('files', '').split(',')
    return render_template('result.html', context=context, result=result, files=files)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    app.run(debug=True)
