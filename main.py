import telebot
from telebot import types
import config
from DB import Question, DB
import random


bot = telebot.TeleBot(config.BOT_API)

def KBDGenerator(array):
    kbd = types.ReplyKeyboardMarkup()
    for i in range(len(array)):
        kbd.add(types.KeyboardButton(array[i]))
    return kbd

@bot.message_handler(commands=['start'])
def Start(message):
    bot.send_message(message.from_user.id, "Choose block:",
                     reply_markup=KBDGenerator(['Listening','Reading','Grammar','Vocabulary']))
    quiz = Quiz()

    bot.register_next_step_handler(message, quiz.WhichQuiz)

@bot.message_handler(content_types=['text'])
def TextMessage(message):
    if message.text == "Start test":
        Start(message)


class Quiz:

    def __init__(self): 
        self.type = ""
        self.i = 0
        self.question = None
        self.current_question = None
        self.counter = 0 # Правильные ответы
        self.additional_counter = 0 # Все ответы
        self.user_answers = []
        self.correct_answers = []
        self.questions = []
        self.DB = DB()

    @staticmethod
    def __SpaceDeleter3000(array_of_str):
        for i in range(len(array_of_str)):
            array_of_str[i].strip()
        return array_of_str

    def WhichQuiz(self, message):
        if message.text == "Listening":
            self.type = "Listening"
        elif message.text == "Reading":
            self.type = "Readi#ng"
        elif message.text == "Grammar":
            self.type = "Grammar"
        elif message.text == "Vocabulary":
            self.type = "Vocabulary"
        elif message.text == '/start':
            Start(message)
        self.question = Question(self.type)
        self.questions = self.question.getQuestion()
        random.shuffle(self.questions)
        self.__Quiz(message)

    def __Quiz(self, message):
        if message.text != "End test":
            if self.current_question:
                self.__AnsCheck(message)
            if len(self.questions) > self.i:
                bot.send_message(message.from_user.id, text=f"{self.questions[self.i]}",
                                reply_markup=KBDGenerator(['End test']))
                if self.question.HasUrl(self.questions[self.i]):
                    try:
                        bot.send_voice(message.from_user.id, voice=self.question.getUrl(self.questions[self.i]))
                    except:
                        pass
                self.current_question = self.questions[self.i]
                self.i += 1
                bot.register_next_step_handler(message, self.__Quiz)
            else:
                self.__EndQuiz(message)
        else:
            self.__EndQuiz(message)

    def __AnswerFormatter3000(self, answer, userAns):
        if answer.find(',') != -1:
            answer.split(',')
            userAns.split(',')
            answer, userAns = self.__SpaceDeleter3000(answer), self.__SpaceDeleter3000(userAns)
        return answer, userAns

    def __AnsCheck(self, message):
        answer = self.question.getCorrectAnswer(self.current_question)
        self.correct_answers.append(answer)
        self.user_answers.append(message.text)
        self.additional_counter += len(answer)
        userAns = message.text
        answer, userAns = self.__AnswerFormatter3000(answer, userAns)
        for j in range(min(len(answer), len(userAns))):
            if userAns[j] == answer[j]:
                self.counter += 1 

    def __CompareWith(self, userID, flag, *result):
        if flag == 'last':
            textflag = "last"
            Res = self.DB.GetRes(flag, userID)
        elif flag == 'avg':
            textflag = "average"
            Res = self.DB.GetRes(flag ,userID)
        if not Res or Res == 0:
            return ""
        try:
            CurRes = (result[0]/result[1])*100
            delta = abs(round(Res - CurRes))
            if Res > CurRes:
                return f"\nYour current result worse than your {textflag} result by {delta}%"
            elif Res < CurRes:
                return f"\nYour current result better than your {textflag} result by {delta}%"
            else:
                return f"\nYour current result is the same as your {textflag} result"
        except ZeroDivisionError:
            return ""

    def __EndQuiz(self, message):
        compare_ans = ""
        for i in range(len(self.user_answers)):
            compare_ans += f"{i+1}) Correct: {self.correct_answers[i]}  Your: {self.user_answers[i]}\n"
        bot.send_message(message.from_user.id, f"""Test finished, your result: {self.counter} / {self.additional_counter}
        {self.__CompareWith(message.from_user.id, 'last', self.counter, self.additional_counter)}{self.__CompareWith(message.from_user.id, 'avg', self.counter, self.additional_counter)}
        \n\n{compare_ans}""", reply_markup=KBDGenerator(['Start test']))
        self.question.DB.addUserResult(message.from_user.id, self.counter, self.additional_counter)
        self.__Default()

    def __Default(self):
        self.type = ""
        self.i = 0
        self.question = None
        self.current_question = None
        self.counter = 0 # Правильные ответы
        self.additional_counter = 0 # Все ответы
        self.user_answers = []
        self.correct_answers = []
        self.questions = []
        

if __name__ == "__main__":
    bot.polling()