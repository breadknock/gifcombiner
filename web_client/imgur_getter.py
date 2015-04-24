from imgurpython import ImgurClient
import urllib
import string


class ImgurAPIClient:
    def __init__(self):
        secret_data = open('../secret.txt', 'r')
        client_id = secret_data.readline().strip()
        client_secret = secret_data.readline().strip()
        self.client = ImgurClient(client_id, client_secret)
        self.url_opener = urllib.URLopener()
        secret_data.close()

    # Implement error checking
    def get_album(self, albumID, randID):
        try:
            target_album = self.client.get_album(albumID)
            links = [i['link'] for i in target_album.images]
            totalsize = sum([i['size'] for i in target_album.images])
            for idx, i in enumerate(links):
                self.url_opener.retrieve(i, randID + '/' +
                                         str(idx).zfill(4) + '.gif')
        except Exception:
            return "FAIL"
        return None

    def upload_image(self, imagename):
        try:
            x = self.client.upload_from_path(imagename)
            return x['link']
        except Exception:
            return None
