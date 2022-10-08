import cv2
from datetime import datetime
import mysql.connector
import requests
#from google.cloud import vision_vlp3beta1 as vision
import numpy as np
import imutils
import time
import json
import re
from rect_detection import rect_detector
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.object_detection import non_max_suppression
import base64

class feed_handler:
    _status: str
    #bounding values for yellow
    y_lower = [16, 120, 0]
    y_upper = [40,255,255]
    #bounding values for white
    w_lower = [0,0,168]
    w_upper = [359,5,255]

    def __init__(self:object, cam:int ,number:str):# init the data for the camera, store as attributes
        self._CAMERA = cam
        self._ID = number
        self._stream = cv2.VideoCapture(cam)

    def set_frame(self:object) -> None:
        #get the video input from webcam
        ret,frame = self._stream.read()
        height,width = frame.shape[:2]
 
        #resize the frame
        frame = cv2.resize(frame,(400,int((height*400)/width)))
        self._frame = frame

    def detect_motion(self:object) -> bool:
        return True

    def filter_frame(self:object) -> None:
        hsv_frame = cv2.cvtColor(self._frame,cv2.COLOR_BGR2HSV)# convert frame to hsv
        y_mask = cv2.inRange(hsv_frame, np.array(self.y_lower), np.array(self.y_upper))# genrtate yellow mask
        #w_mask = cv2.inRange(hsv_frame, np.array(self.w_lower), np.array(self.w_upper))# generate white mask
        #mask = cv2.bitwise_or(y_mask,w_mask)# bitwise or to combine areas of both masks
        result = cv2.bitwise_and(self._frame,self._frame, mask = y_mask)# apply the mask to the frame
        self._f_frame = result
        
        

    def thresh_frame(self:object) -> None:
        grey = cv2.cvtColor(self._f_frame, cv2.COLOR_BGR2GRAY)# convert to black and white
        blurred = cv2.GaussianBlur(grey, (5, 5), 0) # blur the details
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]# find threshhold of the areas
        self._t_frame = thresh

    def shape_frame_format(self:object) -> None:
        resized = imutils.resize(self._frame, width=300)
        ratio = self._frame.shape[0] / float(resized.shape[0])

        grey = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grey, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        self._f_frame = thresh

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        detect = rect_detector()

        for c in cnts:

            M = cv2.moments(c)

            if detect.plate(c):

                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                cv2.drawContours(self._frame, [c], -1, (0, 255, 0), 2)


    def loop(self:object, fps:int) -> bool:
        prev = 0
        while True:
            time_elapsed = time.time() - prev
            self.set_frame()

            if time_elapsed > 1./fps:
                prev = time.time()
                self.filter_frame()
                self.thresh_frame()
                #self.shape_frame_format()
                self.output(self.detect_motion())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return False

    def output(self:object, motion:bool) -> None:
        if motion: 
            cv2.imshow("frame", self._frame)
            anpr = anpr_handler(True,"tits")
            b64 = anpr.endcode_b64(self._frame)

            cv2.imshow("f_frame", self._f_frame)
            cv2.imshow("t_frame", self._t_frame)
            
            
        else: cv2.imshow("no plate found", self._frame)


class sql_handler:

    def __init__(self:object, details:dict) -> None:
        self._user = details["user"]
        self._password = details["password"]
        self._host = details["host"]
        self._db_name = details["database"]
        
    def connect(self:object) -> bool:
        self._db = mysql.connector.connect(user=self._user, password=self._password, host=self._host, database=self._db_name)

        if self._db:
            self._cursor = self._db.cursor()
            print("connection opened")
            return True
        else:
            print("connection failed")
            return False

    def execute(self:object, query:str, vals:any) -> bool:
        self.cursor.execute(query,vals)
        self._db.commit()

    def close(self) -> None:
        self._db.close()
        print("connection closed")


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


class http_handler:
    _payload = ""


    def __init__(self:object, site:int):
        self._endpoint = "localhost:3000/anpr/"+site

    def post_b_64(self:object, b:str) -> None:
        pass

def main():

    config = open("conf.json")
    conf = json.load(config)

    sql = sql_handler(conf["SQL"])
    if sql.connect():

        feed = feed_handler(conf["camera"],"id")
        fps = conf["fps"]

        if not feed.loop(fps):
            feed._stream.release()
            cv2.destroyAllWindows()
            sql.close()

if __name__ == '__main__':
    main()