#!flask/bin/python
import os
import unittest

#from config import basedir
from app import app, db
from app import Student, Instructor
#import requests

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_make_student1(self):
        u = Student(first_name='First', last_name='Last', email='email@gmail.com', password='password')
        db.session.add(u)
        db.session.commit()

        self.assertEqual('First', u.first_name)
        self.assertEqual('Last', u.last_name)
        self.assertEqual('email@gmail.com', u.email)
        self.assertEqual('password', u.password)
        
        # data = {'options':'STUDENT', 'first_name':'First', 'last_name':'Last', 'email':'email@gmail.com', 'pwd':'password'}
        # requests.post('http://127.0.0.1:5000/api/Register', json=data)

    def test_make_Instructor1(self):
        u = Instructor(first_name='First', last_name='Last', email='email@gmail.com', password='password')
        db.session.add(u)
        db.session.commit()

        self.assertEqual('First', u.first_name)
        self.assertEqual('Last', u.last_name)
        self.assertEqual('email@gmail.com', u.email)
        self.assertEqual('password', u.password)

   


    def register(self, email, password,first_name,last_name,options):
        return self.app.post('/api/Register', data=dict(options=options,email=email, password=password,first_name=first_name,last_name=last_name),follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/api/',data=dict(email=email, password=password))

    def logout(self):
        return self.app.get('/api/logout',follow_redirects=True)

    


    

    


if __name__ == '__main__':
    unittest.main()