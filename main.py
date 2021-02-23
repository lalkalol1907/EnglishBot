import telebot
from telebot import types
import config
from DB import Question
import random
from accessify import private

bot = telebot.TeleBot(config.BOT_API)

def KBDGenerator(array):
    kbd = types.ReplyKeyboardMarkup()
    for i in range(len(array)):
        kbd.add(types.KeyboardButton(array[i]))
    return kbd


@bot.message_handler(commands=['start'])
def Start(message):
    bot.send_message(message.from_user.id, "Какой блок ты хочешь отработать?",
                     reply_markup=KBDGenerator(['Listening','Reading','Grammar','Vocabulary']))
    quiz = Quiz()
    bot.register_next_step_handler(message, quiz.WhichQuiz)


@bot.message_handler(content_types=['text'])
def TextMessage(message):
    if message.text == "Начать тест":
        Start(message)


class Quiz:

    def __init__(self):
        self.type = ""
        self.i = 0
        self.current_question = None
        self.counter = 0 # Правильные ответы
        self.additional_counter = 0 # Все ответы
        self.user_answers = []
        self.correct_answers = []
        self.questions = []

    def WhichQuiz(self, message):
        if message.text == "Listening":
            self.type = "Listening"
        elif message.text == "Reading":
            self.type = "Reading"
        elif message.text == "Grammar":
            self.type="Grammar"
        elif message.text == "Vocabulary":
            self.type = "Vocabulary"
        self.__Quiz(message)

    @private
    def __Quiz(self, message):
        question = Question(self.type)
        if self.questions == []:
            self.questions = question.getQuestion()
            random.shuffle(self.questions)
        if message.text != "Закончить тест":
            if self.current_question:
                self.__AnsCheck(message, question.getCorrectAnswer(self.current_question))
            if len(self.questions) > self.i:
                bot.send_message(message.from_user.id, text=f"{self.questions[self.i]}",
                                reply_markup=KBDGenerator(['Закончить тест']))
                if self.type == "Listening":
                    bot.send_voice(message.from_user.id, audio=question.getUrl(self.questions[self.i]))
                self.current_question = self.questions[self.i]
                self.i += 1
                bot.register_next_step_handler(message, self.__Quiz)
            else:
                self.__EndQuiz(message)
        else:
            self.__EndQuiz(message)

    @private
    def __AnsCheck(self, message, answer):
        self.correct_answers.append(answer)
        self.user_answers.append(message.text)
        for j in range(len(answer))
            if message.text[j] == answer[j]:
                self.counter += 1 

    @private
    def __EndQuiz(self, message):
        compare_ans = ""
        for i in range(len(self.user_answers)):
            compare_ans+=f"{i+1}) Correct: {self.correct_answers[i]}  Your: {self.user_answers[i]}\n"
        bot.send_message(message.from_user.id, f"Тест закончен, результат:\n{self.counter} из {self.additional_counter}\n\n{compare_ans}",
                            reply_markup=KBDGenerator(['Начать тест']))
        question.DB.addUserResult(message.from_user.id, self.counter, self.additional_counter)
        self.__Default()

    @private
    def __Default(self):
        return 0
        

if __name__ == "__main__":
    bot.polling()


