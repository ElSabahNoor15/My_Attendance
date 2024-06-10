import pyrebase

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

