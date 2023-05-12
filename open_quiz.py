import re


def get_rand_quiz(path_to_rand_quiz_file):
    questions = {}
    with open(path_to_rand_quiz_file, 'r', encoding='KOI8-R') as f:
        quiz = f.read()
        splitted_text = quiz.split('\n\n')
        for count, string in enumerate(splitted_text):
            if 'Вопрос ' in string:
                question_text = re.sub(r'Вопрос \d+:', '', string).strip()
                answer_text = re.sub(r'Ответ:', '', splitted_text[count + 1]).strip()
                questions[question_text] = answer_text

    return questions


def check_user_answer(correct_answer, user_answer):
    pure_answer = re.sub(r'\([^)]*\)|\.', '', correct_answer)
    return pure_answer == user_answer

