from flask import Flask, render_template, request, redirect, flash, session as flask_session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import NoResultFound
from geopy.geocoders import Nominatim
import pyrebase
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

firebaseConfig = {
    'apiKey': "AIzaSyCEQhy_52fnsW-lbhgFEd-OhODWklqLOe4",
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

# Define the base class for declarative models
Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admin'
    uname = Column(String, primary_key=True, nullable=False, unique=True)
    password = Column(String)

Session = sessionmaker(bind=engine)
session = Session()

# Create the tables in the database
Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loginpage')
def loginPage():
    return render_template('Login_page.html')

@app.route('/loggedin', methods=['POST'])
def loggedin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(username, password)
            flash('You are successfully logged in!', 'success')
            return render_template('Attendance_map_page.html')
        except:
            flash("Invalid Username or Password.", 'danger')
            return redirect('/loginpage')

@app.route('/registerpage')
def registerPage():
    return render_template('Register_page.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            auth.create_user_with_email_and_password(username, password)
            flash('Registration successful! Please log in.', 'success')
            return redirect('/loginpage')
        except:
            flash('Registration failed. Please try again.', 'danger')
            return redirect('/registerpage')

@app.route('/locationLog', methods=['POST'])
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
        db.child("AttendanceDetails").push(attendanceData)
        flash('Location logged successfully!', 'success')
    return render_template('Attendance_map_page.html')

@app.route('/logout')
def logout():
    auth.current_user = None
    return redirect('/loginpage')

@app.route('/adminlogin')
def adminlogin():
    return render_template('admin_loginPage.html')

@app.route('/adminloggedin', methods=['POST'])
def adminloggedin():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['password']
        try:
            admin = session.query(Admin).filter_by(uname=uname).one()
            if admin.password == password:
                flask_session['admin'] = uname
                flash('Admin login successful!', 'success')
                return redirect('/admin')
            else:
                flash('Invalid username or password.', 'danger')
                return redirect('/adminlogin')
        except NoResultFound:
            flash('Admin not found.', 'danger')
            return redirect('/adminlogin')

@app.route('/admin')
def admin():
    if 'admin' not in flask_session:
        flash('Please log in as admin to access this page.', 'danger')
        return redirect('/adminlogin')
    return render_template('admin.html')

@app.route('/adminlogout')
def adminlogout():
    flask_session.pop('admin', None)
    flash('You have successfully logged out.', 'success')
    return redirect('/adminlogin')

# @app.route('/locationlogView',  methods=['GET'])
# def logview():
#     if request.method=='GET':
#         Attendance = db.child("AttendanceDetails").order_by_child("timestamp").get()
#         eachattendance = Attendance.each()
#         for i in eachattendance:
#             username = i.val()["username"]
#             location = i.val()["location"]
#             locationDesc = i.val()["locationDesc"]
#             timestamp = i.val()["timestamp"]
#             print(username+' '+location+' '+locationDesc+' '+timestamp)

#     return render_template('attendance_view.html')

@app.route('/locationlogView', methods=['GET'])
def logview():
    if request.method == 'GET':
        Attendance = db.child("AttendanceDetails").order_by_child("timestamp").get()
        attendance_list = []
        for i in Attendance.each():
            attendance_list.append(i.val())
    return render_template('attendance_view.html', attendance_list=attendance_list)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
