from flask import Flask,render_template,request,redirect
from login import login_blueprint
from adminstrater import student_blueprint


app = Flask(__name__)
app.register_blueprint(login_blueprint,url_prefix='/login')
app.register_blueprint(student_blueprint,url_prefix='/student')

@app.route('/')
def home():
    return render_template('webapp_explain.html')

app.run(debug=True)