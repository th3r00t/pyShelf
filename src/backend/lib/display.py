from __future__ import unicode_literals

import os

import pyfiglet
from prompt_toolkit import prompt as prm


class TerminalDisplay:
    def __init__(self):
        self.term = True
        self.w, self.y = os.get_terminal_size()[0], os.get_terminal_size()[1]
        self.home = os.environ["HOME"]
        breakpoint()
        self.user = os.environ["USER"]
        self.version = "0.4.0"
        self.slogan = "The Installer Initiative"
        self.green = "\033[1;32m"
        self.blue = "\033[94m"
        self.clr_term = "\033[m"

    def screen(self):
        return self.term

    def installer(self):
        questions = [
            {
                "message": ' Input the absolute path to your ebooks\n Enter for default "~/Books" > ',
                "options": "",
                "name": "BOOKPATH",
                "answer": None,
                "default": self.home + "/Books",
            },
            {
                "message": ' Input your PostgreSQL server ip\n Enter for default "localhost" > ',
                "options": "localhost",
                "name": "DB_HOST",
                "answer": None,
                "default": "localhost",
            },
            {
                "message": ' Input your PostgreSQL server port\n Enter for default "5432" > ',
                "options": "5432",
                "name": "DB_PORT",
                "answer": None,
                "default": "5432",
            },
            {
                "message": ' Input your PostgreSQL password\n Enter for default "pyshelf" > ',
                "options": "pyshelf",
                "name": "PASSWORD",
                "answer": None,
                "default": "pyshelf",
            },
            {
                "message": ' Web ui hostname/ip\n Enter for default "localhost" > ',
                "options": "localhost",
                "name": "hostname",
                "answer": None,
                "default": "localhost",
            },
            {
                "message": ' Web ui port\n Enter for default "8000" > ',
                "options": "8000",
                "name": "webport",
                "answer": None,
                "default": "8000",
            },
            {
                "message": ' wsgi port\n Enter for default "8001 > ',
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
            self.banner()
            answer["answer"] = prm(answer["message"])
            if answer["answer"] == "":
                answer["answer"] = answer["default"]
            self.clear()
        return answers

    def h_rule(self):
        print("\u2501" * self.w)

    def banner(self):
        self.h_rule()
        title = pyfiglet.Figlet(font="cyberlarge")
        print(self.green + title.renderText("pyShelf") + self.clr_term)
        print(
            self.blue + " version " + self.version + self.clr_term + " " + self.slogan
        )
        self.h_rule()
        print()

    def banner_render(self):
        title = pyfiglet.Figlet(font="cyberlarge")
        _banner = (
            title.renderText("pyShelf")
            + "\nversion "
            + self.version
            + " "
            + self.slogan
            + "\n"
        )
        return _banner
