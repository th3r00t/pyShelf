from __future__ import unicode_literals

import os
import sys
from pprint import pprint

from prompt_toolkit import prompt as prm


class TerminalDisplay:
    def __init__(self):
        self.term = True
        self.w, self.y = os.get_terminal_size()[0], os.get_terminal_size()[1]

    def screen(self):
        return self.term

    def installer(self):
        questions = [
            {
                "message": "Input the absolute path to your ebooks\nEg. /home/{user}/Books > ",
                "options": "",
                "name": "BOOKPATH",
                "answer": "",
            },
            {
                "message": "Input your PostgreSQL server ip\nEg. localhost > ",
                "options": "localhost",
                "name": "DB_HOST",
                "answer": "",
            },
            {
                "message": "Input your PostgreSQL server port\nEg. 5432 > ",
                "options": "5432",
                "name": "DB_PORT",
                "answer": "",
            },
            {
                "message": "Input your PostgreSQL user name\nEg. pyshelf > ",
                "options": "pyshelf",
                "name": "USER",
                "answer": "",
            },
            {
                "message": "Input your PostgreSQL password\neg. pyshelf > ",
                "options": "pyshelf",
                "name": "PASSWORD",
                "answer": "",
            },
        ]
        answers = self.prompt(questions)
        pprint(answers)

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def prompt(self, questions):
        self.clear()
        answers = questions
        for answer in answers:
            self.h_rule()
            answer["answer"] = prm(answer["message"])
            self.clear()
        return answers

    def h_rule(self):
        print("\u2501" * self.w)
