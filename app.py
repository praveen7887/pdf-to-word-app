from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    pdf = request.files['pdf']
    filename = secure_filename(pdf.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf.save(pdf_path)

    word_filename = filename.rsplit('.', 1)[0] + '.docx'
    word_path = os.path.join(OUTPUT_FOLDER, word_filename)

    cv = Converter(pdf_path)
    cv.convert(word_path, start=0, end=None)
    cv.close()

    return send_file(word_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
