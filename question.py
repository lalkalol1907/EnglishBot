import pymysql
from config import conargs

class Question:
    def __init__(self, type):
        self.conargs = conargs
        self.type = type
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



