from imgurpython import ImgurClient
import os
import random
import urllib
import string
import shutil

s = open('secret.txt','r')
client_id = s.readline().strip()
client_secret = s.readline().strip()
client = ImgurClient(client_id,client_secret)

def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def parseAlbum(albumID):
    al = client.get_album(albumID)
    links = [i['link'] for i in al.images]
    rand_id = id_generator(10)
    os.mkdir(rand_id)
    for idx,i in enumerate(links):
        testfile = urllib.URLopener()
        testfile.retrieve(i,rand_id + '/' + str(idx).zfill(3) + '.gif')
    os.system('convert -delay 0 -loop 0 ' + rand_id + '/*.gif ' + rand_id + '.gif')
    shutil.rmtree(rand_id)
    x = client.upload_from_path('./' + rand_id + '.gif', config=None, anon=True)
    os.remove(rand_id + '.gif')
    return x['link']

if __name__=='__main__':
    print 'Input the album string or url:'
    i = raw_input()
    output = parseAlbum(i.split('/')[-1])
    print 'Your final file was uploaded to ' + output
