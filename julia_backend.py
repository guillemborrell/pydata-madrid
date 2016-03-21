from PIL import Image
from matplotlib import cm
from itertools import product
import numpy as np
import julia_fast
import zmq
import io
import time

zmq_context = zmq.Context.instance()
recv_socket = zmq_context.socket(zmq.REP)
recv_socket.bind('tcp://127.0.0.1:5555')

def gen_image(key, w, h, cre, cim, cmap):
    start = time.perf_counter()
    m = julia_fast.julia_set(w, h, cre + cim*1j)
    end = time.perf_counter()-start
    
    image_data = np.empty((h,w,3), dtype=np.uint8)
    colors = 255*np.array(getattr(cm, cmap).colors)

    for j,i in product(range(h), range(w)):
        image_data[j,i,:] = colors[m[j,i]]

    image = Image.fromarray(image_data, mode='RGB')
    
    stream = io.BytesIO()
    image.save(stream, format='png')
    stream.seek(io.SEEK_SET)
    print('Made {} x {} image in {} seconds'.format(w, h, end))
    return stream.read()


if __name__ == '__main__':
    print('Listening to 127.0.0.1:5555')
    while True:
        message = recv_socket.recv_pyobj()
        recv_socket.send(gen_image(**message))
