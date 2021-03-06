from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
from PIL import Image
import io
import sqlite3 as sql
from urllib.parse import urlparse, parse_qs
import os
import base64 as bs
import sys
import ssl


class handle(BaseHTTPRequestHandler):
    conn = sql.connect('image.db')
    c = conn.cursor()

    def do_POST(self):
        """
        Takes in input uuid and image and stores it in an image database
        """

        content_len = int(self.headers.get_all('content-length')[0])
        x = self.rfile.read(content_len)
    
        uuid,img = x.split(b';')
        uuid = (uuid.decode('ascii'))
        
        img = bs.b64decode(img)

        params = (uuid,memoryview(img))
        self.c.execute('insert into images values(?, ?)', params)
        self.send_response(200)
        self.end_headers()
        dat = self.c.execute('select * from images;')

        self.conn.commit()


    def do_GET(self):
        """
        Takes in input uuid and question, pulls the corresponding image from the image database, and passes it through the model to obtain an answer
        """
        self.send_response(200)
        self.end_headers()

        x = parse_qs(self.path)
        if '/?uuid' in list(x.keys()) and 'q' in list(x.keys()) and len(x.keys()) == 2:
            
            uuid = (x['/?uuid'][0])
            q = x['q'][0]
            self.c.execute('select img from images where uuid=?', (uuid,))
            img = self.c.fetchone()[0]
            img = np.asarray(Image.open(io.BytesIO(img)))
            self.wfile.write(f'{model(img,q)}'.encode('ascii'))
        elif list(x.keys()) == ['/?uuid']:
            uuid = x['/?uuid'][0]
            
            j = self.c.execute('select img from images where uuid=?', (uuid,))
            if len([i for i in j]) != 0:
                self.wfile.write('True'.encode('ascii'))
            else:
                self.wfile.write('False'.encode('ascii'))


def run(server_class=HTTPServer, handler_class=handle, port=81):
    """
    Runs server at port 80
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='server.key', certfile='server.crt',server_side=True,ssl_version=ssl.PROTOCOL_TLSv1_2)
    print('Starting server')
    httpd.serve_forever()

def model(image, q):
    """
    Placeholder model function
    """
    
    return 0
if __name__ == '__main__':
    run()
    