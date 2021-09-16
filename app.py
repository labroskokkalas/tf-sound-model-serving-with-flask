from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import datetime
import model

app = Flask(__name__, template_folder='./')

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
# Make directory if uploads does not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['wav', 'aac'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('files')
        detector_result = ''
        uniq_folder_name = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
        uniq_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'],uniq_folder_name)
        if not os.path.isdir(uniq_upload_folder):
            os.mkdir(uniq_upload_folder)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(uniq_upload_folder, filename))
            else:
                detector_result = 'Error! File extensions allowed: wav,aac'  
                break                
        detector_result = model.get_prediction(uniq_upload_folder)
        return detector_result
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)