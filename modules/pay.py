import re
from db import Database

class Pay:

    def __init__(self, db='db/baby.db', src=None, dst=None, amount=None, *args):
        if src and dst and amount:
            # Run through regex
            self.amount = self.__isValidCurrencySyntax(amount)
            if self.amount:
                # No money laundering
                if src != dst:
                    self.db = Database(path=db)
                    self.makePayment(src, dst, self.amount, self.__noteToString(args))
                else:
                    print "ERROR: Users cannot pay themselves."
                    self.__fail()

        else:
            self.__printUsage()


    def makePayment(self, src, dst, amount, note=None):
        # Validate source user
        srcID = self.db.getUID(src)
        if srcID:
            # Confirm source user has CC registered to account
            if self.db.getCID(uid=srcID):
                dstID = self.db.getUID(dst)
                # Verify destination user exist
                if dstID:
                    self.db.addTransaction(srcID, dstID, amount, note)
                    self.__pass()
                else:
                    print "ERROR: User {uname} was not found.".format(uname=dst)
                    self.__fail()
            else:
                print "ERROR: User {uname} does not have a credit card associated with their account".format(uname=src)
                self.__fail()
        else:
            print "ERROR: User {uname} was not found.".format(uname=src)
            self.__fail()


    def __printUsage(self):
        print "Use this command to pay users."
        print "usage: pay <from_username> <to_username> <amount> (optional)<note>"

    # Decided it was cool to let people trade fractions of cents
    # just so they could practice HFT.
    # No commas, though. Who needs commas?
    def __isValidCurrencySyntax(self, amount):
        if re.match('^\${1}[\d]+\.{1}\d*$', amount):
            if float(amount.lstrip('$')) <= 0:
                print "ERROR: Amount must be greater than 0."
                self.__fail()
            return float(amount.lstrip('$'))
        else:
            print "ERROR: <amount> must be in the format $<digits>.<digits>"
            self.__fail()

    def __noteToString(self, note):
        s = ""
        for word in note:
            s += " "+str(word)
        return s.strip()

    def __pass(self):
        self.db.close()
        self.success = True


    def __fail(self):
        try:
            self.db.close()
        except AttributeError:
            pass
        self.success = False


