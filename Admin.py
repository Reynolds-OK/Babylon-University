from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BabylonUniversity.db'
db = SQLAlchemy(app)


class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    D_head = db.Column(db.String(50))
    D_name = db.Column(db.String(50))
    instructor = db.relationship('Instructors', backref='department')


class Instructors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    I_name = db.Column(db.String(100))
    D_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    course = db.relationship('Courses', backref='instructor')
    

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    C_name = db.Column(db.String(100))
    I_id=db.Column(db.Integer, db.ForeignKey('instructors.id'))
    D_id=db.Column(db.Integer, db.ForeignKey('departments.id'))
    student = db.relationship('Students', backref='course')


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    S_name = db.Column(db.String(100))
    C_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    I_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    D_id = db.Column(db.Integer, db.ForeignKey('departments.id'))



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        group_list = ['Reynolds', 'Wepea', 'Hubert', 'Kofi', 'Alphie', 'Isabella']
        if name in group_list and request.form.get('password') == "Group4":
            return render_template('functions.html', name=name)
        else:
            return render_template('try_again.html')
    return render_template('login.html')


@app.route('/functions')
def functions():
    return render_template('functions.html')


@app.route('/departments', methods = ['GET', 'POST'])
def departments(): 
    if request.method == 'POST':
        D_name=request.form.get('D_name')
        D_head=request.form.get('D_head')

        conn = sqlite3.connect('BabylonUniversity.db')
        c = conn.cursor()
        c.execute("SELECT * from Departments")
        entire_list = c.fetchall()

        for each in entire_list:
            if D_name in each or D_head in each:
                return "Department or Department Head is already in the database"

        departments=Departments(D_name = D_name, D_head = D_head)

        db.session.add(departments)
        db.session.commit()
        return redirect('/departments')

    else:  
        departments = Departments.query.all()
        return render_template('departments.html', departments=departments)


@app.route('/departments/edit/<int:id>', methods=['POST', 'GET'])
def edit_departments(id):
    departments = Departments.query.filter_by(id=id).first()
    if request.method == 'POST':
        departments.D_name = request.form.get('D_name')
        departments.D_head = request.form.get('D_head')

        db.session.commit()
        return redirect('/departments')
    else:
        return render_template('edit_departments.html', departments = departments)


@app.route('/departments/delete/<int:id>', methods=['POST', 'GET'])
def delete_department(id):
    departments = Departments.query.filter_by(id=id).first()

    db.session.delete(departments)
    db.session.commit()
    return redirect('/departments')
    



#Instructors side
@app.route('/instructors', methods=['GET', 'POST'])
def instructors():
    if request.method == 'POST':
        try:
            I_name = request.form.get('I_name')
            D_name = request.form.get('D_name')
            link_department = Departments.query.filter_by(D_name = D_name).first()
            if link_department is None:
                return 'Department not found'
            else:
                instructors = Instructors(I_name=I_name, department=link_department)

                db.session.add(instructors)
                db.session.commit()
                return redirect('/instructors')
        except:
            return "Department not found"

    else:
        instructors = Instructors.query.all()
        return render_template('instructors.html', instructors=instructors)


@app.route('/instructors/edit/<int:id>', methods=['POST', 'GET'])
def edit_instructors(id):
    instructors = Instructors.query.filter_by(id=id).first()
    if request.method == 'POST':
        try:
            D_name = request.form.get('D_name')
            link_department = Departments.query.filter_by(D_name=D_name).first()

            instructors.I_name = request.form.get('I_name')
            instructors.D_id = link_department.id

            db.session.commit()
            return redirect('/instructors')

        except:
            return "Department not found"

    else:
        departments = Departments.query.filter_by(id=instructors.D_id).first()
        return render_template('edit_instructors.html', instructors=instructors, departments=departments)


@app.route('/instructors/delete/<int:id>', methods=['POST', 'GET'])
def delete_instructors(id):
    instructors = Instructors.query.filter_by(id=id).first()

    db.session.delete(instructors)
    db.session.commit()
    return redirect('/instructors')


#Going through Courses
@app.route('/courses', methods=['POST', 'GET'])
def courses():
    if request.method == 'POST':
        try:
            C_name = request.form.get('C_name')
            I_name = request.form.get('I_name')

            link_course_instructor = Instructors.query.filter_by(I_name=I_name).first()
            courses = Courses(C_name=C_name, instructor=link_course_instructor)
            courses.D_id = link_course_instructor.D_id

            db.session.add(courses)
            db.session.commit()
            return redirect('/courses')

        except:
            return "Instructor not found"

    else:
        courses = Courses.query.all()
        return render_template('courses.html', courses=courses)


@app.route('/courses/edit/<int:id>', methods=['POST', 'GET'])
def edit_courses(id):
    courses = Courses.query.filter_by(id=id).first()
    if request.method == 'POST':
        try:
            C_name = request.form.get('C_name')
            I_name = request.form.get('I_name')
            link_instructor = Instructors.query.filter_by(I_name=I_name).first()
            link_department = Departments.query.filter_by(id=link_instructor.D_id).first()

            courses.C_name = C_name
            courses.I_id = link_instructor.id
            courses.D_id = link_department.id

            db.session.commit()
            return redirect('/courses')

        except:
            return "Instructor not found"

    else:
        instructors = Instructors.query.filter_by(id=courses.I_id).first()
        return render_template('edit_courses.html', instructors=instructors, courses=courses)


@app.route('/courses/delete/<int:id>', methods=['POST', 'GET'])
def delete_courses(id):
    courses = Courses.query.filter_by(id=id).first()

    db.session.delete(courses)
    db.session.commit()
    return redirect('/courses')


#Student page
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        try:
            S_name = request.form.get('S_name')
            C_name = request.form.get('C_name')
            I_name = request.form.get('I_name')

            link_student_course = Courses.query.filter_by(C_name=C_name).first()
            link_student_instructor = Instructors.query.filter_by(I_name=I_name).first()

            students = Students(S_name=S_name, course=link_student_course)

            students.I_id = link_student_instructor.id
            students.D_id = link_student_course.D_id

            db.session.add(students)
            db.session.commit()
            return redirect('/students')
        except:
            return "Course or Instructor not found"

    else:
        students = Students.query.order_by(asc(Students.I_id)).all()
        return render_template('/students.html', students=students)


@app.route('/students/edit/<int:id>', methods=['POST', 'GET'])
def edit_students(id):
    students = Students.query.filter_by(id=id).first()
    if request.method == 'POST':
        try:
            S_name = request.form.get('S_name')
            C_name = request.form.get('C_name')
            I_name = request.form.get('I_name')
            link_student_course = Courses.query.filter_by(C_name=C_name).first()
            link_student_instructor = Instructors.query.filter_by(I_name=I_name).first()

            students.S_name = S_name
            students.C_id = link_student_course.id
            students.I_id = link_student_instructor.id
            students.D_id = link_student_course.D_id

            db.session.commit()
            return redirect('/students')

        except:
            return "Instructor or Course not found"

    else:
        instructors = Instructors.query.filter_by(id=students.I_id).first()
        courses = Courses.query.filter_by(id=students.C_id).first()
        return render_template('edit_students.html',students=students,   
                            instructors=instructors, courses=courses)


@app.route('/students/delete/<int:id>', methods=['POST', 'GET'])
def delete_students(id):
    students = Students.query.filter_by(id=id).first()

    db.session.delete(students)
    db.session.commit()
    return redirect('/students')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
