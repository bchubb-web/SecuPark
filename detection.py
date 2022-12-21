import cv2
import json
import base64
from matplotlib.pyplot import contour
import numpy as np


class anpr_handler:
    _endpoint = "https://www."
    
    def __init__(self:object, frame:any, key:str):
        self._api_key = key

    def get_plate(self:object) -> str:
        return self._plate

    def get_api_key(self:object) -> str:
        return self._api_key

    def endcode_b64(self:object, frame) -> str:
        retval, buffer_img= cv2.imencode('.jpg', frame)
        data = base64.b64encode(buffer_img).decode("UTF-8")
        return data


class rect_detect:

    def __init__(self) -> None:
        pass


    def detect(self:object, grey:any, master:any) -> any:
        #grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, thrash = cv2.threshold(grey,240,255, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
            
            x,y,w,h = cv2.boundingRect(approx)
            ar = float(w)/h
            if len(approx) == 4 and cv2.arcLength(contour, True) > 100 and ar >= 1:
                cv2.drawContours(master, [approx], 0, (0,255,0),2)

        return master



def main():
    config = open("conf.json")
    conf = json.load(config)
    stream = cv2.VideoCapture(conf["camera"])
    rect = rect_detect()

    skip = True

    while True:
        ret,frame = stream.read()

        frame = rect.test(frame)

        cv2.imshow("Detection Test", frame)
        if cv2.waitKey(1)&0xff == ord('q'):
            break#press Q to exit the program

    stream.release()#stop video capture
    cv2.destroyAllWindows()#close window

if __name__ == '__main__':
    main()