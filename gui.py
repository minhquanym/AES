from tkinter import *
from tkinter import font
from aes import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter.filedialog import askopenfile 
import os.path
import random
import string

bg_color = "azure3"

root = Tk()
root.geometry("750x600")
root.title("ENCRYPTION PROGRAM") 
root.configure(background = bg_color)


def hide_frame() :                                                                                                                                                                                                                                                                                                                                                                                                                      
    first_frame.grid_forget()
    sec_frame.grid_forget()

def send_output(key,output):
    global_text.set(output)
    global_key.set(key)

def open_file(): 
    
    ex.delete(0,END)

    file1 = askopenfile(mode ='r', filetypes =[('Text Files', '*.txt')]) 
    key=ex.get()
    
    file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 3))
    file2 = open('Encrypted/'+file_name+'.txt',mode='w+')
    if file1 is not None: 
        text = file1.read() 
        messagebox.showinfo("FILE CONTENT",text)
        output=aesEncrypt(text,key)
        
        messagebox.showinfo("ENCRYPTED OUTPUT",output)
        messagebox.showinfo("OUTPUT SAVED IN:",'Encrypted/'+file_name+'.txt')
        file2.write(output)
        file1.close()
        file2.close() 
    else :
        messagebox.showerror("ERROR","File is EMPTY!!")

def popup():
    
    key=e1.get()
    text=e2.get()
    name = e3.get()
    
    
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    
    
    if(text==""):
        messagebox.showerror("ERROR","Enter 16 bit text only")
    else:
        file = open('Encrypted/'+name+'.txt',"w+")
        output=aesEncrypt(text,key)
        
        messagebox.showinfo("ENCRYPTED OUTPUT",output)
        messagebox.showinfo("OUTPUT SAVED IN:",'Encrypted/'+name+'.txt')
        file.write(output)
        file.close()



def popdown():
    name = e4.get()
    file1 = open('Encrypted/'+name+'.txt',"r")
    file2 = open('Decrypted/'+name+'decrypted.txt','w+')
    text= file1.read()
    key=e5.get() 
    e4.delete(0,END)
    
    file1.close()
    if(text==""):
        messagebox.showerror("ERROR","Please enter valid text")
    else:
        output=aesDecrypt(text,key)
        messagebox.showinfo("DECRYPTED OUTPUT",output)
        file2.write(output)
        messagebox.showinfo('Decrypted Output saved in file : ','Decrypted/'+name+'decrypted.txt')
        file2.close()




def file_one():
    hide_frame()
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    ex.delete(0,END)
    first_frame.grid(sticky=N+S+W+E)
    first_frame.configure(background = bg_color)
    myLabel1 = Label(first_frame,text="TEXT ENCRYPTION",bg=bg_color,fg="OrangeRed4",font="Helvetica 20 bold ")
    myLabel2 = Label(first_frame,text="ADVANCED ENCRYPTION STANDARD",bg=bg_color,fg="OrangeRed4",font="Helvetica 18 bold ")
    myLabel1.grid(row=0,column=1)
    myLabel2.grid(row=1,column=1)
    
    myLabel3=Label(first_frame,text="KEY(16 char)",bg=bg_color,fg="black",font="Helvetica 15 bold ")
    myLabel3.grid(row=3,column=0,pady=20,ipadx=10,sticky=E)
    e1.grid(row=3,column=1,pady=20)
    e1.insert(0,"")
    
    myLabel4=Label(first_frame,text="TEXT",bg=bg_color,fg="black",font="Helvetica 15 bold ")
    myLabel4.grid(row=4,column=0,pady=20,ipadx=10,sticky=E)
    e2.grid(row=4,column=1,pady=20)
    e2.insert(0,"Enter text here")
    
    
    myLabel5=Label(first_frame,text="OUTPUT FILENAME",bg=bg_color,fg="black",font="Helvetica 15 bold ")
    myLabel5.grid(row=5,column=0,pady=20,ipadx=10,sticky=E)
    e3.grid(row=5,column=1,pady=20)
    
    encryptButton=Button(first_frame,text="Encrypt",fg="white",bg="OrangeRed4",command=popup,activeforeground="black",activebackground="coral",relief="raised",bd=9)
    encryptButton.grid(row=6,column=1)

    button_quit=Button(first_frame,text="EXIT",command=root.quit,fg="white",bg="OrangeRed4",activeforeground="black",activebackground="coral",relief="raised",bd=9)
    button_quit.grid(row=12,column=1,pady=20)


def file_two():
    hide_frame()
    sec_frame.grid(sticky=N+S+W+E)
    sec_frame.configure(background = bg_color)
    
    myLabel1 = Label(sec_frame,text="TEXT DECRYPTION",bg=bg_color,fg="OrangeRed4",font="Helvetica 20 bold")
    myLabel2 = Label(sec_frame,text="ADVANCED ENCRYPTION STANDARD",bg=bg_color,fg="OrangeRed4",font="Helvetica 18 bold")
    myLabel1.grid(row=0,column=1)
    myLabel2.grid(row=1,column=1)
    
    instLabel = Label(sec_frame,text="Enter the filename in '~/AES/Encrypted'  ",font="Helvetica 15 bold ",bg=bg_color)
    instLabel.grid(row=3,column=1)

    fileLabel = Label(sec_frame,text="FILENAME  ",font="Helvetica 15 bold ",bg=bg_color)
    fileLabel.grid(row=4,column=0,pady=20,ipadx=10,sticky=E)
    e4.grid(row=4,column=1,pady=40)
    
    myLabel4=Label(sec_frame,text="KEY(16 BIT)",font="Helvetica 15 bold ",bg=bg_color)
    myLabel4.grid(row=6,column=0,pady=20,ipadx=10,sticky=E)
    e5.grid(row=6,column=1,pady=20)
    
    decryptButton=Button(sec_frame,text="Decrypt",fg="white",bg="OrangeRed4",command=popdown,activeforeground="white",activebackground="coral",relief="raised",bd=9)
    decryptButton.grid(row=9,column=1)
    
    button_quit=Button(sec_frame,text="EXIT",command=root.quit,fg="white",bg="OrangeRed4",activeforeground="white",activebackground="coral",relief="raised",bd=9)
    button_quit.grid(row=10,column=1,pady=20)


menubar = Menu(root)
menubar.add_command(label="ENCRYPT",activebackground="OrangeRed4",activeforeground="black",command=file_one)
menubar.add_command(label="DECRYPT",activebackground="OrangeRed4",activeforeground="black",command=file_two)
root.config(menu=menubar)
first_frame = Frame(root,width=600,height=400)
sec_frame = Frame(root,width=600,height=400)
e1 = Entry(first_frame,width=65,borderwidth=2)
e2 = Entry(first_frame,width=65,borderwidth=2)
e3 = Entry(first_frame,width=65,borderwidth=2)
ex = Entry(first_frame,width=65,borderwidth=2)
global_text=StringVar()
global_key=StringVar()
e4 = Entry(sec_frame,width=70,borderwidth=2)
e5 = Entry(sec_frame,width=70,borderwidth=2,textvariable=global_key)
file_one()
root.mainloop()