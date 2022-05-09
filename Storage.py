from curses import echo
from multiprocessing.sharedctypes import Value
import re
import livejson, json
import time
import traceback
import threading

class Chacking:
    def __init__(self, database):
        self.database = database
    
    def checking_server_id(self, serverid):
        if str(serverid) not in self.database["server"]:
            return False
        return True
    
    def checking_server_channel(self, serverid, channel):
        if str(channel) not in self.database["server"][str(serverid)]["channel"]:
            return False
        return True
    
    def checking_server_id_channel(self, serverid, channel):
        value_serverid = None
        value_channel = None
        if str(serverid) in self.database["server"]:
            value_serverid = "server:True"
        else:
            value_serverid = "server:False"
        if str(channel) in self.database["server"][str(serverid)]:
            value_channel = "channel:True"
        else:
            value_channeld = "channel:False"
        return value_serverid, value_channel

    def checking_user_id(self, userid):
        if str(userid) not in self.database["user"]:
            return False
        return True

    def checking_user_keyword(self, userid, word):
        if str(word) not in self.database["user"][str(userid)]:
            return False
        return True

    def checking_user_title(self, userid, word, title):
        if str(title) not in self.database["user"][str(userid)][str(word)]:
            return False
        return True
    
    def checking_user_data(self, userid, word, title, data):
        if str(data) not in self.database["user"][str(userid)][str(word)][str(title)]:
            return False
        return True

    def checking_user_id_keyword(self, userid, word):
        value_userid = None
        value_word = None
        if str(userid) in self.database["user"]:
            value_userid = "user:True"
        else:
            value_userid = "user:False"
        if str(word) in self.database["user"][str(userid)]:
            value_word = "word:True"
        else:
            value_word = "word:False"
        return value_userid, value_word

    def checking_user_id_keyword_title(self, userid, word, title):
        value_userid = None
        value_word = None
        value_title = None
        if str(userid) in self.database["user"]:
            value_userid = "user:True"
        else:
            value_userid = "user:False"
        if str(word) in self.database["user"][str(userid)]:
            value_word = "word:True"
        else:
            value_word = "word:False"
        if str(title) in self.database["user"][str(userid)][str(word)]:
            value_title = "title:True"
        else:
            value_title = "title:False"
        return value_userid, value_word, value_title

    def checking_user_id_keyword_title_data(self, userid, word, title, data):
        value_userid = None
        value_word = None
        value_title = None
        value_data = None
        if str(userid) in self.database["user"]:
            value_userid = "user:True"
        else:
            value_userid = "user:False"
        if str(word) in self.database["user"][str(userid)]:
            value_word = "word:True"
        else:
            value_word = "word:False"
        if str(title) in self.database["user"][str(userid)][str(word)]:
            value_title = "title:True"
        else:
            value_title = "title:False"
        if str(data) in self.database["user"][str(userid)][str(word)][str(title)]:
            value_data = "data:True"
        else:
            value_data = "data:False"
        return value_userid, value_word, value_title, value_data

class Storage:

    def __init__(self, path_name = "../database.json"):
        self.path_name = path_name
        self.database = livejson.File(path_name, True, False, 4)
        self.install_id()
        self.checking = Chacking(self.database)
    
    def install_id(self):
        if "user" not in self.database:
            self.database["user"] = {}
        if "server" not in self.database:
            self.database["server"] = {}
    
    
