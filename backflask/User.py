from backflask import Database, Security
import uuid
class User:

    def __init__(self, db):

        self.db = db
        self.sec = Security.Security(db)

    def add(self, username, password):

        salt = uuid.uuid4().hex
        self.db.query("insert into users ('username', 'password', 'salt') values (?,?,?)", 
                      (username, self.sec.hash(password, salt), salt))

    def getID(self, username):

        return self.db.select('users', 'ID', ['username', username])[0]['id']

    def getUserInfo(self, ID):

        query = self.db.select('users', '*', ['ID', ID])
        if not query:
            return False
        else:
            return query[0]

    def getUsername(self, ID):
        
        query = self.getUserInfo(ID)
        if query != False:
            return query['username']
        else:
            return False