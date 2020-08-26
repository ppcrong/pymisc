from threading import Thread, Lock

import cv2

from loglib import loglib


class vslib:
    """
    The library for camera video stream.

    reference: https://gist.github.com/allskyee/7749b9318e914ca45eb0a1000a81bf56
    """

    thread = None
    logger = loglib(__name__)

    def __init__(self, src: int = 0, width: int = 640, height: int = 480):
        self.src = src
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            self.logger.warning('already started!!!')
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = None
        if self.frame is not None:
            frame = self.frame.copy()
        else:
            self.logger.error('frame is None!!!')
        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def is_opened(self):
        return self.stream.isOpened()

    def release(self):
        self.stream.release()

    def getinfo(self):
        w = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = self.stream.get(cv2.CAP_PROP_FPS)
        return w, h, fps

    # region [with]
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info('release')
        self.release()
    # endregion [with]


if __name__ == "__main__":
    import datetime

    with vslib() as vs:
        if not vs.is_opened():
            print(f'open source {vs.src} fail!!!')
        else:
            vs.start()
            w, h, fps = vs.getinfo()
            print(f'w: {w}, h: {h}, fps: {fps}')
            print()
            while True:
                time_start = datetime.datetime.now()
                frame = vs.read()
                time_end = datetime.datetime.now()
                print(f'time: {(time_end - time_start).total_seconds() * 1000 : 0.3f} ms')
                cv2.imshow('webcam', frame)
                if cv2.waitKey(1) == 27:
                    break

            # Number of frames to capture
            num_frames = 120
            # start time
            start = datetime.datetime.now()
            # grab frames
            for i in range(0, num_frames):
                frame = vs.read()
            # end time
            end = datetime.datetime.now()
            # time elapsed
            seconds = (end - start).total_seconds()
            # fps
            fps = num_frames / seconds
            print(f'fps: {fps : 0.3f}')

            vs.stop()
            cv2.destroyAllWindows()
