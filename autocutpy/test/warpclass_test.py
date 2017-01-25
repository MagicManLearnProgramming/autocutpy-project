#! /usr/bin/env python
# coding=utf-8

import cv2
import numpy as np


class Father(object):
    def __init__(self, num):
        assert isinstance(num, int)
        self.num = num
        self.string = str(self.num)

    def plus(self):
        return self.num + 1


def build(string):
    return Father(int(string))


class Son(object):
    def __init__(self, string):
        obj = build(string)
        self.__data = obj

    def get(self):
        return self.__data

    def __repr__(self):
        return "self.__data"

    def __str__(self):
        return str(self.__data)

    def __getattr__(self, attr):
        print "debug attr = ", attr
        return getattr(self.__data, attr)

    def __getitem__(self, item):
        return self.__data[item]



class CvDer(np.ndarray):
    def __new__(subtype, f_name):
        arr = cv2.imread(f_name)
        shape = arr.shape
        arr.__class__ = subtype
        return arr
        # return arr.__new__(subtype, shape, arr.dtype,
        #                 buffer=arr)
        # return np.ndarray.__new__(subtype, shape, arr.dtype,
        #                 buffer=arr)

    def __init__(self, f_name):
        self.c = 111






    # def __new__(cls, f_name):
    #     return np.ndarray.__new__(cv2.imread(f_name))

    def show(self, text):
        cv2.imshow(text, self)
        cv2.waitKey(0)


def test():
    f_name = "../../resources/demo_00.jpg"
    img = CvDer(f_name)
    print type(img)
    img[:200, :200] = 255
    img.show(f_name)
    print img.c


    #img.show(f_name)


    # a = np.array([1, 2])
    # b = a.tolist()
    # c = np.ndarray(b)
    # print c

    # a = Son("12")
    # print a.plus()

    # a = build("12")
    # print a.plus()
    # a.c = 10
    # print a.c
    pass

if __name__ == "__main__":
    test()
