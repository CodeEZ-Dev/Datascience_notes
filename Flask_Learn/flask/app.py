from flask import Flask
'''
 It creates an instance of the Flask class, 
 which will be your WSGI (Web Server Gateway Interface) application.
'''
###WSGI Application
app = Flask(__name__)

@app.route("/")
def login():
    return "Welcome to login page!!!"

@app.route("/home")
def home():
    return "Welcome to home page!!!"

if __name__ == '__main__':
    app.run(debug=True)