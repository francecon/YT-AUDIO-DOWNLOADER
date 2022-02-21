import glob
import os
import re
import sys
import urllib
from tkinter import (BOTH, CENTER, RIGHT, YES, HORIZONTAL, Button, Entry, Label, Listbox, Menu,
                     Scrollbar, StringVar, Tk, Toplevel, Y, font)
from tkinter import messagebox as m_box
from tkinter.ttk import Progressbar
from numpy import insert
import validators
from moviepy.editor import AudioFileClip
from pytube import YouTube, exceptions, request
import subprocess
from threading import Thread

request.default_range_size = 2097152  # about 2MB chunk size

ws = Tk() 
ws.title('YT Downloader - Scarica le tue canzoni') 
ws.geometry('1000x600')
ws.eval('tk::PlaceWindow . center')
if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
elif __file__:
    dirname = os.path.dirname(__file__)

# ws.iconbitmap(os.path.join(dirname, "icon", "icon.ico"))

### Center the window ###

#Same size will be defined in variable for center screen in Tk_Width and Tk_height
Tk_Width = 1000
Tk_Height = 600
   
#calculate coordination of screen and window form
x_Left = int(ws.winfo_screenwidth()/2 - Tk_Width/2)
y_Top = int(ws.winfo_screenheight()/2 - Tk_Height/2)

# Write following format for center screen
ws.geometry("+{}+{}".format(x_Left, y_Top))

###

def make_menu(w):
    global the_menu
    the_menu = Menu(w, tearoff=0)
    the_menu.add_command(label="Taglia")
    the_menu.add_command(label="Copia")
    the_menu.add_command(label="Incolla")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Taglia",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copia",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Incolla",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)


def delSelected():
    link_selected = lb.curselection()
    if len(link_selected) == 0:
        m_box.showerror("Error", "Nessun link selezionato")
    for i in link_selected:
        lb.delete(i)
        
def insert_link():
    inserted_link = link.get() 
    inserted_link.replace(" ", "")
    # check if inserted string is a valid url
    if validators.url(inserted_link):
        #check if the link is a YouTube link
        try:
            YouTube(inserted_link).check_availability()
            list_of_urls = lb.get(0, 'end')
            # check if the link was already inserted
            if inserted_link not in list_of_urls:
                lb.insert('end',inserted_link)
                yt_link.delete(0,'end')
            else:
                yt_link.delete(0,'end')
                m_box.showerror("Error", "Link YouTube già inserito!")
        except exceptions.VideoUnavailable:
            yt_link.delete(0,'end')
            m_box.showerror("Error", "Link video YouTube non disponibile!\nInserisci un link di un video YouTube!")
        except urllib.error.URLError:
            yt_link.delete(0,'end')
            m_box.showerror("Error", "Internet non disponibile")
    else:
        yt_link.delete(0,'end')
        m_box.showerror("Error", "Inserisci un link valido!")

    
def NewWindow():
    # Toplevel object which will
    # be treated as a new window
    global newWindow, lab, lab1, pb1, label2
    
    newWindow = Toplevel(ws)
    # sets the title of the
    # Toplevel widget
    newWindow.title("Download")
    # sets the geometry of toplevel
    newWindow.geometry("600x100+400+200")
    # A Label widget to show in toplevel
    lab = Label(newWindow, text ="", font=("Times", 14),justify=CENTER)
    # lab.place(relx=0.5, rely=0.5, anchor="center")
    # lab.grid(row=0,column=2)
    lab.pack(side="top")
    lab1 = Label(newWindow, text = "", font=("Arial Italic",11),justify=CENTER)
    lab1.pack(side="top")

    pb1 = Progressbar(newWindow, orient=HORIZONTAL, length=300, mode='indeterminate')
    pb1.pack(expand=True,side="left")
    # pb1.grid(row=3,column=2)
    pb1.start()

    #percentage label
    label2=Label(newWindow,text="0%",font=("Arial Bold",15))
    label2.pack(expand=True,fill=BOTH,side="left" )
    # label2.grid(row=3,column=3)

def check():
    list_of_urls = lb.get(0, 'end')
    if len(list_of_urls) == 0:
        m_box.showerror("Error", "Nessun link inserito")
    else:
        answer=m_box.askyesnocancel("Richiesta", "Vuoi davvero scaricare tutte le canzoni?")
        if answer:
            if os.path.isdir(dirname+"/Canzoni_mp4"): #if Canzoni_mp4 esiste allora chiedi se vuole cancellare
                answer=m_box.askyesnocancel("Richiesta", "Vuoi cancellare tutte le canzoni che ci sono nella cartella 'Canzoni_mp4'?")
                if answer:
                    files = glob.glob('./Canzoni_mp4/*')
                    for f in files:
                        os.remove(f)
            download()
        else:
            pass

def threading():
    # Call check function
    t1=Thread(target=check)
    t1.start()

def threading1():
    # Call check function
    t1=Thread(target=insert_link)
    t1.start()

def changeText(txt,title):
    lab.configure(text=txt)
    lab1.configure(text=title)

def on_progress(stream, chunk, bytes_remaining):
    global inc
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    inc=int(percentage_of_completion)
    
    pb1["value"]+=inc-pb1["value"]
    label2.config(text=f"{inc}%")
    if pb1["value"]==100:
        pb1.grid_forget()
        label2.grid_forget()
        label2["text"]="0%"
        pb1["value"]=0


def download():
    flag = False #flag per vedere se il download è andato a buon fine
    NewWindow()
    list_of_urls = lb.get(0, 'end')
    try:
        for i in list_of_urls:
            if flag:
                label2.pack()
            pb1.config(mode="determinate")
            pb1.stop()
            yt = YouTube(i)
            title = yt.title
            title = re.sub(r'[\\/*?:"<>|]',"-",title)
            changeText("Sto SCARICANDO: \n",title)
            default_filename = title + ".mp4"
            new_filename = title+'.mp3'
            parent_dir = os.path.join(dirname, "Canzoni_mp4")
            str = yt.streams.get_audio_only()
            yt.register_on_progress_callback(on_progress)
            str.download(output_path=parent_dir,filename=default_filename,max_retries=10)
            
            try:
                changeText("Sto CONVERTENDO da MP4 a MP3:\n",title)
                pb1.config(mode="indeterminate")
                pb1.start()
                label2.pack_forget()
                subprocess.run([
                    'ffmpeg', '-y',
                    '-i', os.path.join(parent_dir, default_filename),
                    os.path.join(parent_dir, new_filename)
                ],shell=True)
                # audioclip = AudioFileClip(os.path.join(parent_dir, default_filename))
                # audioclip.write_audiofile(os.path.join(parent_dir, new_filename))
                # audioclip.close()
                
                files = glob.glob(parent_dir+'/*.mp4') 
                for f in files:
                    os.remove(f) 
                flag = True 
            except:
                flag=False
                files = glob.glob(parent_dir+'/*.mp4') 
                for f in files:
                    os.remove(f)
                newWindow.destroy()
                m_box.showerror("Error", "Errore di conversione da MP4 a MP3") 
    except:
        flag=False
        newWindow.destroy()
        m_box.showerror("Error", "Errore di download") 
    newWindow.destroy()
    if flag: m_box.showinfo("Scaricato", "Ho scaricato tutto")

make_menu(ws)
show = Label(ws, anchor="w",fg ="#f5453c", text = 'Bentornato su "YT Downloader - Scarica le tue canzoni"', font = ("Serif", 14), padx = 0, pady = 10)
show.pack()
    
show = Label(ws, text = "Lista dei link delle canzoni che vuoi scaricare: ",
             font = ("Times", 14), padx = 10, pady = 5)
show.pack() 

lb = Listbox(ws, selectmode = "multiple")
scroll_one=Scrollbar(ws,command=lb.yview)    
lb.configure(yscrollcommand=scroll_one.set)
lb.pack(padx = 20, pady = 0, expand = YES, fill = BOTH) 
scroll_one.pack(side=RIGHT,fill=Y) 

get_info = Label(ws, text="Inserisci il link della canzone che vuoi scaricare: ",
                 font = ("Times", 14), padx = 10, pady = 10)
get_info.pack()

link = StringVar()

yt_link = Entry(ws, width=60, textvariable=link)
yt_link.pack()
yt_link.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

yt_link.focus()
Button(ws, text="Inserisci link", command=threading1).pack()
ws.bind('<Return>',lambda event:threading1())

Button(ws, text="Cancella link", command=delSelected).pack()
ws.bind('<Delete>',lambda event:delSelected())

Button(ws, text="Scarica le canzoni", command=threading, activeforeground ="#f5453c").pack()

ws.mainloop() 






