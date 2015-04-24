from imgurpython import ImgurClient
import os
import random
import urllib
import string
import shutil

class ImgurAPIClient:
    def __init__(self):
        secret_data = open('secret.txt','r')
        client_id = secret_data.readline().strip()
        client_secret = secret_data.readline().strip()
        self.client = ImgurClient(client_id, client_secret)
        self.url_opener = urllib.URLopener()

    # Implement error checking
    def get_album(self,albumID,randID):
        target_album = self.client.get_album(albumID)
        links = [i['link'] for i in target_album.images]
        totalsize = sum([i['size'] for i in target_album.images])
        for idx, i in enumerate(links):
            self.url_opener.retrieve(i,randID + '/' + str(idx).zfill(4) + '.gif')
        return True

    def upload_image(self,imagename):
        x = self.client.upload_from_path(imagename)
        return x['link']


imgur_client = ImgurAPIClient()
# Generate an ID to be used as the image ID.
def id_generator():
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])

def parseAlbum(album_ID):
    rand_id = id_generator()
    os.mkdir(rand_id)
    imgur_client.get_album(album_ID,rand_id)

    # concatenate the gifs into one single super-gif with the folder's name
    os.system('convert -delay 0 -loop 0 ' + rand_id + '/*.gif ' + rand_id + '.gif')

    # upload the image to imgur
    x = imgur_client.upload_image('./' + rand_id + '.gif')

    # Clean up our created files
    shutil.rmtree(rand_id)
    os.remove(rand_id + '.gif')
    return x

if __name__=='__main__':
    print 'Input the album string or url:'
    i = raw_input()
    output = parseAlbum(i.split('/')[-1])
    print 'Your final file was uploaded to ' + output
