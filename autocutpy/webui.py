#! /usr/bin/env python
# coding=utf-8

import os
from autocutpy import multiple_trim
import cgi


class AutoCutUi(object):
    def __init__(self):
        self.__header = "Content-Type: text/html\n\n"
        self.__formhtml = """<HTML><HEAD><TITLE>get path demo</TITLE></HEAD>
<FORM enctype="multipart/form-data" ACTION="webui.py" method="post">
<BODY><H3>Automatically cut and trim</H3>
<INPUT TYPE=hidden NAME=action VALUE=edit>
<p>Select your file(s) <input type=file name="filename" multiple /></p>
<P><B>Choose the graininess. The bigger graininess, the larger size and the less number of photos.</B></p>
%s
<P><INPUT TYPE=submit></p></FORM></BODY></HTML>"""
        self.__frdo = "<INPUT TYPE=radio NAME=grn VALUE='%s' %s> %s\n"

    def showfrom(self):
        grn = ''
        for i in xrange(6):
            checked = ''
            if i == 5:
                checked = "CHECKED"
            grn += self.__frdo % (str(i), checked, str(i))
        print self.__header + self.__formhtml % (grn)

    def up_load(self, items):
        """
        :param items: List of cgi.FieldStorage() file items
        :return: Up load them and return file list
        """
        fn_lst = []
        if "tmp" not in os.listdir(os.getcwd()):
            os.mkdir("tmp")
        for item in items:
            if item.filename:
                fn = 'tmp/%s' % os.path.basename(item.filename)
                with open(fn, 'wb') as f:
                    f.write(item.file.read())
                fn_lst.append(fn)
            else:
                print item
        return fn_lst

    def process(self):
        fn_lst = []
        grn = 5
        form = cgi.FieldStorage()
        if "filename" in form:
            items = form["filename"]
            if not isinstance(items, list):
                items = [items]
            fn_lst = self.up_load(items)

            print """< input name = "Submit" type = "button" id = "Submit" onClick = "javascript:history.back(1)" value = "BACK" / >"""
        if "grn" in form:
            grn = int(form["grn"].value)
        if fn_lst:
            self.trim(fn_lst, grn)
        else:
            self.showfrom()

    def trim(self, fn_lst, grn):
        print self.__header
        multiple_trim(fn_lst, grn)
        path = os.path.join(os.getcwd(), "result")
        print "The trimmed photos are in <a href='%s'>%s<BR></a>" % (path, path)
        print '<INPUT name = "Submit" type = "button" id = "Submit" ' \
              'onClick = "javascript:history.back(1)" value = "BACK" / >'
        for fn in fn_lst:
            os.remove(fn)


def test():
    # lunch()
    # # browser = Thread(target=webbrowser.open, args=("http://localhost:9527/cgi-bin/get_items.py", ))
    # server = Thread(target=lunch)
    # server.start()
    # # webbrowser.open("http://localhost:9527/cgi-bin/get_items.py")
    # browser = Thread(target=webbrowser.open, args=("http://localhost:9527/get_items.py",))
    # browser.start()
    # response = urllib2.urlopen("http://localhost:9527/get_items.py")
    # print response.read()
    # sleep(1)
    # response = urllib2.urlopen("http://localhost:9527/get_items.py")
    # print response.read()
    # # browser.start()
    # # browser.join()
    # server.join()
    #
    # print "ok"
    pass


def main():
    ui = AutoCutUi()
    ui.process()


if __name__ == "__main__":
    main()
    # test()
