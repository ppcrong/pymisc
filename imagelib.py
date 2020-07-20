import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

from loglib import loglib

MASK5 = 0b011111
MASK6 = 0b111111


class imagelib:
    logger = loglib(__name__)

    @staticmethod
    def rgb88882rgb888(rgb8888, width: int, height: int):
        """
        RGB8888 (RGBA) to RGB888.

        Parameters
        ----------
        rgb8888 : bytes or bytearray
            rgb8888 image data
        width : int
            width of image
        height : int
            height of image

        Returns
        -------
        np.ndarray
            rgb888 image data
        """

        rgb888 = None

        try:
            if type(rgb8888) is bytes:
                rgba = np.frombuffer(rgb8888, dtype=np.uint8).reshape(height, width, 4)
            elif type(rgb8888) is bytearray:
                rgba = np.array(rgb8888, dtype=np.uint8).reshape(height, width, 4)
            rgb888 = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
        except ValueError as e:
            imagelib.logger.error('ValueError: {}'.format(e))

        return rgb888

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
        np.ndarray
            rgb888 image data
        """

        rgb888 = None

        try:
            # convert to ndarray (height, width, channel)
            if type(rgb565) is bytes:
                rgb565 = np.frombuffer(rgb565, dtype=np.uint8).reshape(height, width, 2)
            elif type(rgb565) is bytearray:
                rgb565 = np.array(rgb565, dtype=np.uint8).reshape(height, width, 2)
            # convert WxHx2 array of uint8 into WxH array of uint16
            byte0 = rgb565[:, :, 0].astype(np.uint16)
            byte1 = rgb565[:, :, 1].astype(np.uint16)
            rgb565 = (byte0 | byte1 << 8)
            # convert 565 to 888
            b8 = (rgb565 & MASK5) << 3
            g8 = ((rgb565 >> 5) & MASK6) << 2
            r8 = ((rgb565 >> (5 + 6)) & MASK5) << 3
            rgb888 = np.dstack((r8, g8, b8)).astype(np.uint8)
        except ValueError as e:
            imagelib.logger.error('ValueError: {}'.format(e))

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
        BGR888 to RGB565.

        reference: https://tinyurl.com/yb5clfez

        Parameters
        ----------
        bgr888 : np.ndarray
            bgr888 image data

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
    def cv2imread(img_name: str, cvt_rgb: bool = True):
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
            # imagelib.logger.info('file_name: {}'.format(file_name))
            if not img_name or img_name == '':
                imagelib.logger.error('file_name is None or empty!!!')
                break

            buf = cv2.imread(img_name)
            if cvt_rgb:
                buf = cv2.cvtColor(buf, cv2.COLOR_BGR2RGB)
            break

        return buf

    @staticmethod
    def cv2resize(image: np.ndarray, width: int = 0, height: int = 0, inter: int = cv2.INTER_AREA):
        """
        image resize and keep the aspect rate of the original image when width is 0 or height is 0.

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
        # grab the image size
        (h, w) = image.shape[:2]

        # if both the width and height are 0, then return the original image
        if width == 0 and height == 0:
            return image

        # check to see if the width is 0
        if width == 0:
            # calculate the ratio of the height and construct the dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is 0
        elif height == 0:
            # calculate the ratio of the width and construct the dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # both height/width are not 0, it won't keep aspect ratio
        else:
            dim = (width, height)

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    @staticmethod
    def getiminfo(file: str):
        """
        get image (jpg,bmp...etc) info (width, height, channel).

        Parameters
        ----------
        file : str
            file name

        Returns
        -------
        tuple : a tuple containing:
            - width (int): image width
            - height (int): image height
            - channel (int): image channel
        """

        # get image info
        pilimage = imagelib.pilopen(file)

        if pilimage is None:
            imagelib.logger.error('pilimage is None!!!')
            return 0, 0, 0

        # assign image size
        (width, height) = pilimage.size

        # assign channel
        channel = len(pilimage.getbands())

        return width, height, channel

    @staticmethod
    def im2rgb888(buffer, width: int, height: int, channel: int):
        """
        convert buffer to rgb888.

        Parameters
        ----------
        buffer : bytes or bytearray
            image data
        width : int
            width of image
        height : int
            height of image
        channel : int
            color channel

        Returns
        -------
        np.ndarray
            rgb888 image data
        """

        rgb888 = None
        if channel == 1:
            return NotImplemented
        elif channel == 2:
            rgb888 = imagelib.rgb5652rgb888(buffer, width, height)
        elif channel == 3:
            rgb888 = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 3)
        elif channel == 4:
            rgb888 = imagelib.rgb88882rgb888(buffer, width, height)
        return rgb888

    @staticmethod
    def im2rgb565(file: str, resize_width: int = 0, resize_height: int = 0):
        """
        convert image (jpg,bmp...etc) to rgb565.

        Parameters
        ----------
        file : str
            file name
        resize_width : int
            resize width, resize when both w/h are not 0
        resize_height : int
            resize height, resize when both w/h are not 0

        Returns
        -------
        tuple : a tuple containing:
            - width (int): image width
            - height (int): image height
            - channel (int): image channel
            - image_info (dict): image info (format, size, mode)
            - buf (bytes): image rgb565 data
        """

        # get image info
        pilimage = imagelib.pilopen(file)

        if pilimage is None:
            imagelib.logger.error('pilimage is None!!!')
            return 0, 0, None, None

        image_info = dict({'format': pilimage.format, 'size': pilimage.size, 'mode': pilimage.mode})
        imagelib.logger.info(image_info)

        # assign image size and channel
        (width, height) = pilimage.size
        channel = len(pilimage.getbands())

        # convert to ndarray
        buf = np.array(pilimage)
        if buf is None:
            imagelib.logger.error('convert image fail!!!')
            return 0, 0, None, None

        # [TODO] need to check channels for 1. cv2 resize and 2. convert rgb565 below

        # resize image when both w/h are not 0
        if resize_width != 0 and resize_height != 0:
            (height, width) = (resize_height, resize_width)
            buf = imagelib.cv2resize(buf, width, height)

        # convert rgb888 to rgb565
        if channel > 2:
            # RGB888 or RGBA
            buf = imagelib.rgb8882rgb565(buf)
        else:
            # RGB565
            buf = buf.tobytes()

        return width, height, channel, image_info, buf

    @staticmethod
    def pilopen(img_name: str):
        """
         read image file.

        Parameters
        ----------
        img_name : str
            image name

        Returns
        -------
        PIL.Image.Image
            pil image object
        """

        buf = None

        while True:
            # imagelib.logger.info('file_name: {}'.format(file_name))
            if not img_name or img_name == '':
                imagelib.logger.error('file_name is None or empty!!!')
                break

            try:
                buf = Image.open(img_name)
            except FileNotFoundError as e:
                imagelib.logger.error('FileNotFoundError: {}'.format(e))
            except UnidentifiedImageError as e:
                imagelib.logger.error('UnidentifiedImageError: {}'.format(e))
            except ValueError as e:
                imagelib.logger.error('ValueError: {}'.format(e))

            break

        return buf

    @staticmethod
    def pilresize(image: np.ndarray, width: int = 0, height: int = 0):
        """
        image resize and keep the aspect rate of the original image when width is 0 or height is 0.

        reference: https://tinyurl.com/ych3b4mr

        Parameters
        ----------
        image : np.ndarray
            image buffer
        width : int
            width
        height : int
            height

        Returns
        -------
        np.ndarray
            resized buffer
        """
        # grab the image size
        (h, w) = image.shape[:2]

        # if both the width and height are 0, then return the original image
        if width == 0 and height == 0:
            return image

        # check to see if the width is 0
        if width == 0:
            # calculate the ratio of the height and construct the dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is 0
        elif height == 0:
            # calculate the ratio of the width and construct the dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # both height/width are not 0, it won't keep aspect ratio
        else:
            dim = (width, height)

        # resize the image
        image = Image.fromarray(image)
        resized = image.resize(dim)

        # return the resized image
        return np.array(resized)
