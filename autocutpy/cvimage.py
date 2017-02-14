#! /usr/bin/env python
# coding=utf-8

import cv2
import numpy as np


class CvImage(np.ndarray):
    """
    Transform ndarray object to CvImage object
    """

    def __new__(subtype, arr):
        mat = arr.copy()
        shape = mat.shape
        return np.ndarray.__new__(subtype, shape, mat.dtype,
                                  buffer=mat)

    def __init__(self, arr):
        self.__arr = arr
        self.__gray = None
        self.__blur = None
        self.__bin = None
        self.__thresh = None
        self.__open = None
        self.__close = None
        self.__cnts = None
        self.__bnd_rects = None
        self.__min_rects = None
        self.__inverse = None

    def get_inverse(self):
        """
        :return: The inverse of the image
        """
        if not isinstance(self.__inverse, CvImage):
            self.__inverse = CvImage(255 - self)
        return self.__inverse

    def draw_rect(self, text, rects=None, color=(0, 0, 255), thickness=2):
        """
        :param thickness: Thickness of the rect
        :param color: Color of the rect
        :param text: Title of the image
        :param rects: List of "rect objects" (Rect())
        :return: Just draw the rects in the image. No return
        """
        if not rects:
            rects = self.get_min_rects()

        if len(self.shape) == 2:
            canvas = CvImage(cv2.cvtColor(self, cv2.COLOR_GRAY2RGB))
        else:
            canvas = CvImage(self)

        rect_box = [rect.rect_box for rect in rects]
        canvas = CvImage(cv2.drawContours(canvas, rect_box, -1, color, thickness))
        canvas.show(text)

    def get_bnd_rects(self, renew=False):
        """
        :param renew: generate a new list of "bounding rect objects" (Rect()) or just return the old one(if exist)
        :return: List of "min rect objects"
        """
        if (not self.__bnd_rects) or renew:
            cnts = self.get_cnts()
            rects = [cv2.boundingRect(cnt) for cnt in cnts]
            self.__bnd_rects = [Rect(rect) for rect in rects]
        return self.__bnd_rects

    def get_min_rects(self, renew=False):
        """
        :param renew: generate a new list of "min rect objects" (Rect()) or just return the old one(if exist)
        :return: List of "min rect objects"
        """
        if (not self.__min_rects) or renew:
            cnts = self.get_cnts()
            rects = [cv2.minAreaRect(cnt) for cnt in cnts]
            self.__min_rects = [Rect(rect) for rect in rects]
        return self.__min_rects

    def get_cnts(self, cnt_mode=cv2.RETR_EXTERNAL, renew=False):
        """
        :param cnt_mode: Contour Retrieval Mode e.g. cv2.RETR_EXTERNAL, cv2.RETR_LIST, cv2.RETR_TREE
        :param renew: generate a new contours list or just return the old one(if exist)
        :return: List of contours
        """
        if (not self.__cnts) or renew:
            image, contours, hierarchy = cv2.findContours(self, cnt_mode,
                                                          cv2.CHAIN_APPROX_SIMPLE)
            self.__cnts = contours
        return self.__cnts

    def get_close(self, core=(7, 7), renew=False):
        """
        :param core: the core for open operation
        :param renew: generate a new "CLOSE" image or just return the old one(if exist)
        :return: An image obj of the img after CLOSE operation
        Warning: This function do NOT transform the image to binaraztion image!!!
        """
        if (not isinstance(self.__close, CvImage)) or renew:
            kernel = np.ones(core, np.uint8)
            self.__close = CvImage(cv2.morphologyEx(self, cv2.MORPH_CLOSE, kernel))
        return self.__close

    def get_open(self, core=(7, 7), renew=False):
        """
        :param core: the core for open operation
        :param renew: generate a new "OPEN" image or just return the old one(if exist)
        :return: An image obj of the img after OPEN operation
        Warning: This function do NOT transform the image to binaraztion image!!!
        """
        if (not isinstance(self.__open, CvImage)) or renew:
            kernel = np.ones(core, np.uint8)
            self.__open = CvImage(cv2.morphologyEx(self, cv2.MORPH_OPEN, kernel))
        return self.__open

    def get_bin(self, thresh=0, renew=False):
        """
        :param renew: generate a new blur image or just return the old blur image(if exist)
        :param thresh: the threshold of binarazation
        :return: the binarazation image
        """
        if (not isinstance(self.__bin, CvImage)) or renew:
            gray_img = self.get_gray()
            if thresh == 0:
                self.__thresh, bin_mat = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            else:
                self.__thresh, bin_mat = cv2.threshold(gray_img, thresh, 255, cv2.THRESH_BINARY)
            self.__bin = CvImage(bin_mat)
        return self.__bin

    def get_blur(self, g_core=(1, 3), renew=False):
        """
        :param renew: generate a new blur image or just return the old blur image(if exist)
        :param g_core: the core for gaussian blur
        :return: blur image
        """
        if (not isinstance(self.__blur, CvImage)) or renew:
            self.__blur = CvImage(cv2.GaussianBlur(self, g_core, 0))
        return self.__blur

    def get_gray(self):
        """
        :return: Gray image
        """
        if not isinstance(self.__gray, CvImage):
            self.__gray = CvImage(cv2.cvtColor(self, cv2.COLOR_BGR2GRAY))
        return self.__gray

    def show(self, text):
        """
        :param text: Title of the image
        :return: Just show the image, no return
        """
        cv2.namedWindow(text, cv2.WINDOW_NORMAL)
        cv2.imshow(text, self)
        cv2.waitKey(0)

    def save(self, fn):
        cv2.imwrite(fn, self)


class Rect(object):
    """
    Rect obj with attr as size, bounds, feature... methods as deviation, set_features
    """

    def __init__(self, rect):
        self.rect = rect
        if len(self.rect) == 4:
            self.degree = 0
            self.left, self.up, self.width, self.height = self.rect
            self.right = self.left + self.width
            self.down = self.up + self.height
            self.rect_box = np.int0(((self.left, self.up),
                                     (self.right, self.up),
                                     (self.right, self.down),
                                     (self.left, self.down)))
        else:
            self.degree = rect[2]
            self.width = int(rect[1][0])
            self.height = int(rect[1][1])
            self.rect_box = np.int0(cv2.boxPoints(rect))
            self.points = self.rect_box.T
            self.left = abs(min(self.points[0]))
            self.up = abs(min(self.points[1]))
            self.right = abs(max(self.points[0]))
            self.down = abs(max(self.points[1]))

    def min2bnd(self):
        """
        :return: Given a min rect return a bound rectangle object
        """
        left = abs(self.left)
        up = abs(self.up)
        width = abs(self.right - self.left)
        height = abs(self.down - self.up)
        return Rect([left, up, width, height])

def load_img(fn):
    """
    :param fn: File name of image
    :return: CvImage of that file
    """
    return CvImage(cv2.imread(fn))


def test():
    fn = "../resources/demo_00.jpg"
    img = load_img(fn)
    print img.shape
    gray = img.get_gray()
    print gray.shape
    # img = cv2.imread(fn)
    bin_img = img.get_bin()
    print bin_img.shape
    # bin_img.show("bin")
    op_img = bin_img.get_open()
    # op_img.show("open")
    cl_img = op_img.get_close()
    # cl_img.show("close")
    iv_img = cl_img.get_inverse()
    cnt = iv_img.get_cnts()
    print type(img)
    # img.draw_rect("rect", cnt)
    # cnts = cl_img.get_cnts()
    # print cnts
    # blur = img.get_blur(g_core=(13, 13))
    # blur.show("blur")
    # gray = img.get_gray()
    # gray.show("gray")


    # # img = load_img(fn)
    # # print dir(img)
    # # img.show("test")
    # arr = CvImage(img[1:2, 2:3])
    #
    #
    # new_img = CvImage(arr)
    # img[1:2, 2:3] = 1
    # img.show("img")
    # new_img.show("new")


if __name__ == "__main__":
    test()
