import os
import hashlib, uuid, binascii
from backflask import Database
class Security:

    def __init__(self, db):

        self.db = db

    def checkNull(self, reqs):

        nulls = []
        for key in reqs:
            if not reqs[key]:
                nulls.append(key)
        return nulls

    def getSalt(self):

        salt = uuid.uuid4().hex
        return salt

    def grabSalt(self, username):

        s = self.db.select('users', 'salt', ['username', username])
        if s:
            return s[0]['salt']
        return 0

    def hash(self, password, salt):

        derivedKey = hashlib.pbkdf2_hmac('sha512', bytes(password, encoding='utf-8'), bytes(salt, encoding='utf-8'), 10000)

        return binascii.hexlify(derivedKey)

    def userExists(self, username):
        
        return self.db.count('users', ['username', username])

    def validUser(self, username, password):

        salt = self.grabSalt(username)

        password = self.hash(password, salt)

        return self.db.count('users', ['username', username, 'password', password])

    def validRegistration(self, reqs, db, lengths):

        # check for null values
        
        nulls = self.checkNull(reqs)

        if len(nulls) > 0:
            return nulls

        if len(reqs['password']) < lengths['passwordLen']:
            return "password length must be at least " + str(lengths['passwordLen']) + " characters"

        if len(reqs['username']) < lengths['usernameLen']:
            return "username length must be at least " + str(lengths['usernameLen']) + " characters"

        # check if passwords match
        if reqs['password'] != reqs['passwordAgain']:
            return "passwords"

        # check if username not taken
        
        if not self.userExists(reqs['username']):
            return "valid"
        else:
            return "taken"

    def validLogin(self, reqs, db):

        # check for null values 

        nulls = self.checkNull(reqs)

        if len(nulls) > 0:
            return nulls

        # check if username and password are in db
        c = self.validUser(reqs['username'], reqs['password'])
        if c == 0:
            return False
        else:
            return True

