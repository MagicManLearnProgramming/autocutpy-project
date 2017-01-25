#! /usr/bin/env python
# coding=utf-8

import cgi
import os
from test import wrap_test

header = "Content-Type: text/html\n\n"

formhtml = """<HTML><HEAD><TITLE>get path demo</TITLE></HEAD>
<FORM enctype="multipart/form-data" ACTION="get_items.py" method="post">
<BODY><H3>Automatically cut and trim</H3>
<INPUT TYPE=hidden NAME=action VALUE=edit>
<p>Select your file(s) <input type=file name="filename" multiple /></p>
<P><B>Choose the graininess. The bigger graininess, the larger size and the less number of photos.</B></p>
%s
<P><INPUT TYPE=submit></p></FORM></BODY></HTML>"""

frdo = "<INPUT TYPE=radio NAME=grn VALUE='%s' %s> %s\n"


def showfrom():
    grn = ''
    for i in xrange(6):
        checked = ''
        if i == 5:
            checked = "CHECKED"
        grn = grn + frdo % (str(i), checked, str(i))
    print header + formhtml % (grn)


def up_load(items):
    """
    :param items: List of cgi.FieldStorage() file items
    :return: Up load them and return file list
    """
    fn_lst = []
    for item in items:
        if item.filename:
            fn = 'tmp/%s' % os.path.basename(item.filename)
            with open(fn, 'wb') as f:
                f.write(item.file.read())
            fn_lst.append(fn)
        else:
            print item
    return fn_lst


def get_res():
    fn_lst = []
    grn = 5
    form = cgi.FieldStorage()
    if "tmp" not in os.listdir(os.getcwd()):
        os.mkdir("tmp")
    if "filename" in form:
        items = form["filename"]
        if not isinstance(items, list):
            items = [items]
        fn_lst = up_load(items)
        print header
        wrap_test()
        print fn_lst
    if "grn" in form:
        grn = form["grn"].value
        print grn
    else:
        showfrom()


if __name__ == "__main__":
    get_res()
