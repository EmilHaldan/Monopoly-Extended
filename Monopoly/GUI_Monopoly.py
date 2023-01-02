
import tkinter as tk
from tkinter import *
from tkinter import filedialog, Text
import os
from PIL import Image
from PIL import ImageTk



# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)


def button_1_write_text():  
    global mycanvas
    myLabel = Label(mycanvas, text = "Enter Text here")
    myLabel.grid(row= 2, column = 3)
    myLabel.pack()


if __name__ == "__main__":
    root = Tk()
    root.title("GUI Monopoly Extended")

    myframe = Frame(root)
    myframe.pack(fill=BOTH, expand=YES)
    mycanvas = ResizingCanvas(myframe,width=1920, height=1000, bg="black", highlightthickness=0) #, image = board_image)
    
   
    #imgLabel = Label(root, image=photo)
        
    #imgLabel.pack(fill = None)

    # add some widgets to the canvas
    mycanvas.create_rectangle(900, 10, 1910 , 780, fill="#bd0000")  # Map
    mycanvas.create_rectangle(10, 10, 890 , 550, fill="#3a2edb") # Personal player info
    mycanvas.create_rectangle(10, 560, 890 , 990, fill="#bd0000") # Targeted player info
    mycanvas.create_rectangle(900, 790, 1910 , 990, fill="green") # buttons 
    #mycanvas.create_line(0, 0, 200, 100, fill = "green")
    #mycanvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

    #board_image=Image.open("C:\\OneDrive\\Dokumenter\\Programming\\Python Projects\\Private_Projects\\Monopoly\\Board.png")
    # try:
    board_image = Image.open(".\\Board.png")
    # except:                   
        # board_image = Image.open(".\\Monopoly\\Board.png")

    board_image_2=board_image.resize((1010,785),Image.ANTIALIAS)

    img = ImageTk.PhotoImage(board_image_2)

    mycanvas.create_image(1910,10, anchor = NE, image = img)
    mycanvas.pack(fill=BOTH, expand=YES)

        # button example
    # button_1 = Button(mycanvas,
    #     text = 'Submit', # what should the button say?
    #     command = None, #write_text, # enter the defined function in here (when you press the button)
    #     state= NORMAL, # use ACTIVE,NORMAL,DISABLED to alter its optionality
    #     padx = 40, # makes it wider
    #     pady = 20, # makes it taller
    #     fg = "black", # makes the text COLOR
    #     bg = "lightgrey" # makes the background grey
    #     )  
    # button_1.pack()  

    

    mycanvas.mainloop()

    

if __name__ == "__main__":
    main()