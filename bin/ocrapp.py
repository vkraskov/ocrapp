from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import threading
import base64
from PIL import Image, ImageOps
import io
import os
import subprocess
import urllib.parse

USE_HTTPS = False


class Handler(BaseHTTPRequestHandler):

    def reply_with(self, value):
        self.send_response(200)
        self.end_headers()
        json_string = json.dumps(value)
        self.wfile.write(json_string.encode(encoding='utf_8'))
        self.wfile.write(b"\n")
        return

    def do_GET(self):
        print("GET path: %s" % self.path)
        res = urllib.parse.urlparse(self.path)
        print("GET res.path: %s" % res.path)
        if res.path == '/service/readinessProbe':
            value = {'status': 'ok', 'result': "true"}
            self.reply_with(value)
            return
        if res.path == '/service/livenessProbe':
            value = {'status': 'ok', 'result': "true"}
            self.reply_with(value)
            return
        if res.path == '/service/startupProbe':
            value = {'status': 'ok', 'result': "true"}
            self.reply_with(value)
            return
        #
        self.reply_with({'GET::thread': threading.currentThread().getName()})

    def do_POST(self):
        print("POST path: %s" % self.path)
        post_body = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
        data = json.loads(post_body)
        image_b64 = data['image']
        image_bytes = base64.b64decode(image_b64.encode('utf-8'))
        # f = open('/tmp/my_file', 'w+b')
        #
        file_dir = '/tmp'
        file_name = 'image-' + threading.currentThread().getName()
        file_jpg = file_dir + '/' + file_name + '.jpg'
        file_txt = file_dir + '/' + file_name + '.txt'
        #
        img = Image.open(io.BytesIO(image_bytes))
        # img = ImageOps.grayscale(img)
        thresh = 128
        fn = lambda x: 255 if x > thresh else 0
        img_bw = img.convert('L').point(fn, mode='1')
        im1 = img_bw.save(file_jpg, "JPEG", quality=90, optimize=True, progressive=True)
        #
        cmd_sh = "cd " + file_dir + "; tesseract " + file_jpg + " " + file_name + " -l eng --psm 1 --oem 3 txt"
        print("About to  start %s" % cmd_sh)
        return_code = subprocess.call(cmd_sh, shell=True)
        os.remove(file_jpg)
        #
        with open(file_txt) as f:
            text = f.read()
            print("Got text %s" % text)
            f.close()
            os.remove(file_txt)
            value = {'status': 'ok', 'text': text}
            self.reply_with(value)
            return
        # img_arr = np.asarray(img)
        # print('img shape', img_arr.shape)
        #
        #
        self.reply_with({'POST::thread': threading.currentThread().getName()})
        return


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    from os import environ

    config = {'app_host': '0.0.0.0', 'app_port': 8080}
    if 'APP_API_HOST' in environ:
        config['app_host'] = environ['APP_API_HOST']
    if 'APP_API_PORT' in environ:
        config['app_port'] = environ['APP_API_PORT']

    server = ThreadingSimpleServer((config['app_host'], int(config['app_port'])), Handler)
    server.serve_forever()


if __name__ == '__main__':
    run()
