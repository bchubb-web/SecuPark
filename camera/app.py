import cv2
import numpy as np
from numba import jit, cuda
import time
import json

from SQL import sql_handler
from detection import rect_detect, anpr_handler


# HANDLES MAIN VIDEO FEED
class feed_handler:

    _status: str

    # bounding values for yellow
    y_lower = [16, 100, 0]
    y_upper = [40, 255, 255]
    # bounding values for white
    w_lower = [0, 0, 200]  # light grey
    w_upper = [359, 40, 255]  # white

    def __init__(self: object, cam: int, number: str):
        # init the data for the camera, store as attributes

        self._CAMERA = cam
        self._ID = number
        self._stream = cv2.VideoCapture(cam)

    def set_frame(self: object) -> None:
        # get the video input from webcam
        ret, frame = self._stream.read()
        height, width = frame.shape[:2]

        # resize the frame
        frame = cv2.resize(frame, (400, int((height*400)/width)))
        self._frame = frame

    def detect_motion(self: object) -> bool:
        return True

    def filter_frame(self: object) -> None:
        hsv_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV)  # convert frame to hsv
        y_mask = cv2.inRange(hsv_frame, np.array(self.y_lower), np.array(self.y_upper))  # genrtate yellow mask
        w_mask = cv2.inRange(hsv_frame, np.array(self.w_lower), np.array(self.w_upper))  # generate white mask
        mask = cv2.bitwise_or(y_mask, w_mask)  # bitwise or to combine areas of both masks
        result = cv2.bitwise_and(self._frame, self._frame, mask=mask)  # apply the mask to the frame
        self._f_frame = result

    def thresh_frame(self: object) -> None:
        grey = cv2.cvtColor(self._f_frame, cv2.COLOR_BGR2GRAY)  # convert to black and white
        blurred = cv2.GaussianBlur(grey, (5, 5), 0)  # blur the details
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]  # find threshhold of the areas
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        self._t_frame = thresh

    def loop(self: object, fps: int) -> bool:
        prev = 0
        while True:
            time_elapsed = time.time() - prev
            self.set_frame()

            if time_elapsed > 1./fps:
                prev = time.time()
                self.filter_frame()
                self.thresh_frame()
                self.output(self.detect_motion())
                # print(1./time_elapsed)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return False

    def output(self: object, motion: bool) -> None:
        if motion:
            cv2.imshow("frame", self._frame)
            anpr = anpr_handler(True, "tits")
            b64 = anpr.endcode_b64(self._frame)

            cv2.imshow("f_frame", self._f_frame)
            cv2.imshow("t_frame", self._t_frame)

            test = rect_detect()
            master = test.detect(self._t_frame, self._frame)
            cv2.imshow("DETECTED", master)

        else:
            cv2.imshow("no plate found", self._frame)


def main():

    config = open("conf.json")
    conf = json.load(config)

    sql = sql_handler(conf["SQL"])
    if sql.connect():

        feed = feed_handler(conf["camera"], "id")
        fps = conf["fps"]

        if not feed.loop(fps):
            feed._stream.release()
            cv2.destroyAllWindows()
            sql.close()


if __name__ == '__main__':
    main()
