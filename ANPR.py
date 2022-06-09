import cv2
import mysql.connector
import requests
import re


class feed_handler:
    _status = str
    _frame = any

    def __init__(self:object, cam:int ,number:str):
        self._CAMERA = cam
        self._ID = number
        self._stream = cv2.VideoCapture(0)

    def format_frame(self:object) -> any:

        ret,frame = self._stream.read()
        #resized_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        self._frame = frame


    def output(self:object, plate:bool) -> None:
        if plate: 
            cv2.imshow("plate located", self._frame)
            print("yyy")
        else: cv2.imshow("no plate found", self._frame)


class sql_handler:
    db = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='anpr_records')
    cursor = db.cursor()

    def execute(self:object, query:str, vals:any) -> bool:
        self.cursor.execute(query,vals)


class anpr_handler:
    _endpoint = ""
    
    def __init__(self:object, frame:any, key:str):
        self._api_key = key

    def get_plate(self:object) -> str:
        return self._plate

    def get_api_key(self:object) -> str:
        return self._api_key

    def find_data(self:object) -> None:
        pass


def main():
    regex = "(^[A-Z]{2}[0-9]{2}\s?[A-Z]{3}$)|(^[A-Z][0-9]{1,3}[A-Z]{3}$)|(^[A-Z]{3}[0-9]{1,3}[A-Z]$)|(^[0-9]{1,4}[A-Z]{1,2}$)|(^[0-9]{1,3}[A-Z]{1,3}$)|(^[A-Z]{1,2}[0-9]{1,4}$)|(^[A-Z]{1,3}[0-9]{1,3}$)|(^[A-Z]{3}[0-9]{1,4}$)"
    every_other = True
    feed = feed_handler(0,"id")

    while True:
        feed.format_frame()
        feed.output(True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    feed._stream.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()