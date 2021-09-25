import requests
from pathlib import Path



BIG_NUMBER = int(10e100)

class EsriWorldStreetMap():
    url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}/'
    max_z = BIG_NUMBER
    max_y= BIG_NUMBER
    max_x = BIG_NUMBER
    def download(self, path = "./download"):
        f_default = open("./assets/default.jpeg", "rb")
        default = f_default.read()
        index = 0
        _index = 1
        break_y = False
        break_z = False
        print("Begin")
        for z in range(self.max_z):
            if break_z:
                break
            for y in range(self.max_y):
                if break_y:
                    break_y = False
                    break
                for x in range(self.max_x):
                    if index % 20 and index != _index :
                        _index = index
                        print("{} images téléchargées".format(index),end="\r")
                    r = requests.get(self.url.format(z=z,y=y,x=x))
                    if (default != r.content):
                        index += 1
                        _path = '{path}/{z}/{y}/'.format(path=path,z=z,y=y)
                        Path(_path).mkdir(parents=True, exist_ok=True)
                        with open("{}/{}.jpeg".format(_path, x), 'wb') as f:
                            f.write(r.content)
                    else:
                        if x== 0 :
                            break_y = True
                            if y == 0:
                                break_z = True
                        break
        f_default.close()
        print("End")


    