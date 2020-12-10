from flask import Flask, render_template
import sqlite3, os,sys
#Database: str = 'week12/HW11.db'

app:Flask = Flask(__name__,template_folder=os.getcwd())

@app.route('/')
def hello()->str:
    db_path="HW11.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    cursor = c.execute("select students.Name, students.CWID, grades.Grade,grades.Course,instructors.Name from students inner join grades on grades.StudentCWID=students.CWID inner join instructors on instructors.CWID=grades.InstructorCWID order by students.Name;")
    field_names=['Name','Cwid','Course','Grade','Instructor']
    d=list()
    for row in cursor:
        D=dict()
        for i,j in enumerate(row):
            D[field_names[i]]=j
        d.append(D)
    conn.close()

    return render_template("test.html",
                            tetle='Stevens Repository',
                            tetle_title='Student Summary',
                            students=d
                            )
@app.route('/templates')
def template():
    return render_template("base.html", title="Base Template", body="This is base template")
app.run(debug=True)