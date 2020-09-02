import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

from loglib import loglib

MASK5 = 0b011111
MASK6 = 0b111111


class imagelib:
    logger = loglib(__name__)

    @staticmethod
    def rgba2rgb888(rgba, width: int, height: int):
        """
        RGBA to RGB888.

        Parameters
        ----------
        rgba : bytes or bytearray
            rgba image data
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
            if type(rgba) is bytes:
                rgba = np.frombuffer(rgba, dtype=np.uint8).reshape(height, width, 4)
            elif type(rgba) is bytearray:
                rgba = np.array(rgba, dtype=np.uint8).reshape(height, width, 4)
            rgb888 = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
        except ValueError as e:
            imagelib.logger.error('ValueError: {}'.format(e))

        return rgb888

    @staticmethod
    def rgb8882rgba(rgb888, width: int, height: int):
        """
        RGB888 to RGBA.

        Parameters
        ----------
        rgb888 : bytes or bytearray
            rgb888 image data
        width : int
            width of image
        height : int
            height of image

        Returns
        -------
        np.ndarray
            rgba image data
        """

        rgba = None

        try:
            if type(rgb888) is bytes:
                rgb888 = np.frombuffer(rgb888, dtype=np.uint8).reshape(height, width, 3)
            elif type(rgb888) is bytearray:
                rgb888 = np.array(rgb888, dtype=np.uint8).reshape(height, width, 3)
            rgba = cv2.cvtColor(rgb888, cv2.COLOR_RGB2RGBA)
        except ValueError as e:
            imagelib.logger.error('ValueError: {}'.format(e))

        return rgba

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
    def cv2crop(image: np.ndarray, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        """
        image crop.

        ps. cv2 only accepts RGB888 format.

        Parameters
        ----------
        image : np.ndarray
            image buffer
        x : int
            x
        y : int
            y
        width : int
            width
        height : int
            height

        Returns
        -------
        np.ndarray
            crop buffer
        """
        # grab the image size
        (h, w) = image.shape[:2]

        # if both the width and height are 0, then return the original image
        if width == 0 or width > w or height == 0 or height > h:
            imagelib.logger.error('width == 0 or width > w or height == 0 or height > h , ignore!!!')
            return image

        # convert x, y to int to avoid float type
        x = int(x)
        y = int(y)

        # crop the image
        crop = image[y:y + height, x:x + width]

        # return the resized image
        return crop

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
    def buf2rgba(buffer, width: int, height: int, channel: int):
        """
        convert buffer to rgba.

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
            rgba image data
        """

        rgba = None
        if channel == 1:
            if type(buffer) is bytes:
                image = Image.frombytes('L', (width, height), buffer, 'raw')
            elif type(buffer) is bytearray:
                image = Image.frombytes('L', (width, height), bytes(buffer), 'raw')
            rgba = image.convert('RGBA')
            rgba = np.array(rgba)
        elif channel == 2:
            buffer = imagelib.rgb5652rgb888(buffer, width, height)
            rgba = imagelib.rgb8882rgba(buffer, width, height)
        elif channel == 3:
            rgba = imagelib.rgb8882rgba(buffer, width, height)
        elif channel == 4:
            rgba = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
        return rgba

    @staticmethod
    def buf2rgb888(buffer, width: int, height: int, channel: int):
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
            if type(buffer) is bytes:
                image = Image.frombytes('L', (width, height), buffer, 'raw')
            elif type(buffer) is bytearray:
                image = Image.frombytes('L', (width, height), bytes(buffer), 'raw')
            rgb888 = image.convert('RGB')
            rgb888 = np.array(rgb888)
        elif channel == 2:
            rgb888 = imagelib.rgb5652rgb888(buffer, width, height)
        elif channel == 3:
            rgb888 = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 3)
        elif channel == 4:
            rgb888 = imagelib.rgba2rgb888(buffer, width, height)
        return rgb888

    @staticmethod
    def buf2rgb565(buffer, width: int, height: int, channel: int):
        """
        convert buffer to rgb565.

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
            rgb565 image data
        """

        rgb565 = None
        if channel == 1:
            if type(buffer) is bytes:
                image = Image.frombytes('L', (width, height), buffer, 'raw')
            elif type(buffer) is bytearray:
                image = Image.frombytes('L', (width, height), bytes(buffer), 'raw')
            rgb888 = image.convert('RGB')
            rgb888 = np.array(rgb888)
            rgb565 = imagelib.rgb8882rgb565(rgb888)
        elif channel == 2:
            pass
        elif channel == 3:
            rgb565 = imagelib.rgb8882rgb565(buffer)
        elif channel == 4:
            buffer = imagelib.rgba2rgb888(buffer, width, height)
            rgb565 = imagelib.rgb8882rgb565(buffer)

        # bytes to np.ndarray
        rgb565 = np.frombuffer(rgb565, dtype=np.uint8).reshape(height, width, 2)
        return rgb565

    @staticmethod
    def im2rgba(file: str, resize_width: int = 0, resize_height: int = 0):
        """
        convert image (jpg,bmp...etc) to rgba.

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
            - buf (bytes): image rgba data
        """

        # get image info
        pilimage = imagelib.pilopen(file)

        if pilimage is None:
            imagelib.logger.error('pilimage is None!!!')
            return 0, 0, 0, None, None

        image_info = dict({'format': pilimage.format, 'size': pilimage.size, 'mode': pilimage.mode})
        imagelib.logger.info(image_info)

        # assign image size and channel
        (width, height) = pilimage.size
        channel = len(pilimage.getbands())

        # resize image when both w/h are not 0
        if resize_width != 0 and resize_height != 0:
            (height, width) = (resize_height, resize_width)
            pilimage = pilimage.resize((resize_width, resize_height))

        # Modes: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes
        if pilimage.mode == 'RGBA':
            pass
        else:
            pilimage = pilimage.convert('RGBA')

        # convert to ndarray
        buf = np.array(pilimage)
        if buf is None:
            imagelib.logger.error('convert image fail!!!')
            return 0, 0, 0, None, None

        return width, height, 4, image_info, buf.tobytes()

    @staticmethod
    def im2rgb888(file: str, resize_width: int = 0, resize_height: int = 0):
        """
        convert image (jpg,bmp...etc) to rgb888.

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
            - buf (bytes): image rgb888 data
        """

        # get image info
        pilimage = imagelib.pilopen(file)

        if pilimage is None:
            imagelib.logger.error('pilimage is None!!!')
            return 0, 0, 0, None, None

        image_info = dict({'format': pilimage.format, 'size': pilimage.size, 'mode': pilimage.mode})
        imagelib.logger.info(image_info)

        # assign image size and channel
        (width, height) = pilimage.size
        channel = len(pilimage.getbands())

        # resize image when both w/h are not 0
        if resize_width != 0 and resize_height != 0:
            (height, width) = (resize_height, resize_width)
            pilimage = pilimage.resize((resize_width, resize_height))

        # Modes: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes
        if pilimage.mode == 'RGB':
            pass
        else:
            pilimage = pilimage.convert('RGB')

        # convert to ndarray
        buf = np.array(pilimage)
        if buf is None:
            imagelib.logger.error('convert image fail!!!')
            return 0, 0, 0, None, None

        return width, height, 3, image_info, buf.tobytes()

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

        # get RGB888 first
        width, height, _, image_info, buf888 = imagelib.im2rgb888(file, resize_width, resize_height)

        # convert to ndarray
        rgb888 = np.frombuffer(buf888, dtype=np.uint8).reshape(height, width, 3)
        if rgb888 is None:
            imagelib.logger.error('convert image fail!!!')
            return 0, 0, 0, None, None

        # convert to RGB565
        buf = imagelib.rgb8882rgb565(rgb888)

        return width, height, 2, image_info, buf

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

    @staticmethod
    def pilcrop(image: np.ndarray, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        """
        image crop.

        Parameters
        ----------
        image : np.ndarray
            image buffer
        x : int
            x
        y : int
            y
        width : int
            width
        height : int
            height

        Returns
        -------
        np.ndarray
            crop buffer
        """
        # grab the image size
        (h, w) = image.shape[:2]

        # if both the width and height are 0, then return the original image
        if width == 0 or width > w or height == 0 or height > h:
            imagelib.logger.error('width == 0 or width > w or height == 0 or height > h , ignore!!!')
            return image

        # crop the image
        image = Image.fromarray(image)
        box = (x, y, x + width, y + height)
        crop = image.crop(box)

        # return the resized image
        return np.array(crop)

    @staticmethod
    def rgb8882yuv(rgb):
        """
        reference: https://gist.github.com/Quasimondo/c3590226c924a06b276d606f4f189639
        input is a RGB numpy array with shape (height,width,3), can be uint,int, float or double,
        values expected in the range 0..255
        output is a double YUV numpy array with shape (height,width,3), values in the range 0..255
        """
        m = np.array([[0.29900, -0.16874, 0.50000],
                      [0.58700, -0.33126, -0.41869],
                      [0.11400, 0.50000, -0.08131]])

        yuv = np.dot(rgb, m)
        yuv[:, :, 1:] += 128.0
        return yuv

    @staticmethod
    def yuv2rgb888(yuv):
        """
        reference: https://gist.github.com/Quasimondo/c3590226c924a06b276d606f4f189639
        input is an YUV numpy array with shape (height,width,3) can be uint,int, float or double,
        values expected in the range 0..255
        output is a double RGB numpy array with shape (height,width,3), values in the range 0..255
        """
        m = np.array([[1.0, 1.0, 1.0],
                      [-0.000007154783816076815, -0.3441331386566162, 1.7720025777816772],
                      [1.4019975662231445, -0.7141380310058594, 0.00001542569043522235]])

        rgb = np.dot(yuv, m)
        rgb[:, :, 0] -= 179.45477266423404
        rgb[:, :, 1] += 135.45870971679688
        rgb[:, :, 2] -= 226.8183044444304
        return rgb

    @staticmethod
    def folder_crop_resize(folder: str, prefix_name: str, w_resize: int, h_resize: int):
        """
        test only, not handle exception.
        """
        # create folder if not exist
        convert_folder = f'{folder}/convert/'
        import os
        if not os.path.isdir(convert_folder):
            import pathlib
            pathlib.Path(convert_folder).mkdir(parents=True, exist_ok=True)

        files = []

        # get all files
        import os
        for r, d, f in os.walk(folder):
            # append full path with file name
            full_paths = [os.path.join(r, file) for file in f]
            files.extend(full_paths)

        # crop/resize each file
        for i, file in enumerate(files):
            file_new = f'{convert_folder}{prefix_name}_{w_resize}x{h_resize}_{(i + 1):03}'
            imagelib.file_crop_resize(file, file_new, w_resize, h_resize)

    @staticmethod
    def file_crop_resize(file: str, file_new: str, w_resize: int, h_resize: int):
        """
        test only, not handle exception.
        """
        w, h, c, image_info, rgb888 = imagelib.im2rgb888(file)

        rgb888 = np.frombuffer(rgb888, dtype=np.uint8).reshape(h, w, 3)

        if w > h:
            x = int((w - h) / 2)
            y = 0
            w = h
            rgb888 = imagelib.cv2crop(rgb888, x, y, w, h)
        elif w < h:
            x = 0
            y = int((h - w) / 2)
            h = w
            rgb888 = imagelib.cv2crop(rgb888, x, y, w, h)

        rgb888 = imagelib.cv2resize(rgb888, w_resize, h_resize)
        cv2.imwrite(f'{file_new}.jpg', rgb888[:, :, ::-1])  # convert rgb888 to bgr888 for cv2 save image
        rgb565 = imagelib.rgb8882rgb565(rgb888)

        from filelib import filelib
        filelib.file_write_binary(rgb565, f'{file_new}.raw')
