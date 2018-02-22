from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
import numpy as np
from PIL import Image
import io


class handle(BaseHTTPRequestHandler):
    images = {}
    qs = {}
    def do_POST(self):

        content_len = int(self.headers.get_all('content-length')[0])
        x=self.rfile.read(content_len)
        try:
            self.images[self.client_address[0]] = np.asarray(Image.open(io.BytesIO(x)))

        except:
            self.qs[self.client_address[0]] = x.decode('ascii')


        self.send_response(200)
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f'{model(self.images[self.client_address[0]], self.qs[self.client_address[0]])}'.encode('ascii'))
        del self.images[self.client_address[0]]
        del self.qs[self.client_address[0]]
        
        

def run(server_class=HTTPServer, handler_class=handle, port=80):

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server')
    httpd.serve_forever()
def model(image, q):
    #placeholder model function
    return 0
if __name__ == '__main__':
    run()
    