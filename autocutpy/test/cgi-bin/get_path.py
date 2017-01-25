#! /usr/bin/env python
# coding=utf-8

import cgi
import os

header = "Content-Type: text/html\n\n"

formhtml = """<HTML><HEAD><TITLE>get path demo</TITLE></HEAD>
<FORM enctype="multipart/form-data" ACTION="get_path.py" method="post">
<BODY><H3>Automatically cut and trim</H3>
<INPUT TYPE=hidden NAME=action VALUE=edit>
<p>Select your file(s) <input type="file" name="filename" multiple /></p>
<p><input type="submit" value="upload" /></p>
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


def get_res(form):
    """
    :param form:  cgi.FieldStorage() object
    :return: file names and graininess
    """
    pass


def process():
    form = cgi.FieldStorage()
    if "tmp" not in os.listdir(os.getcwd()):
        os.mkdir("tmp")
    if "filename" in form:
        files = form["filename"]
        print header
        for item in files:
            if item.filename:
                fn = os.path.basename(item.filename)
                with open('tmp/%s' % fn, 'wb') as f:
                    f.write(item.file.read())
                print "%s uploaded!"
            else:
                print item
    else:
        showfrom()


if __name__ == "__main__":
    process()
