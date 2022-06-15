import cv2
from datetime import datetime
import mysql.connector
import requests
#from google.cloud import vision_vlp3beta1 as vision
import numpy as np
import time
import json
import re


class feed_handler:
    _status: str
    y_lower=[20, 35, 140]
    y_upper = [50,255,255]

    def __init__(self:object, cam:int ,number:str):# init the data for the camera, store as attributes
        self._CAMERA = cam
        self._ID = number
        self._stream = cv2.VideoCapture(cam)

    def format_frame(self:object) -> None:

        ret,frame = self._stream.read()
        height,width = frame.shape[:2]
        frame = cv2.resize(frame,(800,int((height*800)/width)))
        self._frame = frame

    def detect_motion(self:object) -> bool:
        return True

    def filter_frame(self:object) -> None:
        hsv_frame = cv2.cvtColor(self._frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, np.array(self.y_lower), np.array(self.y_upper))
        result = cv2.bitwise_and(self._frame,self._frame, mask = mask)
        self._frame = result

    def loop(self:object, fps:int) -> bool:
        prev = 0
        while True:
            time_elapsed = time.time() - prev
            self.format_frame()

            if time_elapsed > 1./fps:
                prev = time.time()
                self.filter_frame()
                self.output(self.detect_motion())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return False

    def output(self:object, plate:bool) -> None:
        if plate: 
            cv2.imshow("plate found", self._frame)
            
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

    def find_data(self:object) -> None:
        pass


def main():

    config = open("conf.json")
    conf = json.load(config)

    sql = sql_handler(conf["SQL"])
    if sql.connect():

    # regex = "(^[A-Z]{2}[0-9]{2}\s?[A-Z]{3}$)|(^[A-Z][0-9]{1,3}[A-Z]{3}$)|(^[A-Z]{3}[0-9]{1,3}[A-Z]$)|(^[0-9]{1,4}[A-Z]{1,2}$)|(^[0-9]{1,3}[A-Z]{1,3}$)|(^[A-Z]{1,2}[0-9]{1,4}$)|(^[A-Z]{1,3}[0-9]{1,3}$)|(^[A-Z]{3}[0-9]{1,4}$)"
    
        feed = feed_handler(conf["camera"],"id")
        
        fps = conf["fps"]

        if not feed.loop(fps):
            
            feed._stream.release()
            cv2.destroyAllWindows()
            sql.close()

if __name__ == '__main__':
    main()