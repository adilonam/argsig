import requests
from pathlib import Path
import os.path
from datetime import datetime
import math

BIG_NUMBER = int(10e100)

class EsriWorldStreetMap():
    url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}/'
    def download(self, path = "./download", z_begin = 0, y_begin = 0, x_begin = 0, z_end = BIG_NUMBER, y_end = BIG_NUMBER, x_end = BIG_NUMBER):
        f_default = open("./assets/default.jpeg", "rb")
        log = open("./assets/log.txt", "a")
        default = f_default.read()
        index = 0
        _index = 1
        break_y = False
        break_z = False
        log.write("[{}] Begin\n".format(datetime.now()))
        for z in range(z_begin, z_end +1 ):
            if break_z:
                break
            for y in range(y_begin, y_end + 1 ):
                if break_y:
                    break_y = False
                    break
                _path = './{path}/{z}/{y}/'.format(path=path,z=z,y=y)
                Path(_path).mkdir(parents=True, exist_ok=True)
                for x in range(x_begin, x_end + 1):
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
        log.write("[{}] End\n".format(datetime.now()))
        log.close()
        
    def specific(self, begin = (11.821210065250792, 4.958433331541971), end = (41.23902940678558, -18.295661311840025)):
        max_z = BIG_NUMBER
        for z in range(max_z):
            img_begin = self.image_coordinate(*begin, z)
            img_end = self.image_coordinate(*end, z)
            self.download(z_begin=z, z_end=z, 
            y_begin= min(img_begin[0], img_end[0]), y_end=max(img_begin[0], img_end[0]), 
            x_begin= min(img_begin[1], img_end[1]), x_end=max(img_begin[1], img_end[1])
             )
    

    def image_coordinate(self, latitude, longitude, zoom):
        xtile = math.floor( (longitude + 180) / 360 * (1<<zoom) )
        ytile = math.floor( (1 - math.log(math.tan(math.radians( latitude)) + 1 / math.cos(math.radians(latitude))) / math.pi) / 2 * (1<<zoom) )
        return (ytile, xtile)
        



    