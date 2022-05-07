from curses import echo
import re
import livejson, json
import time
import traceback
import threading

class Chacking:
    def __init__(self, database):
        self.database = database
        
    def checking_user_info(self, userid):
        if str(userid) not in self.database["user"]:
            return False
        else:
            return True

    def checking_user_keyword(self, userid, word):
        if str(word) not in self.database["user"][str(userid)]:
            return False
        else:
            return True

    def checking_user_title(self, userid, word, title):
        if str(title) not in self.database["user"][str(userid)][str(word)]:
            return False
        else:
            return True
    
    def checking_user_data(self, userid, word, title, data):
        if str(data) not in self.database["user"][str(userid)][str(word)][str(title)]:
            return False
        else:
            return True

class Storage:

    def __init__(self, path_name = "database.json"):
        self.path_name = path_name
        self.database = livejson.File(path_name, True, False, 4)
        self.install_info()
        self.checking = Chacking(self.database)
    
    def install_info(self):
        if "user" not in self.database:
            self.database["user"] = {}
    
    
