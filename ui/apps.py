from flask import Flask, request, jsonify, send_from_directory
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
    return send_from_directory('static', 'index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    context = request.form.get('context')
    files = request.files.getlist('screenshots')
    print(context)
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

    return jsonify({
        'message': 'Files uploaded successfully',
        'context': context,
        'saved_files': saved_files
    })

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set your Hugging Face token as the API key if you use embeddings
# If you don't use embeddings, leave it empty
openai.api_key = "YOUR_HUGGING_FACE_TOKEN"  # Replace with your actual token

# Set the API base URL if needed, e.g., for a local development environment
openai.api_base = "http://localhost:1337/v1"

def main():
    user_message = input("Enter your prompt: ")  # User-defined message

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],  # Use the user's input
        stream=True,  
        # If you want the response streamed
    )

    if isinstance(response, dict):
        # Not streaming
        print(response.choices[0].message.content)
    else:
        # Streaming
        for token in response:
            content = token["choices"][0]["delta"].get("content")
            if content is not None:
                print(content, end="", flush=True)

if __name__ == "__main__":
    main()



if __name__ == '__main__':
    app.run(debug=True)
