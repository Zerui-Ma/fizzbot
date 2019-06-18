#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# author: mazr

'''
Answer the questions automatically
'''

import json
import urllib.error
import urllib.request

domain = 'https://api.noopschallenge.com'


# print server response


def print_response(dict):
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')


# try an answer and see what fizzbot thinks of it


def try_answer(question_url, answer):
    body = json.dumps({'answer': answer})
    try:
        req = urllib.request.Request(
            domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        response = json.load(res)
        return response

    except urllib.error.HTTPError as e:
        response = json.load(e)
        return response


# generate answers according to numbers and rules


def gen_answer(numbers, rules):
    res = ''
    for num in numbers:
        code = ''
        for rule in rules:
            if num % rule['number'] == 0:
                code += rule['response']

        if not code:
            code = str(num)

        res += code + ' '
    return res[:-1]


# keep trying answers until a correct one is given


def get_correct_answer(question_url, numbers, rules):
    while True:
        if question_url == '/fizzbot/questions/1':
            answer = 'Python'

        else:
            answer = gen_answer(numbers, rules)

        response = try_answer(question_url, answer)

        if (response.get('result') == 'interview complete'):
            print_response(response)
            exit()

        if (response.get('result') == 'correct'):
            return response.get('nextQuestion')


# do the next question


def do_question(domain, question_url):
    request = urllib.request.urlopen(('%s%s' % (domain, question_url)))
    question_data = json.load(request)

    numbers = question_data.get('numbers')
    rules = question_data.get('rules')
    next_question = question_data.get('nextQuestion')

    if next_question:
        return next_question

    else:
        return get_correct_answer(question_url, numbers, rules)


def main():
    question_url = '/fizzbot/questions/1'
    while question_url:
        question_url = do_question(domain, question_url)


if __name__ == '__main__':
    main()
