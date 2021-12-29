from downloads import EsriWorldStreetMap

ersi = EsriWorldStreetMap()

# cd /home/adil/dev/python/leaflet/download && source venv/bin/activate && venv/bin/python main.py

if __name__ == "__main__":
    # ersi.download()
    test = ersi.specific( begin = (10.756043395476832, 15.151256455158718), end = (47.10696511636121, -33.57353845655261))


