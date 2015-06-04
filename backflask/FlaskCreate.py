import sys

# trying to import flask
try:
    from flask import Flask, render_template

except ImportError:

    print("Could not import flask!")
    sys.exit(1)

app = Flask(__name__, template_folder="../templates")
app.secret_key = 'some_secret'

def getInstance():

    return app

def run(parameters = {}):

    if not parameters:

        app.run(debug = debug)
        
    else:

        try:
            # ** operator unpacks dictioanry
            app.run(**parameters)

        except ValueError:

            print("Run parameters are of wrong type")

