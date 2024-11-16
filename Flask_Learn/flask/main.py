from flask import Flask,render_template
'''
 It creates an instance of the Flask class, 
 which will be your WSGI (Web Server Gateway Interface) application.
'''
###WSGI Application
app = Flask(__name__)

@app.route("/")
def login():
    return "<html><h1>Welcome to Login Page</h1></html>"

@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)