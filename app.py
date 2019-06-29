from flask import Flask, render_template, request, flash, redirect, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os


app = Flask(__name__)

dropzone = Dropzone(app)

# dropzone config
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['SECRET_KEY'] = 'hjkjgiiuworiof'

# upload config
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/images'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app, 32 * 1024 * 1024) # 32MB, default is 16MB


@app.route('/', methods=['GET', 'POST'])
def index():
    file_urls = [] # list to hold uploaded image urls

    if request.method == "POST":
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            print(file.filename)

            # save files to the images folder
            filename = photos.save(
                file,
                name = file.filename
            )
            # append image urls
            file_urls.append(photos.url(filename))

        flash(u'Files uploaded!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html')


def make_dir(folder_name):
    folder_path = os.getcwd + 'images/'+folder_name
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


if __name__ == "__main__":
    app.run(debug=True)
