import re
from db import Database

class User:

    def __init__(self, db='db/baby.db', user=None, *args):
        if user and not args:
            self.user = self.__validateUsername(user)
            self.db = Database(path=db)
            if self.user:
                self.success = self.addUser(self.user)
            else:
                self.success = 1
        else:
            self.__printUsage()


    def addUser(self,uname):
        if self.db.addUser(uname):
            print "ERROR: Username {uname} is unavailable.".format(uname=uname)
            return 1
        self.db.close()
        return 0

    def __printUsage(self):
        print "This command is used to add a user to the VenmoJr Database"
        print "usage: user <username>"

    # All alphanum with _ and -. No |\|*$(0P3'rs allowed
    def __validateUsername(self, uname):
        if re.match('^[\w\-]+$',uname):
            return uname
        else:
            print "ERROR: Invalid username. Usernames may only contain letters, numbers, -, and _"
            return 0



