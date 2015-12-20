from db import Database

class Balance:

    def __init__(self, db='db/baby.db', user=None, *args):
        if user and not args:
            self.db = Database(path=db)
            self.printBalance(user)
        else:
            self.__printUsage()

    def printBalance(self, user):
        uid = self.db.getUID(user)
        if uid:
            balance = format(self.db.getBalance(uid), '.2f')
            print "-- ${bal}".format(bal=balance)
            self.db.close()
        else:
            print "ERROR: This user does not exist"
            self.db.close()


    def __printUsage(self):
        print "Use this command to display the balance of a <user>"
        print "usage: balance <user>"
