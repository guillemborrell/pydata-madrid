from flask import Flask, request, make_response
from julia_set import julia_set
from PIL import Image
from matplotlib import cm
from itertools import product
import numpy as np
import time
import io
import julia_fast

app = Flask(__name__)

@app.route('/')
def root():
    w = request.args.get('w')
    if not w: w = 400
    else: w = int(w)
    h = request.args.get('h')
    if not h: h = 300
    else: h = int(h)
    cre = request.args.get('cre')
    if not cre: cre = -0.8
    else: cre = float(cre)
    cim = request.args.get('cim')
    if not cim: cim = .156
    else: cim = float(cim)
    cmap = request.args.get('cmap')
    if not cmap: cmap = 'inferno'

    start = time.perf_counter()
    m = julia_fast.julia_set(w, h, cre + cim*1j)
    print(time.perf_counter()-start)
    
    image_data = np.empty((h,w,3), dtype=np.uint8)
    colors = 255*np.array(getattr(cm, cmap).colors)

    for j,i in product(range(h), range(w)):
        image_data[j,i,:] = colors[m[j,i]]

    image = Image.fromarray(image_data, mode='RGB')
    
    stream = io.BytesIO()
    image.save(stream, format='png')
    stream.seek(io.SEEK_SET)
    
    resp =  make_response(stream.read())
    resp.headers['Content-Type'] = 'image/png'

    return resp


application = app


if __name__ == '__main__':
    app.debug = True
    app.run()

    
