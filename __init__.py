from flask import *
import os
from google.cloud import vision
from werkzeug.utils import secure_filename
import io

UPLOAD_FOLDER = '/Library/Webserver/Documents/teste/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
vision_client = vision.Client()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key ='yD%9ksGTCPkquBcq!tyGKh2Ebro'


@app.route('/')
def index():
	return "Hello World"

@app.route('/register')
def register():
	return "Register here."

@app.route('/home', methods = ['POST', 'GET'])
def home():
	if request.method == "POST":
		if 'file' not in request.files :
			print('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			with io.open(file_name, 'rb') as image_file:
				content = image_file.read()
				image = vision_client.image(content=content)
				landmarks = image.detect_landmarks()
				print "4"
				logos = image.detect_logos()
				print "5"
				labels = image.detect_labels()
				print "6"
				faces = image.detect_faces()
				print "7"
				a=[]
				for i in landmarks:
					a.append(i.description)
				op = {"landmarks":a}
				return json.dumps(op)
	else:
		return render_template('index.html')
if __name__=='__main__':
	app.run(debug=True)