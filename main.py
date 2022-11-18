from tkinter import *
from tkinter.font import BOLD, ITALIC
from turtle import fillcolor, width
import pygame
from pygame import mixer
from tkinter import ttk
from PIL import Image
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

print(resource_path)

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)
    
root=Tk()
root.title("Dizik")
root.resizable(False,False)
root.geometry("600x400")
root.iconbitmap(r"C:\dizik\res\icon.ico")
root.tk.call("source", r"C:\dizik\Azure-ttk-theme-main\azure.tcl")
root.tk.call("set_theme", "light")
mixer.init()

is_light=True
is_playing=False
is_paused=False
currentsong=''
track=StringVar(value="No song selected")

def thmchng():
    global is_light
    if is_light:
        themebtn.config(image=on)
        root.tk.call("set_theme", "dark")
        is_light=False
    else:
        themebtn.config(image=off)
        root.tk.call("set_theme", "light")
        is_light=True

on=PhotoImage(file=r"C:\dizik\res\on.png")
off=PhotoImage(file=r"C:\dizik\res\off.png")

themebtn=Button(root,image=off,bd=0,command=thmchng)
themebtn.place(x=550, y=0)

def add_music():
    os.chdir(r"C:\dizik\song")
    songs=os.listdir()
    print(songs)
    for song in songs:
        playlist.insert(END,song[:-4])

def play_music():
    global track
    global currentsong
    global is_playing
    if is_paused==True:
        if playlist.get(ACTIVE)==currentsong:
            mixer.music.unpause()
            playbtn.config(image=pausephoto, command=pause_music)
        else:
            global is_playing
            track.set(playlist.get(ACTIVE))
            is_playing=True
            playbtn.config(image=pausephoto, command=pause_music)
            currentsong= playlist.get(ACTIVE)
            print(currentsong)
            mixer.music.load(currentsong+".mp3")
            mixer.music.play()

    else:
        track.set(playlist.get(ACTIVE))
        playlist.select_set(ACTIVE)
        is_playing=True
        playbtn.config(image=pausephoto, command=pause_music)
        currentsong= playlist.get(ACTIVE)
        print(currentsong)
        mixer.music.load(currentsong+".mp3")
        mixer.music.play()

def pause_music():
    global is_paused
    global currentsong
    print(currentsong)
    is_paused=True
    mixer.music.pause()
    playbtn.config(image=playphoto, command=play_music)


def stop_music():
    mixer.music.stop()


def volupdown(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)
    if btnscale.get()==0:
        volbtn.config(image=voldownphoto)
    else:
        volbtn.config(image=volupphoto)

def onvolbtnclick():
    mixer.music.set_volume(0)
    volbtn.config(image=voldownphoto, command=againvolbtnclick)

def againvolbtnclick():
    volume = btnscale.get()
    mixer.music.set_volume(volume)
    btnscale.set(volume)
    volbtn.config(image=volupphoto, command=onvolbtnclick)

def next_song():
    global currentsong
    global is_playing
    is_playing=True
    playbtn.config(image=pausephoto, command=pause_music)
    nextindex=playlist.index(ACTIVE)+1
    lastindex=playlist.index("end")
    if nextindex>=lastindex:
        currentsong=playlist.get(0)
        playlist.select_clear(0,END)
        playlist.selection_set(0)
        playlist.see(0)
        playlist.activate(0)
        playlist.selection_anchor(0) 
        mixer.music.load(currentsong+".mp3")
        track.set(playlist.get(ACTIVE))
        mixer.music.play()
    else:
        currentsong=playlist.get(nextindex)
        playlist.select_clear(0,END)
        playlist.selection_set(nextindex)
        playlist.see(nextindex)
        playlist.activate(nextindex)
        playlist.selection_anchor(nextindex)
        mixer.music.load(currentsong+".mp3")
        track.set(playlist.get(ACTIVE))
        mixer.music.play()

def prev_song():
    global currentsong
    global is_playing
    is_playing=True
    playbtn.config(image=pausephoto, command=pause_music)
    nextindex=playlist.index(ACTIVE)-1
    if nextindex==-1:
        currentsong=playlist.get("end")
        playlist.select_clear(0,END)
        playlist.selection_set(END)
        playlist.see(END)
        playlist.activate(END)
        playlist.selection_anchor(END)
        mixer.music.load(currentsong+".mp3")
        track.set(playlist.get(ACTIVE))
        mixer.music.play()
    else:
        currentsong=playlist.get(nextindex)
        playlist.select_clear(0,END)
        playlist.selection_set(nextindex)
        playlist.see(nextindex)
        playlist.activate(nextindex)
        playlist.selection_anchor(nextindex)
        mixer.music.load(currentsong+".mp3")
        track.set(playlist.get(ACTIVE))
        mixer.music.play()

label1=Label(root, text="Dizik Playlist", font=('Calibri', 15, BOLD))
label1.place(x=10, y=10)
label2=Label(root, text="Made by BitBitDev(Sanu Kumar)", font=("Calibri", 10, ITALIC))
label2.place(x=120,y=17)

separator = ttk.Separator(root, orient='horizontal')
separator.place(relx=0, rely=0.78, relwidth=1,)

cdphoto=PhotoImage(file=r"C:\dizik\res\music-disc.png")
imglbl=Label(root, image=cdphoto)
imglbl.place(x=10, y=320)

currentsonglabel=Label(root, textvariable=track, bd=0)
currentsonglabel.place(x=75,y=345)
    
playphoto=PhotoImage(file=r"C:\dizik\res\play.png")
pausephoto=PhotoImage(file=r"C:\dizik\res\pause.png")
playbtn=Button(root, image=playphoto, command=play_music,bd=0)
playbtn.place(x=260, y=320)

nextphoto=PhotoImage(file=r"C:\dizik\res\next.png")
prevphoto=PhotoImage(file=r"C:\dizik\res\previous.png")
nextbtn=Button(root, image=nextphoto, command=next_song,bd=0)
nextbtn.place(x=320, y=320)
prevbtn=Button(root, image=prevphoto, command=prev_song,bd=0)
prevbtn.place(x=200, y=320)


volupphoto=PhotoImage(file=r"C:\dizik\res\vol.png")
voldownphoto=PhotoImage(file=r"C:\dizik\res\mute.png")
volbtn=Button(root, image=volupphoto,bd=0, command=onvolbtnclick)
volbtn.place(x=441, y=335)

btnscale=ttk.Scale(root, from_=0, to_=100, orient=HORIZONTAL, command=volupdown)
btnscale.set(80)
mixer.music.set_volume(0.8)
btnscale.place(x=470,y=342)

def on_closing():
    stop_music()
    root.destroy

playlist=Listbox(root, height=10,bd=1,selectmode=SINGLE,relief=FLAT, highlightthickness=0)
playlist.place(x=13, y=40)

add_music()
    
root.protocol("WM_WINDOW_DELETE",on_closing)
root.mainloop()