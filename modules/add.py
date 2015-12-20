from db import Database

class Add:

    success = ''

    def __init__(self, db='db/baby.db', username=None, cardnumber=None ):

        if username and cardnumber:
            self.db = Database(path=db)
            self.addCard(username, cardnumber)

        else:
            self.__printUsage()


    def addCard(self, uName, cardNumber):
        if self.__basicValidate(cardNumber) and self.__isValid(cardNumber):
            uID = self.db.getUID(uName)
            if uID:
                if self.db.addCard(cardNumber, uID):
                    self.__fail()
                else:
                    self.__pass()
            else:
                print "ERROR: User {uname} was not found.".format(uname=uName)
                self.__fail()
            return 1
        else:
            self.__fail()
            print "ERROR: Invalid card number"
            return 1


    def __luhnChecksum(self, cardNumber):
        # String -> int[] conversion
        def digits(number):
            return [int(digit) for digit in str(number)]
        num = digits(cardNumber)
        odd = num[-1::-2]
        even= num[-2::-2]
        checksum = 0
        checksum += sum(odd)
        for d in even:
            checksum += sum(digits(d*2))
        return checksum % 10

    def __isValid(self, number):
        return self.__luhnChecksum(number) == 0

    # Check proper length and isInt
    def __basicValidate(self, number):
        if 12 <= len(number) <= 19:
            try:
                return True
            except ValueError:
                return 0


    def __pass(self):
        self.db.close()
        self.success = True


    def __fail(self):
        self.db.close()
        self.success = False




    def __printUsage(self):
        print "Use this command to associate Credit Cards with Users."
        print "usage: add <user> <card number>"


