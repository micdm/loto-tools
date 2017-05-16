#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

from keras.models import load_model
import numpy as np

class RequestHandler(BaseHTTPRequestHandler):

    model = load_model(sys.argv[1])

    def do_GET(self):
        values = list(map(float, self.path[9:].split(',')))
        values = np.array([values])
        prediction = self.model.predict(values)[0]
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(('%s\n%s' % (prediction[0], prediction[1])).encode())


server = HTTPServer(('localhost', 12000), RequestHandler)
server.serve_forever()
