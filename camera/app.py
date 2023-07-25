import cv2

from feed import feed_handler


def main():
    feed = feed_handler(0)
    while feed.set_frame():
        feed.filter_frame()
        feed.thresh_frame()
        feed.output(self.detect_motion())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    feed._stream.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
