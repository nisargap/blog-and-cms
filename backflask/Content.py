from backflask import Database
def addpost(db, fields):

    # userID, title, message, timestamp, picURL
    numFields = 5
    if len(fields) != numFields:
        return False

    db.insert('posts', fields)

    print(db.getAll('posts', '*'))

    return True

def deletepost(db, id):

    db.delete('posts', ['id', id])

    return True

def updatepost(db, id, newValues):

    fieldsArray = []
    for key in newValues:
        fieldsArray.append(key)
        fieldsArray.append(newValues[key])

    db.update('posts', fieldsArray, ['id', id])

    return True

def rights(db, user, postID):

    results = db.select('posts', '*', ['id', postID, 'userID', user])
    if len(results) == 0:
        return False
    return True

def getpost(db, postID):

    return db.select('posts', '*', ['id', postID])