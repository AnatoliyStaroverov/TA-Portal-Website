import flask_sqlalchemy as sqlalchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship,sessionmaker
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask_login import UserMixin
from flask import Flask

app = Flask(__name__,static_url_path='/static')
db = sqlalchemy.SQLAlchemy(app)


# Database model for Instructor information
class Instructor(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #space = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    phone = db.Column(db.String(64), nullable=False, default="N/A")
    office = db.Column(db.String(64), nullable=False, default="N/A")

    def __init__(self,first_name,last_name,email,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email  = email
        self.password = password

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if password == self.password:
            return True
        return False
        #return check_password_hash(self.password, password)


# Database model for Course information
class Course(db.Model):
    name = db.Column(db.String(64), nullable=False, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128), nullable=False)

# Database model for course instructor teaches
class InstructorCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, primary_key=True)

# Database model for TA application to course
class CourseTA(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(64), nullable=False, primary_key=True)

# database for posted jobs
class Jobs(db.Model):
    __tablenames__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(128), nullable=False)
    semester = db.Column(db.String(128), nullable=False)
    pay = db.Column(db.Float, default=0.0)
    gpa_required = db.Column(db.Float, default=0.0)
    jobs_app = relationship("Job_Application", backref='jobz',lazy='dynamic')
    

    

    def __init__ (self,position,semester,pay,gpa_required):
        self.position = position
        self.semester = semester
        self.pay = pay
        self.gpa_required = gpa_required

# database for job application
class Job_Application(db.Model):

    __tablename__  = 'job_application'

    id = db.Column(db.Integer, primary_key=True)
    #position = db.Column(db.String(50),nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

    grade_recieved = db.Column(db.String(128), nullable=False)
    Avalialability = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    gpa_overall = db.Column(db.Float, default=0.0)
    job_status = db.Column(db.String(12), nullable=False)

    #owner = db.relationship("Student")

    

    def __init__ (self,grade_recieved,Avalialability,bio,gpa_overall,job_status,owner):
        self.grade_recieved = grade_recieved
        self.Avalialability = Avalialability
        self.bio = bio
        self.gpa_overall = gpa_overall
        self.job_status = job_status
        self.owner = owner
        #self.jobz = jobz
        #self.owner_id = owner_id
        #self.student_id = student_id
        
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')