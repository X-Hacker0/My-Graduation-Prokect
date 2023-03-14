# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 09:53:18 2022

@author: oday
"""


import face_recognition  # Python Library for Face Recognition System
import cv2  # OpenCV Library for Facial Recognition using Real time web data.
import os
import subprocess
from Crypto import Random  # for SSL Encryption
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import numpy as np


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, "rb") as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", "wb") as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, "rb") as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], "wb") as fo:
            fo.write(dec)
        os.remove(file_name)

    def get_all_files(self):
        root = tk.Tk()
        root.withdraw()
        folder_selected = askdirectory(
            initialdir="./DB3_B/", title="Select the Directory to be encrypted"
        )
        dir_path = folder_selected
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if fname != "script.py" and fname != "data.txt.enc":
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):

        dirs = self.get_all_files()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.get_all_files()
        for file_name in dirs:
            self.decrypt_file(file_name)

    def get_key_from_face(self):
        # Initialize variables
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        video_capture = cv2.VideoCapture(0)
        face_encodings = []
        face_names = []
        process_this_frame = True

        # Load your face encoding
        your_face_encoding = face_recognition.load_image_file('dataSet/User.1.1.jpg')
        your_face_encoding = face_recognition.face_encodings(your_face_encoding)[0]

        # Loop through the video frames
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []

                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    match = face_recognition.compare_faces([your_face_encoding], face_encoding)
                    name = "Unknown"

                    if match[0]:
                        # If your face is recognized, return the key
                        return self.key

            process_this_frame = not process_this_frame

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


def main():
    clear = lambda: os.system("cls")
    key = b"[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e"
    enc = Encryptor(key)

    # Get the key from your face
    key = enc.get_key_from_face()

    while True:
        clear()
        choice = int(input( "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the "
                            "directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))

        clear()
        if choice == 1:
            root = tk.Tk()
            root.withdraw()
            file_path = askopenfilename(initialdir='./DB3_B/', title='Select the file to be encrypted', filetypes=[("Allfiles", "*.*")]) # show an "Open" dialog box and return the path to the selected file
            print(file_path)
            enc.encrypt_file(file_path)
        elif choice == 2:
            root = tk.Tk()
            root.withdraw()
            file_path = askopenfilename(initialdir='./DB3_B/', title='Select the file to be decrypted', filetypes=[("Allfiles", "*.*")]) # show an "Open" dialog box and return the path to the selected file
            print(file_path)
            enc.decrypt_file(file_path)
        elif choice == 3:
            enc.encrypt_all_files()
        elif choice == 4:
            enc.decrypt_all_files()
        elif choice == 5:
            exit()
        else:
            print("Please select a valid option!")


if __name__ == "__main__":
    main()
