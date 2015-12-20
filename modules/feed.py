from db import Database

class Feed:

    def __init__(self, db='db/baby.db', user=None, *args):
        if user and not args:
            self.db = Database(path=db)
            self.printFeed(user)
        else:
            self.__printUsage()


    def printFeed(self, user):
        transactions = self.__getTransactionList(user)
        if transactions:
            for row in self.__formatTransactions(transactions):
                print row
        else:
            print "No transactions exist for this user"


    def __getTransactionList(self,user):
        # Verify user exist
        self.uid = self.db.getUID(user)
        if self.uid:
            feed = self.db.getFeed(self.uid)
            return feed
        else:
            self.db.close()
            return 0

    def __formatTransactions(self, transactions):
        line = "-- {src} paid {dst} {amount} for {note}"
        result = []
        src = ''
        dst = ''

        for t in transactions:
            # Hurray for ternary operations!
            src = "You" if t[1]== self.uid else self.db.getUname(t[1])
            dst = "you" if t[2]== self.uid else self.db.getUname(t[2])
            amt = "${amt}".format(amt=format(t[3],'.2f'))
            # Just in case someone didn't leave a note.
            try:
                note= t[5]
            except IndexError:
                # AND THATS WHY YOU ALWAYS LEAVE A NOTE
                note = 'prosthetic arm.'
            result.append(line.format(src=src, dst=dst, amount=amt, note=note))

        self.db.close()
        return result






    def __printUsage(self):
        print "Use this command to list all transactions where <user> is present"
        print "usage: feed <user>"

