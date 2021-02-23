import telebot
from telebot import types
import config
from question import Question

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
        self.counter = 0
        self.user_answers = []
        self.correct_answers = []

    def WhichQuiz(self, message):
        if message.text == "Listening":
            self.type = "Listening"
        elif message.text == "Reading":
            self.type = "Reading"
        elif message.text == "Grammar":
            self.type="Grammar"
        elif message.text == "Vocabulary":
            self.type = "Vocabulary"
        self.Quiz(message)

    def Quiz(self, message):
        question = Question(self.type)
        questions = question.getQuestion()
        if message.text != "Закончить тест":
            if self.current_question:
                answer = question.getCorrectAnswer(self.current_question)
                self.correct_answers.append(answer)
                self.user_answers.append(message.text)
                if message.text == answer:
                    self.counter += 1
            if len(questions) > self.i:
                bot.send_message(message.from_user.id, text=f"{questions[self.i]}",
                                reply_markup=KBDGenerator(['Закончить тест']))
                if self.type == "Listening":
                    bot.send_audio(message.from_user.id, audio=question.getUrl(questions[self.i]))
                self.current_question = questions[self.i]
                self.i += 1
                bot.register_next_step_handler(message, self.Quiz)
            else:
                compare_ans = ""
                for i in range(len(self.user_answers)):
                    compare_ans+=f"{i+1}) Correct: {self.correct_answers[i]}  Your: {self.user_answers[i]}\n"
                bot.send_message(message.from_user.id, f"Тест закончен, результат:\n{self.counter} из {self.i}\n\n{compare_ans}",
                                reply_markup=KBDGenerator(['Начать тест']))
                self.i, self.counter, self.current_question, self.type = 0, 0, None, ""
        else:
            compare_ans = ""
                for i in range(len(self.user_answers)):
                    compare_ans+=f"{i+1}) Correct: {self.correct_answers[i]}  Your: {self.user_answers[i]}\n"
            bot.send_message(message.from_user.id, f"Тест закончен, результат:\n{self.counter} из {self.i-1}\n\n{compare_ans}",
                            reply_markup=KBDGenerator(['Начать тест']))
            self.i, self.counter, self.current_question, self.type = 0, 0, None, ""
            


if __name__ == "__main__":
    bot.polling()


