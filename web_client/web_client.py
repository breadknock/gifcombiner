from flask import Flask
from flask import request
from flask import render_template
from imgur_getter import ImgurAPIClient
import os
import random
import string
import shutil

app = Flask(__name__)
imgur_client = ImgurAPIClient()


# Remove old image file and image folder
def clean_up(rand_id):
    try:
        shutil.rmtree(rand_id)
        os.remove('./' + rand_id + '.gif')
    # If the file doesn't exist
    except OSError:
        pass


# Create a random ID to store the images as to prevent conflicts with threading
def create_random_id():
    return ''.join([random.choice(string.ascii_letters + string.digits)
                    for i in range(10)])


@app.route('/')
def send_homepage():
    return render_template('index.html')


@app.route('/API', methods=['POST'])
def create_image():
    print request.form.getlist('input_type')
    if 'input_type' not in request.form or 'output_type' not in request.form:
        return 'Need to declare an input and output type', 500

    rand_id = create_random_id()
    os.mkdir(rand_id)

    filename = './' + rand_id + '.gif'

    link = ''

    # Download files to the server from the selected API
    if request.form['input_type'] == 'IMGUR' and 'album_id' in request.form:
        err = imgur_client.get_album(request.form['album_id'], rand_id)
        if err is not None:
            clean_up(rand_id)
            return err, 500
    else:
        print 'Input not recognized'
        clean_up(rand_id)
        return 'Input type not recognized', 500

    os.system('convert -delay 0 -loop 0 ' +
              rand_id + '/*.gif ' + rand_id + '.gif')
    print 'Created composite gif: ' + rand_id + '.gif'

    # Host files to the selected API output
    if request.form['output_type'] == 'IMGUR':
        link = imgur_client.upload_image(filename)
        clean_up(rand_id)
        if link is None:
            return 'Could not post the gif', 500
        else:
            print 'GIF uploaded'
    else:
        clean_up(rand_id)
        return 'Input type not recognized', 500

    return link

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
