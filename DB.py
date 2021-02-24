import pymysql
from config import conargs

class DB:

    def __init__(self):
        self._conargs = conargs

    def addUserResult(self, userID, *results):
        if len(results) == 1:
            result_percent = results[0]
        else:
            try:
                result_percent = round((results[0]/results[1])*100)
            except ZeroDivisionError:
                return 0
        con = pymysql.connect(**self._conargs)
        with con.cursor() as cur:
            cur.execute(f"INSERT INTO ResultsTable VALUES({self._LastIDfinder('ResultsTable')+1}, '{userID}', {result_percent})")
        con.commit()
        con.close()

    def _LastIDfinder(self, TableName):
        con = pymysql.connect(**self._conargs)
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {TableName}")
            rows = cur.fetchall()
        try:    
            return rows[len(rows)- 1][0]
        except:
            return -1

    def GetRes(self, flag, userID):
        con = pymysql.connect(**self._conargs)
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM ResultsTable WHERE UserID = '{userID}'")
            rows = cur.fetchall()
        try:
            if flag == 'last': 
                return rows[len(rows)-1][2]
            elif flag == 'avg':
                sum_for_avg = 0
                div_for_avg = 0
                for row in rows:
                    sum_for_avg += int(row[2])
                    div_for_avg += 1
                return round(sum_for_avg/div_for_avg)
        except:
            return None 
        

class Question:

    def __init__(self, type):
        self.__type = type
        self.__DB = DB()
        self.__conargs = self.__DB._conargs

    def HasUrl(self, question):
        if self.__type == "Listening":
            return True
        return False

    def getQuestion(self):
        con = pymysql.connect(**self.__conargs)
        questions = []
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.__type}Table")
            rows = cur.fetchall()
            for row in rows:
                questions.append(row[1])
        return questions

    def getCorrectAnswer(self, question):
        con = pymysql.connect(**self.__conargs)
        CorrectAns = ""
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.__type}Table WHERE question = '{question}'")
            rows = cur.fetchall()
            for row in rows:
                CorrectAns = row[2]
        return CorrectAns

    def getUrl(self, question):
        con = pymysql.connect(**self.__conargs)
        URL = ""
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.__type}Table WHERE question = '{question}'")
            rows = cur.fetchall()
            for row in rows:
                URL = row[3]
        return URL

