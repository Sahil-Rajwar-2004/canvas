import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox as msg
from plyer import notification

canvas = np.ones((650,1250,3),np.uint8)*255
drawing = False
color = (0,0,0)
running = True
radius = 10
title = "Canvas"

def draw(event,x,y,flags,param):
    global drawing,color
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(canvas,(x, y),radius,color,-1)

def save():
    location = filedialog.asksaveasfilename(defaultextension = ".png",filetypes = [("PNG","*.png")])
    if location:
        cv2.imwrite(location,canvas)
        notification.notify(
                title = title,
                message = f"File saved at {location}!",
                app_name = "Canvas",
                timeout = 5
            )

def penSize(change):
    global radius
    radius += change
    if radius <= 1:
        radius = 1

def load():
    file_path = filedialog.askopenfilename(filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
    if file_path:
        loaded_canvas = cv2.imread(file_path)
        if loaded_canvas is not None:
            global canvas
            canvas = loaded_canvas
            notification.notify(
                title = title,
                message = f"Loaded file from {file_path}!",
                app_name = "Canvas",
                timeout = 5
            )

def customColor():
    global color
    rgbColor,_ = colorchooser.askcolor(title="Select Color")
    if rgbColor:
        bgrColor = (int(rgbColor[2]),int(rgbColor[1]),int(rgbColor[0]))
        color = bgrColor

cv2.namedWindow("Canvas")
cv2.setMouseCallback("Canvas",draw)

while running:
    cv2.imshow("Canvas",canvas)
    key = cv2.waitKey(1)

    if key == 27:
        ask = msg.askyesno("Warning", "Want to save the file before quitting?")
        if ask:
            save()
        running = False
    elif key == ord("i"):
        info = Tk()
        info.resizable(False, False)
        info.geometry("350x250")
        label_text = """[Esc]: Exit\n[i]: Display Info\n[r]: Red\n[g]: Green\n[b]: Blue\n[e]: Eraser\n[c]: Clear\n[s]: Save File\n[+]: Increase Pen Size\n[-]: Decrease Pen Size\n[p]: Customize Color"""
        label = Label(info, text=label_text, font=("Cascadia Code", 10))
        label.pack(fill = BOTH,padx = 5,pady = 5,anchor = W)
        exit_button = Button(info, bg = "#242424", fg = "#ffffff", text = "Exit", font = ("cascadia code",9), command = info.destroy)
        exit_button.pack(ipadx = 10)
        info.mainloop()
    elif key == ord("r"):
        color = (0,0,255)
    elif key == ord("g"):
        color = (0,255,0)
    elif key == ord("b"):
        color = (255,0,0)
    elif key == ord("e"):
        color = (255,255,255)
    elif key == ord("c"):
        canvas = np.ones((650,1250,3),np.uint8)*255
    elif key == ord("s"):
        save()
    elif key == ord("l"):
        ask = msg.askyesno("Warning","Would you like to save the current file?")
        if ask:
            save()
        load()
    elif key == ord("+"):
        penSize(1)
    elif key == ord("-"):
        penSize(-1)
    elif key == ord("p"):
        customColor()

cv2.destroyAllWindows()
