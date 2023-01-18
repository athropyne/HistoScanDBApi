from flask import Flask, flash, redirect, url_for, render_template, request
import os

from werkzeug.utils import secure_filename

import os.path

import slideio as slideio
from matplotlib import pyplot as plt

#папка для сохранения загруженных файлов
UPLOAD_FOLDER = './'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'svs'}

#создаем экземпляр приложения
app = Flask(__name__)

def svs_convert():
    image_path = os.path.join('input', 'md519.svs')
    slide = slideio.open_slide(image_path, "SVS")
    raw_string = slide.raw_metadata
    print(raw_string.split("|"))

    scene = slide.get_scene(0)
    scene.name, scene.rect, scene.num_channels, scene.resolution

    image = scene.read_block(size=(500, 0))
    plt.imshow(image)
    plt.savefig(os.path.join('static/assets/images', 'sample-el-1-bg.jpg'))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/case')
def case():
    return render_template('case.html')


@app.route('/entry')
def entry():
    return render_template('entry.html')


@app.route('/cases')
def cases():
    return render_template('cases.html')


@app.route('/account')
def account():
    return render_template('account.html')


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/case', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        """ проверим, передается ли в запросе файл """
        if 'file' not in request.files:
            """ После перенаправления на страницу загрузки """
            """ покажем сообщение пользователю """
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            """ безопасно извлекаем оригинальное имя файла """
            filename = secure_filename(file.filename)
            # сохраняем файл
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # если все прошло успешно, то перенаправляем
            # на функцию-представление 'download_file'
            # для скачивания файла
            svs_convert()
            return redirect(url_for('upload_file', name=filename))



if __name__ == '__main__':
    app.run(debug=True)



