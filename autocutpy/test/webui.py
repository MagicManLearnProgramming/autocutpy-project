#! /usr/bin/env python
# coding=utf-8

import webbrowser
from os import curdir, sep
from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
from threading import Thread
from time import sleep
import cgitb;
import urllib2

cgitb.enable()


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


def lunch():
    try:
        server_address = ("", 9527)
        handler = CGIHTTPRequestHandler
        handler.cgi_directories = ["/"]
        sv = HTTPServer(server_address, handler)
        print "Welcome to Autocutpy web server!"
        sv.serve_forever()
    except KeyboardInterrupt:
        print "^C received, shutting down"
        sv.socket.close()

def wrap_test():
    print "Now wrapping...<br>n"

def test():
    # lunch()
    # browser = Thread(target=webbrowser.open, args=("http://localhost:9527/cgi-bin/get_items.py", ))
    server = Thread(target=lunch)
    server.start()
    # webbrowser.open("http://localhost:9527/cgi-bin/get_items.py")
    browser = Thread(target=webbrowser.open, args=("http://localhost:9527/get_items.py",))
    browser.start()
    response = urllib2.urlopen("http://localhost:9527/get_items.py")
    print response.read()
    sleep(1)
    response = urllib2.urlopen("http://localhost:9527/get_items.py")
    print response.read()
    # browser.start()
    # browser.join()
    # server.join()
    #
    # print "ok"


if __name__ == "__main__":
    test()
