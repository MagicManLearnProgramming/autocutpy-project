#! /usr/bin/env python
# coding=utf-8

import os

def test():
    if "result" in os.listdir(os.getcwd()):
        print "yes"
    else:
        os.mkdir("result")

if __name__ == "__main__":
    test()
