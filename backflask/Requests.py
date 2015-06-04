from flask import request

def getReq(name):

    return request.form[name]