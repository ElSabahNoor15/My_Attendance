from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Integer, String
from geopy.geocoders import Nominatim
import geocoder
from datetime import datetime
import json
from urllib.request import urlopen
import pyrebase

app = Flask(__name__)


firebaseConfig = {'apiKey': "AIzaSyCEQhy_52fnsW-lbhgFEd-OhODWklqLOe4",
  'authDomain': "csauth-f6467.firebaseapp.com",
  'projectId': "csauth-f6467",
  'storageBucket': "csauth-f6467.appspot.com",
  'messagingSenderId': "906880690426",
  'appId': "1:906880690426:web:a6a7a7fca7ed297b59c143",
  'measurementId': "G-R3KLF3W3Q4",
  'databaseURL': "https://csauth-f6467-default-rtdb.asia-southeast1.firebasedatabase.app/"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
# Create an SQLite database engine
engine = create_engine('sqlite:///Compunetsystem.db', echo=True, pool_size=10, max_overflow=20)
# engine = create_engine('postgres://csadmin:User123@localhost:5432/csattendanceapp', echo=True, pool_size=10, max_overflow=20)

# # Define the base class for declarative models
Base = declarative_base()

# class User(Base):
#     __tablename__ = 'user'
#     sno = Column(Integer, autoincrement=True, unique=True)
#     username = Column(String, primary_key=True)
#     password = Column(String)

# class Attendance(Base):
#     __tablename__ = 'attendance'
#     attendId = Column(Integer, autoincrement=True, unique=True)
#     username = Column(String)
#     location = Column(String)
#     locationDesc = Column(String)
#     dateTime = Column(DateTime, default=datetime.now, primary_key=True)

#     def __repr__(self) -> str:
#         return f"{self.attendId} - {self.username}"

# class Admin(Base):
#     __tablename__ = 'admin'
#     uname = Column(String, primary_key=True, nullable=False, unique=True)
#     password = Column(String)


Session = sessionmaker(bind=engine)
session = Session()

# Create the tables in the database
# Base.metadata.create_all(engine)

# admin = Admin(uname = 'ComAdmin', password='Admin1997$')
# session.add(admin)
# session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loginpage')
def loginPage():
    return render_template('Login_page.html')

@app.route('/loggedin', methods=['GET','POST'])
def loggedin():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        try:

            auth.sign_in_with_email_and_password(username,password)
        
            print('You are successfully logged in!')
            return render_template('Attendance_map_page.html')
        except:
            print("Invalid Username or Password.")   
            return redirect('/loginpage')

@app.route('/registerpage')
def registerPage():
    return render_template('Register_page.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':       
        username = request.form['username']
        password = request.form['password']
        userauth = auth.create_user_with_email_and_password(username,password)
    return render_template('Login_page.html')

@app.route('/locationLog', methods=['GET', 'POST'])
def location_logging():
    if request.method == 'POST':
        uname = request.form['uname']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        location = f"{latitude},{longitude}"
        
        geoloc = Nominatim(user_agent="GetLoc")
        locname = geoloc.reverse(location)
        locationDesc = ' '.join(str(e) for e in locname)

        attendanceData = {
            "username": uname,
            "location": location,
            "locationDesc": locationDesc,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.push(attendanceData)
    return render_template('Attendance_map_page.html')

@app.route('/logout')
def logout():
    auth.current_user = None
    return redirect('/loginpage')   



# @app.route('/adminlogin')
# def adminlogin():
#     return render_template('admin_loginPage.html')

# @app.route('/adminloggedin', methods=['GET','POST'])
# def adminloggedin():
#     if request.method=='POST':
#         uname = request.form['uname']
#         password = request.form['password']
        
#         admin = session.query(Admin).filter_by(uname=uname).first()
#         if(admin.uname == uname and admin.password == password):
#             #flash('You are successfully logged in!')
#             return redirect('/admin')
#         else:   
#             return redirect('/adminlogin')

#             #flash('Your credential does not match!')
#     #user = User.query.all()
    
#     return render_template('admin_loginPage.html')


# @app.route('/admin')
# def admin():
#     allusers = session.query(User)
#     print(allusers)
#     return render_template('admin.html', allusers=allusers)

# @app.route('/locationlogView')
# def logview():
#     attendance = session.query(Attendance)
#     print(attendance)
#     return render_template('attendance_view.html', attendance=attendance)

if __name__ == "__main__":
    app.run(debug=True,port=8000)
    