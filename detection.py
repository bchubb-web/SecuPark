import cv2


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

