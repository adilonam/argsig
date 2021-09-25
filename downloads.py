import requests
from pathlib import Path
import os.path
from datetime import datetime

BIG_NUMBER = int(10e100)

class EsriWorldStreetMap():
    url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}/'
    max_z = BIG_NUMBER
    max_y= BIG_NUMBER
    max_x = BIG_NUMBER
    def download(self, path = "./download"):
        f_default = open("./assets/default.jpeg", "rb")
        log = open("./assets/log.txt", "a")
        default = f_default.read()
        index = 0
        _index = 1
        break_y = False
        break_z = False
        log.write("[{}] Begin\n".format(datetime.now()))
        for z in range(self.max_z):
            if break_z:
                break
            for y in range(self.max_y):
                if break_y:
                    break_y = False
                    break
                _path = './{path}/{z}/{y}/'.format(path=path,z=z,y=y)
                Path(_path).mkdir(parents=True, exist_ok=True)
                for x in range(self.max_x):
                    if index != _index :
                        _index = index
                        log.write("[{}] {} images téléchargées\n".format(datetime.now(), index))
                    file = "./{}/{}.jpeg".format(_path, x)
                    if os.path.isfile(file):
                        index += 1
                        continue
                    r = requests.get(self.url.format(z=z,y=y,x=x))
                    if (default != r.content):
                        index += 1
                        with open(file, 'wb') as f:
                            f.write(r.content)
                    else:
                        if x== 0 :
                            break_y = True
                            if y == 0:
                                break_z = True
                        break
        f_default.close()
        log.close()
        log.write("[{}] End\n".format(datetime.now()))


    