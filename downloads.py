import requests
from pathlib import Path

class EsriWorldStreetMap():
    url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}/'
    max_z = 10e100
    max_y= 10e100
    max_x = 10e100
    def download(self, path = "./download"):
        f_default = open("./assets/default.jpeg", "rb")
        default = f_default.read()
        index = 0
        count = self.max_z *self.max_y* self.max_x
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
                    index += 1
                    if index % 50 :
                        print("Progress = {:.2f}%".format(index*100/count))
                    r = requests.get(self.url.format(z=z,y=y,x=x))
                    if (default != r.content):
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


    