from imgurpython import ImgurClient
import urllib
import string

# Acts as an interface to Imgur, to download and upload images
class ImgurAPIClient:
    MAX_IMAGE_SIZE = 20000000 # ~20MB
    def __init__(self):
        secret_data = open('../secret.txt', 'r')
        client_id = secret_data.readline().strip()
        client_secret = secret_data.readline().strip()
        self.client = ImgurClient(client_id, client_secret)
        self.url_opener = urllib.URLopener()
        secret_data.close()

    # Downloads the given album from Imgur
    def get_album(self, albumID, randID):
        try:
            target_album = self.client.get_album(albumID)
            links = [i['link'] for i in target_album.images]
            totalsize = sum([i['size'] for i in target_album.images])
            if totalsize > self.MAX_IMAGE_SIZE:
                return 'The given album is too big. (>20MB)'

            # Name the images with a number (0001.gif, etc.) to keep ordering
            for idx, i in enumerate(links):
                self.url_opener.retrieve(i, randID + '/' +
                                         str(idx).zfill(4) + '.gif')
        except Exception as e:
            print e
            if '(404)' in str(e):
                return str(e)[5:]
            elif 'Connection aborted' in str(e):
                return 'Lost server connection'
            else:
                return 'Could not complete request'
        return None

    # Uploads the image to Imgur
    def upload_image(self, imagename):
        try:
            x = self.client.upload_from_path(imagename)
            return x['link']
        except Exception:
            return None
