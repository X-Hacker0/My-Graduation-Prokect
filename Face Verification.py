# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 07:12:53 2022

@author: oday
"""


import ctypes
import datetime
import os
import sys
import time
from math import sin, cos, radians
import PIL
import cv2
import numpy as np
import pyautogui as pyautogui
from PIL import Image
from tkinter import *
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import win32gui, win32con

splash_screen_root = Tk()

width_of_window = 1080
height_of_window = 720
screen_width = splash_screen_root.winfo_screenwidth()
screen_height = splash_screen_root.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
splash_screen_root.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))



#splash_screen_root.geometry("400x250")
splash_screen_root.title("Multifactor Face Authentication Technique")

splash_screen_root.overrideredirect(1)

width = 1080
height = 700

image = Image.open("pic.png")
im = image.resize((width,height),Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(im)
ttk.Label(image=img).grid()


s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='lime green')
pb=Progressbar(splash_screen_root,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=2000,mode='indeterminate')
pb.place(x=-800,y=700)


def PrograssBar():

    r=0
    for i in range(100):
        pb['value']=r
        splash_screen_root.update_idletasks()
        time.sleep(0.03)
        r=r+1

def main():
    PrograssBar()
    splash_screen_root.destroy()
    root=Tk()
    root.title("Face Is The Key")
    root.geometry("900x500")
    capt=ttk.Button(root,text='Capture Your Face')
    capt.pack()
    capt.config(command=create)
    lock=ttk.Button(root,text='Start Windows Lock')
    lock.pack()
    lock.config(command=detect)
    track1=ttk.Button(root,text='Start Face Tracking')
    track1.pack()
    track1.config(command=track)
    quitWindow = tk.Button(root, text="Quit",command=root.destroy)
    quitWindow.pack()
    copy_right1 = tk.Label(root,text ='powerd by :\n Oday Abuzaid : 2019904091 \n Ayham Doumi : 2019804005 \n Thaer Alshorman : 2019804002')
    copy_right1.place(relx = 1.0,rely = 1.0,anchor ='se')
    copy_right2 = tk.Label(root,text ='Supervisior Name : \n Dr.Adnan Rawashdeh ')
    copy_right2.place(relx = 0.0,rely = 1.0,anchor ='sw')
    copy_right3 = tk.Label(root,text ='Yarmouk Universty  \n Cyber Security \n Team#3: ')
    copy_right3.place(relx = 0.5,rely = 0.5,anchor ='center')
    copy_right3.config(font=('Helvatical bold',26))
splash_screen_root.after(2000, main)
hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

def create():
    if not os.path.isdir("dataSet"):
        os.mkdir("dataSet")
    if not os.path.isfile("haarcascade_frontalface_default.xml"):
        print("Cascade Classifier File Not Found")
        main()
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    cam = cv2.VideoCapture(0);
    img = cv2.VideoCapture(0)
    id=1
    sampleNum=0
    while(True):
        ret,img = cam.read();
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray,1.3,5);
        for (x,y,w,h) in faces:
            sampleNum=sampleNum+1
            cv2.imwrite("dataSet/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.waitKey(100);
        cv2.imshow("Face",img);
        cv2.waitKey(1);
        if(sampleNum>20):
            break
            id=id+1
    cam.release()
    cv2.destroyAllWindows()
    train()
    main()

def train():
    if not os.path.isdir("recognizer"):
        os.mkdir("recognizer")
    if not os.path.isdir("dataSet"):
        print("No capture faces found, run the option 1 again !!!!!!!")
        main()
    if len(os.listdir("dataSet")) == 0:
        print("No capture faces found, run the option 1 again !!!!!!!")
        main()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataSet'

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = PIL.Image.open(imagePath).convert('L');
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces

    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)
    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()
    main()



def detect():
    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    counter_correct = 0  # counter variable to count number of times loop runs
    counter_wrong = 0

    now = datetime.datetime.now()  # extract current time
    now = now.second  # we need only seconds

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    assure_path_exists("/recognizer/")

    recognizer.read('recognizer/trainingData.yml')  # load training model

    cascadePath = "haarcascade_frontalface_default.xml"  # cascade path

    faceCascade = cv2.CascadeClassifier(cascadePath);  # load cascade

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL  # Set the font style

    cam = cv2.VideoCapture(0)

    while True:

        now1 = datetime.datetime.now()
        now1 = now1.second
        if (now1 > now + 8):
            cam.release()
            cv2.destroyAllWindows()
            ctypes.windll.user32.LockWorkStation()
            sys.exit()

        ret, im = cam.read()

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            cv2.rectangle(im, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 4)

            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])  # Recognize the face belongs to which ID

            # if(Id == 1):    # Check the ID if exist
            #   Id = "{0:.2f}%".format(round(100 - confidence, 2))

            if (confidence > 50):  # confidence usually comes greater than 80 for strangers
                counter_wrong += 1
                print("Wrong")
                Id = "Unknown + {0:.2f}%".format(round(100 - confidence, 2))
                print(confidence)
                print("counter_wrong - " + str(counter_wrong))
                cv2.rectangle(im, (x - 22, y - 90), (x + w + 22, y - 22), (0, 0, 255), -1)
                cv2.putText(im, str(Id), (x, y - 40), font, 1, (0, 0, 0), 2)
            else:  # confidence usually comes less than 80 for correct user(s)
                Id = "User Authenticated + {0:.2f}%".format(round(100 - confidence, 2))
                print("Verified")
                print(confidence)
                counter_correct += 1
                print("counter_correct - " + str(counter_correct))
                cv2.rectangle(im, (x - 22, y - 90), (x + w + 22, y - 22), (255, 255, 255), -1)
                cv2.putText(im, str(Id), (x, y - 40), font, 1, (0, 0, 0), 2)

            if (counter_wrong == 10):
                pyautogui.moveTo(48, 748)
                pyautogui.click(48, 748)
                pyautogui.typewrite("Hello Stranger!!! Whats Up.")
                cam.release()
                cv2.destroyAllWindows()
                ctypes.windll.user32.LockWorkStation()
                sys.exit()

            if (counter_correct == 50):  # if counter = 6 then program will terminate as it has recognized correct user for 6 times.
                cam.release()
                cv2.destroyAllWindows()
                sys.exit()

        cv2.imshow('Webcam', im)

        if cv2.waitKey(10) & 0xFF == ord('q'):  # If '*' is pressed, terminate the  program
                break

    cam.release()
    cv2.destroyAllWindows()
    main()



def track():
    # Load the cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Set the window name
    window_name = "Face Recognition"

    # Initialize the timer
    timer = time.time()

    # Start a infinite loop
    while True:
        # Read the frame from the webcam
        _, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # If a face is detected, draw a green rectangle around it and reset the timer
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            timer = time.time()

        # If the timer has been running for more than 5 seconds and no face has been detected, lock the system
        if time.time() - timer > 5 and len(faces) == 0:
            # Code for locking the system goes here
            print("Locking the system...")
            ctypes.windll.user32.LockWorkStation()
            break

        # Display the frame
        cv2.imshow(window_name, frame)

        # Check if the user pressed the Esc key
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    # Release the webcam and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    main()
mainloop()
main()
