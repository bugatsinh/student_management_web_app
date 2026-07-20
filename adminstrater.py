from flask import render_template,request,redirect,Blueprint
import sqlite3


student_blueprint = Blueprint('student', __name__, template_folder='templates')

class students_managment_main:
    def __init__(self):
        self.serv = sqlite3.connect("student_data.db")
        self.curser = self.serv.cursor()
        self.curser.execute("""CREATE TABLE IF NOT EXISTS student_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            age INTEGER,
                            marks INTEGER,
                            grade TEXT ) """)

    def added(self,namb,agd,markz):
        marks = int(markz)
        name=namb
        age = agd
        if 100 >= marks >= 95 :
            grade='A+'
        elif 95 >= marks >= 85:
           grade='A'
        elif 85 >= marks >= 80:
            grade='B+'
        elif 80 >= marks >= 75:
            grade='B'
        elif 75 >= marks >= 70:
            grade='C'
        else:
            grade='D'
        self.curser.execute("insert into student_data (name,age,marks,grade) values (?,?,?,?) ", (name,age,marks,grade))
        self.serv.commit()

    def update_marks(self,markz,id):
        marks = int(markz)
        if 100 >= marks >= 95 :
            grade='A+'
        elif 95 >= marks >= 85:
           grade='A'
        elif 85 >= marks >= 80:
            grade='B+'
        elif 80 >= marks >= 75:
            grade='B'
        elif 75 >= marks >= 70:
            grade='C'
        else:
            grade='D'
            
        print(marks,grade)
        self.curser.execute("UPDATE student_data SET marks = ? WHERE id = ?",(marks,id))
        self.curser.execute("UPDATE student_data SET grade = ? WHERE id = ?",(grade,id))
        self.serv.commit()
        print('updated succesfully')

    def delet_std(self,id):
        self.curser.execute("DELETE FROM student_data WHERE id=?",(id,))
        self.serv.commit()
        print('deleted succcesfully')

@student_blueprint.route('/')
def home():
    return render_template('index.html')


@student_blueprint.route('/add',methods = ['GET','POST'])
def add():
    smn = students_managment_main()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        marks = request.form["marks"]
        smn.added(name,age,marks)
        return redirect("/")
    return render_template('add.html')


@student_blueprint.route('/manage_students')
def managestudent():
    smn = students_managment_main()
    smn.curser.execute("SELECT * FROM student_data")
    dta = smn.curser.fetchall()
    smn.curser.execute("SELECT marks FROM student_data")
    drm = smn.curser.fetchall()
    marks_all = 0
    for line in drm:
        marks_all += line[0]
    if drm:
        avm = marks_all / len(drm)
    else:
        avm = 0
    smn.curser.execute("SELECT * FROM student_data ORDER BY marks DESC")
    tpr = smn.curser.fetchone()
    return render_template('manage_student.html',data = dta,average_marks=avm,trp=tpr)

@student_blueprint.route('/delet/<int:id>',methods = ['GET','POST','DELETE'])
def delet_student(id):
    smn = students_managment_main()
    if request.method == "POST":
        smn.delet_std(id)
        return redirect("/")

@student_blueprint.route('/update/<int:id>',methods = ['GET','POST'])
def update_student(id):
    smn = students_managment_main()
    if request.method == "POST":
        marks = request.form["NEW_Marks"]
        smn.update_marks(marks,id)
        return redirect("/")
    return render_template("update_marks.html",id=id)
    

@student_blueprint.route('/search',methods=["GET","POST"])
def search():
    smn = students_managment_main()
    if request.method == "POST":
        id = request.form["student_id"]
        nmae = request.form["student_name"]
        smn.curser.execute("SELECT * FROM student_data where id = ? AND name = ?",(id,nmae))
        student = smn.curser.fetchone()
        if student:
            return render_template("search.html",student = student)
        else:
            gabu = "Student not found"
            return render_template("search.html",gabu=gabu)

    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)