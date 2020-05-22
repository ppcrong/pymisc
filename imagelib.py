import cv2
import numpy as np

from printlib import printlib

MASK5 = 0b011111
MASK6 = 0b111111


class imagelib:

    @staticmethod
    def rgb5652rgb888(rgb565, width: int, height: int):
        """
        RGB565 to RGB888.

        reference: https://tinyurl.com/y8fqbvfm

        Parameters
        ----------
        rgb565 : bytes or bytearray
            rgb565 image data
        width : int
            width of image
        height : int
            height of image

        Returns
        -------
        bytearray
            rgb888 image data
        """

        # convert to ndarray (height, width, channel)
        if type(rgb565) is bytes:
            rgb888 = np.frombuffer(rgb565, dtype=np.uint8).reshape(height, width, 2)
        elif type(rgb565) is bytearray:
            rgb888 = np.array(rgb565, dtype=np.uint8).reshape(height, width, 2)
        # convert WxHx2 array of uint8 into WxH array of uint16
        byte0 = rgb888[:, :, 0].astype(np.uint16)
        byte1 = rgb888[:, :, 1].astype(np.uint16)
        rgb888 = (byte0 | byte1 << 8)
        # convert 565 to 888
        b8 = (rgb888 & MASK5) << 3
        g8 = ((rgb888 >> 5) & MASK6) << 2
        r8 = ((rgb888 >> (5 + 6)) & MASK5) << 3
        rgb888 = np.dstack((r8, g8, b8)).astype(np.uint8)

        return rgb888

    @staticmethod
    def rgb8882rgb565(rgb888: np.ndarray):
        """
        RGB888 to RGB565.

        reference: https://tinyurl.com/yb5clfez

        Parameters
        ----------
        rgb888 : np.ndarray
            rgb888 image data

        Returns
        -------
        bytes
            rgb565 image data
        """

        r5 = (rgb888[..., 0] >> 3).astype(np.uint16) << 11
        g6 = (rgb888[..., 1] >> 2).astype(np.uint16) << 5
        b5 = (rgb888[..., 2] >> 3).astype(np.uint16)
        rgb565 = r5 | g6 | b5

        return rgb565.tobytes()

    @staticmethod
    def bgr8882rgb565(bgr888: np.ndarray):
        """
        RGB888 to RGB565.

        reference: https://tinyurl.com/yb5clfez

        Parameters
        ----------
        bgr888 : np.ndarray
            rgb888 image data

        Returns
        -------
        bytes
            rgb565 image data
        """

        r5 = (bgr888[..., 2] >> 3).astype(np.uint16) << 11
        g6 = (bgr888[..., 1] >> 2).astype(np.uint16) << 5
        b5 = (bgr888[..., 0] >> 3).astype(np.uint16)
        rgb565 = r5 | g6 | b5

        return rgb565.tobytes()

    @staticmethod
    def cv2imread(img_name: str, cvt_rgb=True):
        """
         read image file.

        Parameters
        ----------
        img_name : str
            image name
        cvt_rgb : bool
            if convert to RGB

        Returns
        -------
        np.ndarray
            image buffer
        """

        buf = None

        while True:
            # printlib.print('file_name: {}'.format(file_name))
            if not img_name or img_name == '':
                printlib.print('file_name is None or empty!!!')
                break;

            buf = cv2.imread(img_name)
            if cvt_rgb:
                buf = cv2.cvtColor(buf, cv2.COLOR_BGR2RGB)
            break;

        return buf

    @staticmethod
    def cv2resize(image, width=None, height=None, inter=cv2.INTER_AREA):
        """
        image resize and keep the aspect rate of the original image when width is None or height is None.

        ps. cv2 only accepts RGB888 format.

        reference: https://tinyurl.com/ych3b4mr

        Parameters
        ----------
        image : np.ndarray
            image buffer
        width : int
            width
        height : int
            height
        inter : int
            interpolation

        Returns
        -------
        np.ndarray
            resized buffer
        """
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        elif height is None:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # both height/width are not None, it won't keep aspect ratio
        else:
            dim = (width, height)

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized
