from __future__ import unicode_literals

import os

from prompt_toolkit import prompt as prm


class TerminalDisplay:
    def __init__(self):
        self.term = True
        self.w, self.y = os.get_terminal_size()[0], os.get_terminal_size()[1]
        self.home = os.environ["HOME"]
        self.user = os.environ["USER"]

    def screen(self):
        return self.term

    def installer(self):
        questions = [
            {
                "message": 'Input the absolute path to your ebooks\nEnter for default "~/Books" > ',
                "options": "",
                "name": "BOOKPATH",
                "answer": None,
                "default": self.home + "/Books",
            },
            {
                "message": 'Input your PostgreSQL server ip\nEnter for default "localhost" > ',
                "options": "localhost",
                "name": "DB_HOST",
                "answer": None,
                "default": "localhost",
            },
            {
                "message": 'Input your PostgreSQL server port\nEnter for default "5432" > ',
                "options": "5432",
                "name": "DB_PORT",
                "answer": None,
                "default": "5432",
            },
            {
                "message": 'Input your PostgreSQL user name\nEnter for default "pyshelf" > ',
                "options": "pyshelf",
                "name": "USER",
                "answer": None,
                "default": "pyshelf",
            },
            {
                "message": 'Input your PostgreSQL password\nEnter for default "pyshelf" > ',
                "options": "pyshelf",
                "name": "PASSWORD",
                "answer": None,
                "default": "pyshelf",
            },
            {
                "message": 'Web ui hostname/ip\nEnter for default "localhost" > ',
                "options": "localhost",
                "name": "hostname",
                "answer": None,
                "default": "localhost",
            },
            {
                "message": 'Web ui port\nEnter for default "8000" > ',
                "options": "8000",
                "name": "webport",
                "answer": None,
                "default": "8000",
            },
            {
                "message": 'wsgi port\nEnter for default "8001"\n"You should probably leave this alone, unless you know what you\'re doing" > ',
                "options": "8001",
                "name": "wsgiport",
                "answer": None,
                "default": "8001",
            },
        ]
        return self.prompt(questions)

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def prompt(self, questions):
        self.clear()
        answers = questions
        for answer in answers:
            self.h_rule()
            answer["answer"] = prm(answer["message"])
            if answer["answer"] == "":
                answer["answer"] = answer["default"]
            self.clear()
        return answers

    def h_rule(self):
        print("\u2501" * self.w)
