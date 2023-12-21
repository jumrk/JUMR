import cv2
import imutils
import numpy as np
import pytesseract
import re


from tkinter import filedialog
from tkinter import Label
from tkinter import Tk
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from tkinter import Button

from PIL import Image,ImageTk
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'  
tk=Tk()
tk.title("Pytesseract")
tk.geometry("700x500+100+80")
tk.resizable(0,0)
tk.configure(background="gray")

def find_contours(image):
    cnts= cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)    
    screenCnt = None
    return cnts

def OpenFile():
    global img
    try:
        f_types = [('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        print(filename)
        img = cv2.imread(filename)
        img = imutils.resize(img, width=550)
        imgtk = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgtk = Image.fromarray(imgtk)
        imgtk = ImageTk.PhotoImage(image=imgtk)
        im=Label(image=imgtk)
        im.image=imgtk
        im.pack()
        im.place(x=30,y=10)
    except:
        print("no image")
    

def image_process():
    global img
    try:
        img = imutils.resize(img, width=550)
        blur = cv2.GaussianBlur(img, (5,5),0)  
        
        lower_white=np.array([0,0,200])  #hsv
        upper_white=np.array([180,30,255])
    
        
        hsv_img=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
        mask_white=cv2.inRange(hsv_img,lower_white,upper_white)
         
        cnts_white =  find_contours(mask_white)
        for cw in cnts_white:  
            if cv2.contourArea(cw)>1000:
                (x,y,w,h) = cv2.boundingRect(cw)
                Cropped_white = mask_white[y:y+h, x:x+w]
                
                if h > 20 and h < 80  and w >160 and w < 400 :
                    print(w,h)
                    blur_crop = blur[y:y+h, x:x+w]
    
                    gray = cv2.cvtColor(blur_crop, cv2.COLOR_BGR2GRAY)
                    bienso = pytesseract.image_to_string(gray,config='--psm 6')
                    bienso = re.sub("[^-.qA-Za-z0-9]","",bienso)
                    print(bienso)
                    
                    
                    lb01=Label(tk,fg="#8B8B00",bg="#EEEED1",relief ="ridge" ,font="Times 15",width = 35, text=bienso)
                    lb01.pack()
                    lb01.place(x=200,y=448)
                
                    cv2.rectangle(img,(x,y), (x+w,y+h), (0, 255, 0), 2)
                    cv2.putText(img,bienso,(x,y+h+20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    imgtk = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    imgtk = Image.fromarray(imgtk)
                    imgtk = ImageTk.PhotoImage(image=imgtk)
                    im=Label(image=imgtk)
                    im.image=imgtk
  im.pack()
                    im.place(x=30,y=10)
                    img = None
    except:
        print("no image")

    
    
def main_loop():
    tk.after(10,  main_loop)

BT = Button(tk, text ="Load",bg = "yellow",width=9,height = 1, command = OpenFile)
BT.pack()
BT.place(x=10,y=450)

BT = Button(tk, text ="Detect",bg = "green",width=9,height = 1, command = image_process)
BT.pack()
BT.place(x=90,y=450)

lb01=Label(tk,fg="#8B8B00",bg="#EEEED1",relief ="ridge" ,font="Times 15",width = 35, text="")
lb01.pack()
lb01.place(x=200,y=448)


main_loop()
tk.mainloop()
cv2.destroyAllWindows()