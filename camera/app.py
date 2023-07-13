import cv2
import numpy as np
from numba import jit, cuda
import time


from feed import feed_handler


def main():
    feed = feed_handler(0)
    if not feed.loop(24):
        feed._stream.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
