import threading
import tkinter as tk
from tkinter.ttk import *
from tkinter import DISABLED, NORMAL, RIGHT
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# this is the configuration key that links me to my firebase db
firebaseConfig = {
  'apiKey': "AIzaSyBYgdf9hXlpXGnAKDn2frp1iibzRWkky5s",
  'authDomain': "dont-stop-trying.firebaseapp.com",
  'databaseURL': "https://trialauth-7eea1.firebaseio.com",
  'projectId': "dont-stop-trying",
  'storageBucket': "dont-stop-trying.appspot.com",
  'messagingSenderId': "663416344871",
  'appId': "1:663416344871:web:528346d0ec57ca421f9902",
  'measurementId': "G-V8VH5PN6K4"
}

cap=0

cred = credentials.Certificate("cert.json")
firebase_admin.initialize_app(cred)

# initializing the tkinter window and frames
uii = tk.Tk()
uii.geometry('720x512')
home = tk.Frame(uii)
calc = tk.Frame(uii)
out = tk.Frame(uii)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firestore.client()


def show_frame(frame):
    frame.tkraise()
    # this function changes frames in the window to the next frame


for frame in (home, calc, out):
    frame.grid(row=0, column=0, sticky='nsew')


grades = {'A': 5, 'B': 3, 'C': 2, 'D': 1, 'F': 0}


def datastore():
    if semester.get() == 'Alpha':
        db.collection('users').document('alpha').set({'courses': firestore.ArrayUnion([courses.get()])}, merge=True)
        db.collection('users').document('alpha').set({'grade': firestore.ArrayUnion([grade.get()])}, merge=True)
        db.collection('users').document('alpha').set({'units': firestore.ArrayUnion([weight.get()])}, merge=True)
    if semester.get() == 'Omega':
        db.collection('users').document('Omega').set({'courses': firestore.ArrayUnion([courses.get()])}, merge=True)
        db.collection('users').document('Omega').set({'grade': firestore.ArrayUnion([grade.get()])}, merge=True)
        db.collection('users').document('Omega').set({'units': firestore.ArrayUnion([weight.get()])}, merge=True)
    # this function collects input and saves it on cloud firestore database


def delete():
    if semester.get() == 'alpha':
        db.collection('users').document('alpha').update({
            'course10': firestore.DELETE_FIELD
        })
    if semester.get() == 'Omega':
        db.collection('users').document('Omega').delete()
    # this function deletes the current entry from cloud firestore


def login():
    u_name = str(Entry.get(open_entry))
    pas_word = str(Entry.get(open_entry2))
    try:
        login = auth.sign_in_with_email_and_password(u_name, pas_word)
        reply_label.config(text="Successfully logged in!")
        but.config(state=NORMAL)
    except:
        reply_label.config(text="Invalid email or password")
    return
    # this function uses firebase authetication to login

def calculate_gpa():
    dirr = db.collection('users')
    docs = dirr.where("courses", "array_contains", "CIT101").get()
    for doc in docs:
        reply = (doc.to_dict())
        weight_value = (reply['units'])
        weight_value = map(int, weight_value)
        li = [i for i in weight_value]
        sum_unit = (sum(li))

        grade_value = (reply['grade'])
        grade_c = {'A': 5, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        if grade_value:
            grad_list = [grade_c[grade] for grade in grade_value if grade in grade_c]
            products = [a * b for a, b in zip(li, grad_list)]
            sum_points = sum(products)
            gpa = sum_points/sum_unit
            print(gpa)
            output.config(text=gpa)
            # this is the calculator function


header = Style()
header.configure('head.TLabel', font=('coolvetica rg', 50), foreground='#892CAA')

header = Style()
header.configure('bod.TLabel', font=('coolvetica rg', 28), foreground='#892CAA')

body = Style()
body.configure('bodyy.TLabel', font=('product sans', 20), foreground='Black',)

body = Style()
body.configure('body2.TLabel', font=('product sans', 100))

body = Style()
body.configure('body.TEntry', font=('product sans', 20))

body = Style()
body.configure('body.TCombobox')

body = Style()
body.configure('body.TButton')

heading = Style()
Style().configure("sexy.TButton", padding=6, relief="flat")


openn = Label(home, text='Login', style='head.TLabel')
openn.pack(fill='both', expand=True)

user_label = Label(home, text='Email', style='bodyy.TLabel')
user_label.pack(fill='both', expand=True)

open_entry=  Entry(home, style='body.TEntry')
open_entry.pack(fill='x', ipady=10)

pass_label = Label(home, text='Password', style='bodyy.TLabel')
pass_label.pack(fill='both', expand=True)

open_entry2 = Entry(home, style='body.TEntry')
open_entry2.pack(fill='x',ipady=10)

reply_label = Label(home,text='', style='bodyy.TLabel')
reply_label.pack(fill='both', expand=True)

but4=Button(home, text='Login', command=login, style='sexy.TButton')
but4.pack(fill='x', ipady=10)

but = Button(home, text='Result upload' ,command=lambda:show_frame(calc), style='sexy.TButton', state=DISABLED)
but.pack(fill='x', ipady=10)

openn1 = Label(calc,text='Welcome',style='head.TLabel')
openn1.pack()

info_dis = Label(calc, text='Enter information below', style='bodyy.TLabel')
info_dis.pack()

s_label = Label(calc,text='semester',style='bodyy.TLabel')
s_label.pack()

semester = tk.StringVar()
sem_box = Combobox(calc, textvariable=semester, style='com.TCombobox')
sem_box['values'] = ('Alpha', 'Omega')
sem_box['state'] = 'readonly'
sem_box.pack(fill='x',ipady=10)

c_label = Label(calc,text='course',style='bodyy.TLabel')
c_label.pack()

courses = tk.StringVar()
course_box = Combobox(calc, textvariable=courses,style='com.TCombobox')
course_box['values'] = ('ECN323', 'ECN311','ECN355','EEE412','CIT101','BUS677','FINN00','ECN443','GEC511','CEN223')
course_box['state'] = 'readonly'
course_box.pack(fill='x',ipady=10)

g_label=Label(calc,text='grade',style='bodyy.TLabel')
g_label.pack()

grade = tk.StringVar()
grade_box = Combobox(calc, textvariable=grade, style='com.TCombobox')
grade_box['values'] = ('A', 'B','C','D','F')
grade_box['state'] = 'readonly'
grade_box.pack(fill='x',ipady=10)


w_label=Label(calc,text='weight',style='bodyy.TLabel')
w_label.pack()

weight = tk.StringVar(value=0)
spin_box = Spinbox(
    calc,
    from_=0,
    to=6,
    textvariable=weight,
    wrap=True)
spin_box.pack(fill='x',ipady=10)

but1=Button(calc,text='NEXT', command=datastore, style='sexy.TButton')
but1.pack(side=RIGHT)

but3=Button(calc,text='SUBMIT', style='sexy.TButton',command=threading.Thread(target=calculate_gpa).start)
but3.pack(side=RIGHT)

but6=Button(calc,text='CLEAR', style='sexy.TButton', command=delete)
but6.pack(side=RIGHT)

but2=Button(calc,text='CALCULATE', style='sexy.TButton', command=lambda:show_frame(out))
but2.pack(side=RIGHT)

openn2=Label(out, text='Your estimated GPA is', style='bodyy.TLabel')
openn2.pack()

output=Label(out, text='0.00', style='head.TLabel')
output.pack()

but2=Button(out,text='Back to Home', command=lambda:show_frame(home))
but2.pack()

show_frame(home)
uii.mainloop()