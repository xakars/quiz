import os
import random
import re


path_to_quiz = 'quiz-questions'
quiz_file_names =  os.listdir(path_to_quiz)
path_to_rand_quiz_file = os.path.join(path_to_quiz, random.choice(quiz_file_names))

questions = {}

with open(path_to_rand_quiz_file, 'r', encoding='KOI8-R') as f:
    quiz = f.read()
    splitted_text = quiz.split('\n\n')
    for count, string in enumerate(splitted_text):
        if 'Вопрос ' in string:
            question_text = re.sub(r'Вопрос \d+:', '', string).strip()
            answer_text = re.sub(r'Ответ:', '', splitted_text[count + 1]).strip()
            questions[question_text] = answer_text

print(questions)

