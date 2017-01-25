#! /usr/bin/env python
# coding=utf-8

import webbrowser
from os import curdir, sep
from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
import cgitb; cgitb.enable()
import os


class MyHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        try:
            f = open(curdir + sep + self.path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404, "File not found: %s" % self.path)


def test():
    # reshtml = "Hello World"
    # print reshtml
    try:
        server = HTTPServer(('', 9527), MyHandler)
        print "welcome"
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C received, shutting down"
        server.socket.close()


if __name__ == "__main__":
    path = os.getcwd()
    print os.path.join(path, "tmp", "jpg")
    # w = webbrowser.open("http://localhost:9527/cgi-bin/hello.py")
    # test()
