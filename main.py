from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)

# Встановлення дозволених розширень файлів
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# Функція для перевірки дозволених розширень файлів
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            start_time = time.time()
            file.save(os.path.join('/шлях/до/вашого/каталогу', filename))
            end_time = time.time()
            duration = end_time - start_time
            file_size = os.path.getsize(os.path.join('/шлях/до/вашого/каталогу', filename))
            file_size_mb = file_size / (1024 * 1024)
            download_link = request.url_root + 'download/' + filename
            return f'Файл успішно завантажено!<br>Тривалість завантаження: {duration:.2f} секунд<br>Час завантаження: {time.ctime()}<br>Розмір файлу: {file_size_mb:.2f} МБ<br><a href="{download_link}">Посилання на скачування</a>'
        else:
            return 'Неприпустимий формат файлу. Дозволені розширення: txt, pdf, png, jpg, jpeg, gif'
    return '''
    <!doctype html>
    <html>
    <head>
    <title>Завантаження файлу: txt, pdf, png, jpg, jpeg, gif</title>
    </head>
    <body>
    <h1>Завантаження файлу</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Завантажити>
    </form>
    </body>
    </html>
    '''


# Сторінка для скачування файлу
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('/шлях/до/вашого/каталогу', filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
