import numpy as np

MASK5 = 0b011111
MASK6 = 0b111111


class imagelib:

    @staticmethod
    def rgb5652888(rgb565, width: int, height: int):
        """
        RGB565 to RGB888.

        reference: https://tinyurl.com/yb5clfez

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
    def rgb8882565(rgb888: bytearray):
        """
        RGB888 to RGB565.

        reference: https://tinyurl.com/y8fqbvfm

        Parameters
        ----------
        rgb888 : bytearray
            rgb888 image data

        Returns
        -------
        bytearray
            rgb565 image data
        """

        r5 = (rgb888[..., 2] >> 3).astype(np.uint16) << 11
        g6 = (rgb888[..., 1] >> 2).astype(np.uint16) << 5
        b5 = (rgb888[..., 0] >> 3).astype(np.uint16)
        rgb565 = r5 | g6 | b5

        return rgb565
