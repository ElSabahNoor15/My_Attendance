from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Integer, String
from geopy.geocoders import Nominatim
import geocoder
from datetime import datetime


app = Flask(__name__)


# Create an SQLite database engine
engine = create_engine('sqlite:///Compunetsystem.db', echo=True)

# Define the base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    sno = Column(Integer, autoincrement=True, unique=True)
    username = Column(String, primary_key=True)
    password = Column(String)

class Attendance(Base):
    __tablename__ = 'attendance'
    attendId = Column(Integer, autoincrement=True, unique=True)
    username = Column(String)
    location = Column(String)
    locationDesc = Column(String)
    dateTime = Column(DateTime, default=datetime.now, primary_key=True)

    def __repr__(self) -> str:
        return f"{self.attendId} - {self.username}"

class Admin(Base):
    __tablename__ = 'admin'
    uname = Column(String, primary_key=True, nullable=False, unique=True)
    password = Column(String)


Session = sessionmaker(bind=engine)
session = Session()

# Create the tables in the database
Base.metadata.create_all(engine)
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
        
        user = session.query(User).filter_by(username=username).first()
        if(user.username == username and user.password == password):
            #flash('You are successfully logged in!')
            return render_template('Attendance_map_page.html', user = user)
        else:   
            return redirect('/loginpage')

            #flash('Your credential does not match!')
    #user = User.query.all()
    #return render_template('Login_page.html', user=user)
    

@app.route('/locatioLog', methods=['GET','POST'])
def location_logging():
    if request.method=='POST':

        username = request.form['username']
        geoloc = Nominatim(user_agent="GetLoc")
        g = geocoder.ip('me')
        latlong = g.latlng
        location = ', '.join(str(e) for e in latlong)
        locname = geoloc.reverse(latlong)
        locationDesc = ' '.join(str(e) for e in locname)
        attendance =  Attendance(username=username, location=location, locationDesc = locationDesc)
        session.add(attendance)
        session.commit()
    return render_template('Attendance_map_page.html')
    

@app.route('/registerpage')
def registerPage():
    return render_template('Register_page.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':       
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)      
        session.add(user)
        session.commit()
    return render_template('Login_page.html')

@app.route('/adminlogin')
def adminlogin():
    return render_template('admin_loginPage.html')

@app.route('/adminloggedin', methods=['GET','POST'])
def adminloggedin():
    if request.method=='POST':
        uname = request.form['uname']
        password = request.form['password']
        
        admin = session.query(Admin).filter_by(uname=uname).first()
        if(admin.uname == uname and admin.password == password):
            #flash('You are successfully logged in!')
            return redirect('/admin')
        else:   
            return redirect('/adminlogin')

            #flash('Your credential does not match!')
    #user = User.query.all()
    
    return render_template('admin_loginPage.html')


@app.route('/admin')
def admin():
    allusers = session.query(User)
    print(allusers)
    return render_template('admin.html', allusers=allusers)

@app.route('/locationlogView')
def logview():
    attendance = session.query(Attendance)
    print(attendance)
    return render_template('attendance_view.html', attendance=attendance)

if __name__ == "__main__":
    app.run(debug=True,port=8000)
    