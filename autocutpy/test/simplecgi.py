#!/usr/bin/env python

import BaseHTTPServer
import CGIHTTPServer
import cgitb
import webbrowser

cgitb.enable()  ## This line enables CGI error reporting

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 9527)
handler.cgi_directories = ["/cgi-bin"]

httpd = server(server_address, handler)
webbrowser.open("http://localhost:9527/cgi-bin/get_items.py")
httpd.serve_forever()
