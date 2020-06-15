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

    def __init__(self, src=0, width=640, height=480):
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
        if self.frame:
            frame = self.frame.copy()
        else:
            self.logger.error('frame is None!!!')
        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()


if __name__ == "__main__":
    vs = vslib().start()
    while True:
        frame = vs.read()
        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == 27:
            break

    vs.stop()
    cv2.destroyAllWindows()
