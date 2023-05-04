import os
import random
import re
import argparse


def get_rand_quiz(path):
    questions = {}
    with open(path, 'r', encoding='KOI8-R') as f:
        quiz = f.read()
        splitted_text = quiz.split('\n\n')
        for count, string in enumerate(splitted_text):
            if 'Вопрос ' in string:
                question_text = re.sub(r'Вопрос \d+:', '', string).strip()
                answer_text = re.sub(r'Ответ:', '', splitted_text[count + 1]).strip()
                questions[question_text] = answer_text

    return questions

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='quiz-questions', help='path to quizzes files')
    args = parser.parse_args()
    path_to_quizzes = args.path
    quizzes_file_names = os.listdir(path_to_quizzes)
    path_to_rand_quiz_file = os.path.join(path_to_quizzes, random.choice(quizzes_file_names))
    get_rand_quiz(path_to_rand_quiz_file)
