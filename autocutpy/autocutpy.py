#! /usr/bin/env python
# coding=utf-8

from trimmer import *
from multiprocessing import Pool, cpu_count
import sys
import getopt
from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
from threading import Thread
import webbrowser
import os
import platform



def trim(fn, grn=5, path=""):
    """
    function: Put the trimmed photos into result dir
    :param path: The directory to save the result
    :param fn: file name
    :param grn: The graininess of trimmer. range is (0, 5), the graininess larger, the trimmed photos larger(Maybe).
    :return: No return. But print result text. e.g. "xxxx.jpg trimmed"
    """
    if "Windows" in platform.platform():
        fn = fn.encode('gbk')
    else:
        fn = fn.encode('utf-8')
        
    if not path:
        if "result" not in os.listdir(os.getcwd()):
            os.mkdir("result")
        out_path = os.path.join(os.getcwd(), "result",  + os.path.basename(fn)[: -4] + "_%s.jpg")
    else:
        out_path = os.path.join(path, os.path.basename(fn)[: -4] + "_%s.jpg")

    try:
        img = load_img(fn)
        trm = Trimmer(img, grn)
        photos = trm.trim2()
        for idx, photo in enumerate(photos):
            new_fn = out_path % idx
            photo.save(new_fn)
        result = "%s trimmed<br>" % fn
    except Exception, e:
        result = e

    print result


def multiple_trim(fn_lst, grn=5, path=""):
    """
    :param path: The directory to save the result
    :param fn_lst: List of file names
    :param grn: The graininess of trimmer. range is (0, 5), the graininess larger, the trimmed photos larger(Maybe).
    :return: No return. But print result texts. e.g. "xxxx.jpg trimmed"
    """
    p = Pool(cpu_count())
    for fn in fn_lst:
        p.apply_async(trim, (fn, grn, path))
    p.close()
    p.join()


def process():
    hp = """
        command e.g.:
        1. >>>python autocutpy.py -f pic/demo_01.jpg -g 5
        -f: input file name with path
        2. >>>python autocutpy.py -p pic/
        -p: path of input files
        3. >>>python autocutpy.py -w
        -w start a web server.
        4. >>>python autocutpy.py -h
        -h: Show the help
        5. >>>python autocutpy.py
        No arg. start a graphical user interface.
        """
    if len(sys.argv) < 2:
        import gui
        return gui.main()
    else:
        fn_lst = grn = None
        opts, args = getopt.getopt(sys.argv[1:], "f:p:g:h")
        for opt, value in opts:
            if opt == "-f":
                fn_lst = [value]
            elif opt == "-p":
                fn_lst = [value + fn for fn in os.listdir(value)]
            elif opt == "-g":
                grn = value
            elif opt == "-w":
                return web_ui()
            elif opt == "-h":
                print hp
                return
        return multiple_trim(fn_lst, grn)


def launch():
    """
    Launch a web server of Autocutpy
    """
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


def web_ui():
    """
    Launch web server and a browser that points to that web server
    """
    server = Thread(target=launch)
    server.start()
    browser = Thread(target=webbrowser.open, args=("http://localhost:9527/webui.py",))
    browser.start()


def test():
    path = "../resources/"
    fn_lst = [path + fn for fn in os.listdir(path) if fn[-4:] == ".jpg"]
    multiple_trim(fn_lst)


if __name__ == "__main__":
    process()
