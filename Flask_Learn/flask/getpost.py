from flask import Flask,render_template,request
'''
 It creates an instance of the Flask class, 
 which will be your WSGI (Web Server Gateway Interface) application.
'''
###WSGI Application
app = Flask(__name__)

@app.route("/")
def login():
    return "<html><h1>Welcome to Login Page</h1></html>"

@app.route("/home",methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/form',methods=['GET','POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        return f'Hello {name}'
    return render_template('form.html')

@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        return f'Hello {name}'
    return render_template('form.html')    

if __name__ == '__main__':
    app.run(debug=True)