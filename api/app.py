import os

import flask_sqlalchemy as sqlalchemy
from flask import Flask, jsonify, request,render_template,redirect,url_for,json,flash
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_cors import CORS
import datetime
from flask_bootstrap import Bootstrap

from flask_login import LoginManager,current_user, login_user,logout_user, login_required
from flask_login import UserMixin

from hashlib import md5
from database.models import *



#from sqlalchemy_imageattach.entity import Image, image_attachment


app = Flask(__name__,static_url_path='/static')
app.debug = True
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

#UPLOAD_FOLDER = '../static/templates'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap(app)
app.config.update(DEBUG=True)
db = sqlalchemy.SQLAlchemy(app)



base_url = '/api/'

@login_manager.user_loader
def load_user(id):
    user = Student.query.get(int(id))
    if user is not None:
        return user
    else:
        return Instructor.query.get(int(id))

        
    
        
@app.route(base_url, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('studenthome'))

    form = LoginForm()
    if form.validate_on_submit():

        user = Student.query.filter_by(email=form.email.data).first()
        # Login Student
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('apply'))

        user = Instructor.query.filter_by(email=form.email.data).first()
        # Login Instructor
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('post'))

        # Login failed
        flash('Invalid username or password')
        return redirect(url_for('login'))
   
    return render_template('mainpage.html', title='Sign In', form=form)



# Route to student Profile
@app.route(base_url + 'studentProfile', methods=['GET'])
def studenthome():
    return render_template('student_Profile.html')


# Route to Instructor Profile
@app.route(base_url + 'instructorProfile', methods=['GET'])
def instructorhome():
    return render_template('Instructor_Profile.html')

# Route to create a student account and main page
@app.route(base_url + 'Register', methods=['POST','GET'])
def createAccount():

    if request.method == 'POST':
        # Student option is checked
        if request.form['options'] == 'STUDENT':
            new_user = Student(request.form['first-name'],request.form['last-name'],request.form['email'],request.form['pwd'])
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)

            # Make sure id is unique
            while Instructor.query.filter_by(id=new_user.id).first() is not None:
                new_user.id = new_user.id + 1
            db.session.commit()
            db.session.refresh(new_user)

            login_user(new_user)
            return redirect(url_for('studenthome'))

        # Instructor option is checked
        elif request.form['options'] == 'INSTRUCTOR':
            new_user = Instructor(request.form['first-name'],request.form['last-name'],request.form['email'],request.form['pwd'])
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)

            # Make sure id is unique
            while Student.query.filter_by(id=new_user.id).first() is not None:
                new_user.id = new_user.id + 1
            db.session.commit()
            db.session.refresh(new_user)

            login_user(new_user)
            return redirect(url_for('instructorhome'))

    return redirect(url_for('login'))
    #return render_template('studenPortal.html', Jobs = Jobs.query.all())



# Route to create a instructor account
@app.route(base_url + 'instructors', methods=['POST'])
def createInstructor():
    instructor = Instructor(**request.json)
    
    db.session.add(instructor)
    db.session.commit()
    db.session.refresh(instructor)
    return jsonify({"status": 1, "instructor": instructor_to_obj(instructor)}), 200

# Route to post a job for Instructors
@app.route(base_url + 'post', methods=['POST','GET'])
#@login_required
def post():

    if request.method == 'POST':
        new_job = Jobs(request.form['position'],request.form['Semester'],request.form['pay'],request.form['gpa_required'])
        db.session.add(new_job)
        db.session.commit()
        db.session.refresh(new_job)
        #,applicates = Job_Application.query.all()
    return render_template('instructorPortal.html',applicates = Job_Application.query.all())

# Route to Display jobs for students
@app.route(base_url + 'apply', methods=['POST','GET'])
@login_required
def apply():

    
    if request.method == 'POST':
        #temp_student = Student(first_name=current_user.first_name,last_name=current_user.last_name,email=current_user.email,password=current_user.password)
        #db.session.add(temp_student)
        #db.session.commit()
        new_app = Job_Application(grade_recieved=request.form['Grade'],Avalialability=request.form['Avalialability'],bio=request.form['bio'],gpa_overall=request.form['gpa_overall'],job_status=request.form['job_status'],owner=current_user)
        new_app.job_status = "Submited"  
        
        #new_app = Job_Application(owner=temp_student)
        db.session.add(new_app)
        db.session.commit()
        db.session.refresh(new_app)
        flash("Job Application successfully Submited")

        


    return render_template('studenPortal.html', Jobs = Jobs.query.all(),Appliedjobs = Job_Application.query.filter_by(id=current_user.id))


# Route to edit info in a student account
# Edit ONLY major, gpa and grad_date
@app.route(base_url + 'students_edit', methods=['GET', 'POST'])
@login_required
def editStudent():

    if request.method == 'POST':

        current_user.gpa = request.form['editGpa']
        current_user.major = request.form['editMajor']

        db.session.add(current_user)
        db.session.commit()
        db.session.refresh(current_user)

        return render_template('student_Profile.html',current_user=current_user)

    return render_template('student_Profile.html',current_user=current_user)

    


# Route to edit info in an Instructor account
# Edit ONLY email, office, and phone
@app.route(base_url + 'instructors_edit', methods=['GET', 'POST'])
@login_required
def editInstructor():

    if request.method == 'POST':

        current_user.email = request.form['editEmail']
        current_user.phone = request.form['editPhone']
        current_user.office = request.form['editOffice']

        db.session.add(current_user)
        db.session.commit()
        db.session.refresh(current_user)

        return render_template('Instructor_Profile.html',current_user=current_user)

    return render_template('Instructor_Profile.html',current_user=current_user)
  
# Route to update Student Application 
@app.route(base_url + 'updateApplication', methods=['POST'])
@login_required
def update_application(applicate):
    
    if request.method == 'POST':
        student = Student.query.filter_by(id =applicate.owner_id)
        student.Job_Application.job_status = "Rejected"
        db,session.add(student)
        db.session.commit()
        db.session.refresh(student)
        return render_template('instructorPortal.html',applicates = Job_Application.query.all())




# Route to Delete student Application
@app.route(base_url + 'cancel_Application', methods=['DELETE'])
@login_required
def cancel_application():

    if request.method == 'DELETE':
        job_position = request.form['job_name']

        job_pos = current_user.jobs.filter_by(position=job_position)
        db.session.delete(job_pos)
        db.session.commit()
        db.session.refresh()
        return render_template('studenPortal.html', Jobs = Jobs.query.all(),Appliedjobs = Job_Application.query.filter_by(id=current_user.id),applied=Jobs.query.filter_by())


# Route to Login out User
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def main():
    db.create_all() # creates the tables you've provided
    app.run(debug=True)       # runs the Flask application  
     
if __name__ == '__main__':
    main()
