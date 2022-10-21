import mysql.connector

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



