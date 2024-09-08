from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import cv2
import numpy as np
import os
from bson.objectid import ObjectId
from mongo_connection import get_mongo_client  # Import MongoDB connection
from image_processing import process_image  # Import image processing function

app = Flask(__name__)

# เปลี่ยนการกำหนดค่า UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

# เชื่อมต่อ MongoDB
client = get_mongo_client()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Upload route
@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = 'uploaded_image.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process image and get results
        result_image_path, counts = process_image(filepath, filename, app.config['UPLOAD_FOLDER'])
        
        # Determine the section with the highest count
        max_section = max(counts, key=counts.get)
        max_count = counts[max_section]
        
        # Fetch data from MongoDB based on max_section
        data_from_db = None
        if client is not None:
            db = client["Andrographolide"]
            collection = db["Andro_result"]
            try:
                # Mapping of section to specific MongoDB documents or criteria
                section_mapping = {
                    "Top": "66d817929a0fa00f548f7c86",  # Replace with actual ObjectId for each section
                    "Middle": "66d817929a0fa00f548f7c87",  # Replace with correct ObjectId
                    "Bottom": "66d817929a0fa00f548f7c88",  # Replace with correct ObjectId
                    "Footer": "66d817929a0fa00f548f7c89"   # Replace with correct ObjectId
                }
                
                # Fetch data from MongoDB using the mapped ObjectId
                section_id = section_mapping.get(max_section)
                if section_id:
                    data_from_db = collection.find_one({"_id": ObjectId(section_id)})
            except Exception as e:
                print(f"Error fetching data from MongoDB: {str(e)}")
        
        return render_template('index.html', result_image=url_for('uploaded_file', filename='result_' + filename), 
                               max_section=max_section, max_count=max_count, data_from_db=data_from_db)


# Route to serve uploaded image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
