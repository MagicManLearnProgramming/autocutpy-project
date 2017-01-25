#! /usr/bin/env python
# coding=utf-8

import cgi

header = "Content-Type: text/html\n\n"

formhtml = """<HTML><HEAD><TITLE>get path demo</TITLE></HEAD>
<FORM ACTION="get_path.py">
<BODY><H3>GET PATH</H3>
<B>Enter your path</B>
<INPUT TYPE=hidden NAME=action VALUE=edit>
<INPUT TYPE=text NAME=path VALUE="NEW PATH" SIZE=15>
<P><B>Choose the graininess. The bigger the photos larger.</B>
%s
<P><INPUT TYPE=submit></FORM></BODY></HTML>"""

frdo = "<INPUT TYPE=radio NAME=grn VALUE='%s' %s> %s\n"


def showfrom():
    grn = ''
    for i in xrange(6):
        checked = ''
        if i == 5:
            checked = "CHECKED"
        grn = grn + frdo % (str(i), checked, str(i))
    print header + formhtml % (grn)


def process():
    form = cgi.FieldStorage()
    showfrom()


if __name__ == "__main__":
    process()
