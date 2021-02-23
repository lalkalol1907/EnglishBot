import pymysql
from config import conargs

class DB:

    def __init__(self):
        self.conargs = conargs

    def addUserResult(self, userID, *results):
        if len(results) == 1:
            result_percent = results[0]
        else:
            result_percent = round((results[0]/results[1])*100)
        con = pymysql.connect(**self.conargs)
        with con.cursor() as cur:
            cur.execute(f"INSERT INTO ResultsTable VALUES({self.LastIDfinder('ResultsTable')+1}, '{userID}', {result_percent})")
        con.commit()
        con.close()

    def LastIDfinder(self, TableName):
        con = pymysql.connect(**self.conargs)
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {TableName}")
            rows = cur.fetchall()
        try:    
            return rows[len(rows)- 1][0]
        except:
            return -1

    def GetLastRes(self):
        pass

    def GetAvgRes(self):
        pass
        

class Question:
    def __init__(self, type):
        self.type = type
        self.DB = DB()
        self.conargs = self.DB.conargs
        if type == "Listening":
            self.url = self.getUrl()
        self.text = self.getQuestion()


    def getQuestion(self):
        con = pymysql.connect(**self.conargs)
        questions = []
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.type}Table")
            rows = cur.fetchall()
            for row in rows:
                questions.append(row[1])
        return questions

    def getCorrectAnswer(self, question):
        con = pymysql.connect(**self.conargs)
        CorrectAns = ""
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.type}Table WHERE question = '{question}'")
            rows = cur.fetchall()
            for row in rows:
                CorrectAns = row[2]
        return CorrectAns

    def getUrl(self, question):
        con = pymysql.connect(**self.conargs)
        URL = ""
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.type}Table WHERE question = '{question}'")
            rows = cur.fetchall()
            for row in rows:
                URL = row[3]
        return URL

