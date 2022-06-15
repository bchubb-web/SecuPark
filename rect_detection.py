import cv2
class rect_detector:

    def __init__(self) -> None:
        pass

    def plate(self,c) -> any:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c,0.04*peri, True)

        if len(approx) == 4:
            (x,y,w,h) = cv2.boundingRect(approx)
            aspect_ratio = w/float(h)

            if aspect_ratio < 1.5:
                return False
            return True
        return False