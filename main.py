import sqlite3
from flask import render_template, redirect, flash, session, abort
import time
# my module backflask
from backflask import *

db = Database.Database("users")
sec = Security.Security(db)
usr = User.User(db)

# define routes here
inst = FlaskCreate.getInstance()
@inst.route("/")
def index():

    if SessionHandler.exists('user'):
        return redirect('/home')

    session['registrationToken'] = sec.getSalt()
    session['loginToken'] = sec.getSalt()
    
    return render_template("index.html", registrationToken = session["registrationToken"], 
                                          loginToken  = session["loginToken"])

@inst.route("/home")
def home():

    if not SessionHandler.exists('user'):
        return redirect('/')

    return render_template("members.html", user = usr.getUsername(session['user']))

@inst.route("/register", methods = ['POST'])
def register():

    cred = {'username' : Requests.getReq('username'),
            'password' : Requests.getReq('password'),
            'passwordAgain' : Requests.getReq('passwordAgain')}

    if not SessionHandler.validToken('registrationToken', 
                                    Requests.getReq('registrationToken')):
        return redirect('/')
    else:
        del session['registrationToken']

    # the last parameter is for lengths
    validation = sec.validRegistration(cred, db, {'passwordLen' : 6, 'usernameLen' : 4})

    if validation == "valid":
        usr.add(cred['username'], cred['password'])
        session['user'] = usr.getID(cred['username'])
        return redirect("/home")
    else:
        print("invalid registration : ")
        if type(validation) == list:
            for value in validation:
                flash(value + " is null")
        elif validation == "passwords":
            flash("passwords do not match")
        elif validation == "taken":
            flash("username has been taken already")
        else:
            flash(validation)

    return redirect("/")

@inst.route("/login", methods = ['POST'])
def login():

    cred = {'username' : Requests.getReq('username'), 
            'password' : Requests.getReq('password')}

    if not SessionHandler.validToken('loginToken', Requests.getReq('loginToken')):
        return redirect('/')
    else:
        del session['loginToken']

    validation = sec.validLogin(cred, db)

    if validation and type(validation) != list:
        if not SessionHandler.exists('user'):
            session['user'] = usr.getID(cred['username'])
        return redirect("/home")
    else:
        flash("invalid login")
        return redirect("/")

@inst.route("/logout")
def logout():

    if not SessionHandler.exists('user'):
        return redirect("/")

    session.clear()
    return redirect("/")

@inst.route("/submitpost", methods = ['POST'])
def submitpost():
    cred = {'userID' : session['user'],
            'title' : Requests.getReq('title'),
            'message' : Requests.getReq('message'),
            'picURL' : Requests.getReq('picurl'),
            'date' : Requests.getReq('time')}

    Content.addpost(db, cred)
    flash("Post added successfuly!")
    return redirect("/addpost")

@inst.route("/delete/<int:id>", methods = ['GET'])
def deletepost(id = 0):
    if not SessionHandler.exists('user'):
        return redirect("/")

    if not Content.rights(db, session['user'], id):
        return "Not sufficient rights"

    Content.deletepost(db, id)
    return redirect('/viewposts')

@inst.route("/edit/<int:id>", methods = ['POST'])
def editpost(id = 0):
    if not SessionHandler.exists('user'):
        return redirect("/")

    if not Content.rights(db, session['user'], id):
        return "Not sufficient rights"

    cred = {'title' : Requests.getReq('title'),
            'message' : Requests.getReq('message'),
            'picURL' : Requests.getReq('picurl')} 

    Content.updatepost(db, id, cred)

    return redirect('/viewposts')

@inst.route("/updatepost/<int:id>")
def updatepost(id = 0):

    if not SessionHandler.exists('user'):
        return redirect("/")

    if not Content.rights(db, session['user'], id):
        return "Not sufficient rights"

    post = Content.getpost(db, id)

    post = post[0]

    return render_template("edit.html", title = post['title'], 
                                        message = post['message'], 
                                        picURL =  post['picURL'], id = id)

@inst.route("/addpost")
def addpost():

    if not SessionHandler.exists('user'):
        return redirect("/")

    return render_template("addpost.html", time = time.time())

@inst.route("/viewposts")
def viewposts():

    if not SessionHandler.exists('user'):
        return redirect("/")

    posts = db.select('posts', '*', ['userID', session['user']])

    if len(posts) == 0:
        posts = ["no posts!"]

    return render_template("viewposts.html", posts = posts)

@inst.route("/blog/<username>")
def viewblog(username):

    if not sec.userExists(username):
        abort(404)
    posts = db.select('posts', '*', ['userID', usr.getID(username)])

    return render_template("blog.html", posts = posts, username = username)

@inst.route("/blogsettings")
def blogsettings():

    if not SessionHandler.exists('user'):
        return redirect("/")

    return render_template("blogsettings.html")

@inst.route("/browse")
def browse():

    if not SessionHandler.exists('user'):
        return redirect("/")

    usernames = db.getAll('users', 'username')

    return render_template("browse.html", usernames = usernames)


@inst.route("/settings")
def settings():

    if not SessionHandler.exists('user'):
        return redirect("/")

    return render_template("settings.html")

@inst.errorhandler(404)
def fourZeroFour(e):

    return Error.getMessage(404)

@inst.errorhandler(500)
def fiveHundred(e):

    return Error.getMessage(500)

if __name__ == '__main__':
    FlaskCreate.run({ 'debug' : True, 'port'  : 1337 })