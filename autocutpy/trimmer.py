#! /usr/bin/env python
# coding=utf-8

from cvimage import *
from PIL import Image


class Trimmer(object):
    """
    Automatically cut and trim the image.
    """

    def __init__(self, img, grn=5):
        """
        :param img: A CvImage object
        :param grn: The graininess of trimmer. 0 - 5, the graininess larger, the trimmed photos larger(Maybe).
        """
        if grn == 0:
            self.__grn = 0
        else:
            self.__grn = grn * 10 + 200
        self.__img = img
        self.__min_rects = None
        self.__bnd_rects = None

    def get_min_rects(self):
        """
        :return: The rects of the photos in the image
        """
        if not self.__min_rects:
            bin_img = self.__img.get_bin(self.__grn)
            op_img = bin_img.get_open()
            cl_img = op_img.get_close()
            iv_img = cl_img.get_inverse()
            self.__min_rects = [rect for rect in iv_img.get_min_rects() if rect.height * rect.width > 50000]
        return self.__min_rects

    def get_bnd_rects(self):
        """
        :return: The rects of the photos in the image
        """
        if not self.__bnd_rects:
            bin_img = self.__img.get_bin(self.__grn)
            op_img = bin_img.get_open()
            cl_img = op_img.get_close()
            iv_img = cl_img.get_inverse()
            self.__bnd_rects = [rect for rect in iv_img.get_bnd_rects() if rect.height * rect.width > 50000]
        return self.__bnd_rects

    def cut_bnd(self, rect, min_rect):
        """
        :param min_rect: A min rectangle Rect() object.
        :param rect: A bounding rectangle Rect() object.
        :return: A piece of the photo in the rectangle. Rotate by PIL Lib. With Anti-aliasing, smoother.
        """
        roi = self.__img[rect.up: rect.down, rect.left: rect.right]
        # print "debug [rect.up: rect.down, rect.left: rect.right] = ", [rect.up, rect.down, rect.left, rect.right]
        # print "debug min = ", [min_rect.up, min_rect.down, min_rect.left, min_rect.right]
        pil_img = Image.fromarray(roi)

        # minimal the rotational angle
        if min_rect.degree > 45:
            angle = min_rect.degree - 90
        elif min_rect.degree < -45:
            angle = 90 + min_rect.degree
        else:
            angle = min_rect.degree

        # pil_img = pil_img.rotate(angle, Image.BICUBIC)
        real_size = pil_img.size
        region = pil_img.convert('RGBA').rotate(angle, Image.BICUBIC, 1)
        ro_img = Image.new(pil_img.mode, real_size, color="white")
        left, up = ((ro_img.size[0] - region.size[0]) // 2, (ro_img.size[1] - region.size[1]) // 2)
        ro_img.paste(region, (left, up), region)
        mat = np.array(ro_img)

        # Sometimes min_rect.height and min_rect.width were exchanged
        if (rect.height < rect.width and min_rect.height > min_rect.width) or \
                (rect.height > rect.width and min_rect.height < min_rect.width):
            min_rect.height, min_rect.width = min_rect.width, min_rect.height

        up = int((rect.height - min_rect.height) / 2)
        left = int((rect.width - min_rect.width) / 2)

        return CvImage(mat[up: rect.height - up, left: rect.width - left])

    def cut_min(self, rect):
        """
        :param rect: A Rect() object.
        :return: A piece of the photo in the rectangle.
        """
        center, (width, height), theta = rect.rect
        theta *= np.pi / 180

        c_x = (np.cos(theta), np.sin(theta))
        c_y = (-np.sin(theta), np.cos(theta))
        x = center[0] - c_x[0] * (width / 2) - c_y[0] * (height / 2)
        y = center[1] - c_x[1] * (width / 2) - c_y[1] * (height / 2)

        matrix = np.array([[c_x[0], c_y[0], x],
                           [c_x[1], c_y[1], y]])

        mat = cv2.warpAffine(self.__img, matrix, (int(width), int(height)), flags=cv2.WARP_INVERSE_MAP,
                             borderMode=cv2.BORDER_REPLICATE)
        return CvImage(mat)

    def trim(self, rects=None):
        """
        :param rects: Rect() objects contain the pictures
        :return: Pictures in the rectangles.
        """
        if not rects:
            rects = self.get_min_rects()
        result = []
        for rect in rects:
            result.append(self.cut_min(rect))
        return result

    def trim2(self):
        """
        :param rects: Rect() objects contain the pictures
        :return: Pictures in the rectangles.
        """
        min_rects = self.get_min_rects()
        bnd_rects = [rect.min2bnd() for rect in min_rects]
        # print "debug bnd_rects", bnd_rects[0].up
        result = []
        for bnd_rect, min_rect in zip(bnd_rects, min_rects):
            piece = self.cut_bnd(bnd_rect, min_rect)
            result.append(piece)
        return result


def test():
    # fn = r"C:\Users\MaGiCmAn\Desktop\img-170213094812-001.jpg"
    fn = r"C:\Users\MaGiCmAn\Desktop\newdemo.jpg"
    img = load_img(fn)
    trm = Trimmer(img)
    photos1 = trm.trim()
    photos2 = trm.trim2()
    for idx in xrange(len(photos2)):
        photos2[idx].show(str(idx))
        pn = fn[: -4] + '_' + str(idx)
        photos2[idx].save(pn + "_2.jpg")
        # photos1[idx].save(pn + "_1.jpg")
        # print "debug photos2.shape = ", photos2[idx].shape


if __name__ == "__main__":
    test()
