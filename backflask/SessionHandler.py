from flask import session

def exists(sessionName):

    if session.get(sessionName):
        return True

    return False

def validToken(sessionName, request):

    if exists(sessionName) and session[sessionName] == request:
        return True
    return False
