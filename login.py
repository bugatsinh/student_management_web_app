from flask import render_template,request,redirect, url_for,Blueprint
import sqlite3
import hashlib


login_blueprint = Blueprint('login',__name__,template_folder='templates')

class log_info():
    def __init__(self):
        self.serv = sqlite3.connect("log_info.db")
        self.cursor = self.serv.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS log_info (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            fullName VARCHAR(255) NOT NULL,
                            email TEXT,
                            pass VARCHAR(255) NOT NULL
                            ) """)
    def signing_up(self,fullName,email,passwrd):
        password = hashlib.sha256(passwrd.encode()).hexdigest()
        self.cursor.execute("INSERT INTO log_info (fullName,email,pass) values (?,?,?)",(fullName,email,password))
        self.serv.commit()



@login_blueprint.route("/log_in",methods=["GET","POST"])
def log_pose():
    lag = log_info()
    if request.method == "POST":
        username =request.form['username']
        password =request.form['password']
        lag.cursor.execute("SELECT * FROM log_info")
        data = lag.cursor.fetchall()
        for line in data:
            print(line[1],line[3])
            pasdr = hashlib.sha256(password.encode()).hexdigest()
            if username==line[1] and pasdr==line[3]:
                print("login succesfully")
                rover = False
            else:
                rover = True
        if rover == False:
            return redirect("/student")
        else:
            return render_template("login_data.html",rover=rover)


    return render_template("login_data.html")


@login_blueprint.route("/sign_up",methods=["GET","POST"])
def sign_up():
    lg = log_info()
    if request.method == "POST":
        fullName =request.form['username']
        email =request.form['email']
        password =request.form['password']
        confirmPassword =request.form['confirm_password']
        if password == confirmPassword:
            lg.signing_up(fullName,email,password)
            raunda = False
            return redirect("/")
        else:
            raunda = True
        return render_template("sign_up.html",raunda=raunda)
    return render_template("sign_up.html")

