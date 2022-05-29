from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog

import pygame
from mutagen.mp3 import MP3

import time


from Drive import DriveAPI

import Server


class Player:
    def __init__(self):
        self.root = Tk()
        self.root.title("MP3 Player")
        self.root.geometry("500x300")

        pygame.mixer.init()

        self.Uploaded=False
        self.IsPaused=False
        self.SizeOfListBox=0

        self.songbox = Listbox(self.root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
        self.songbox.pack()

        self.BackButtonImg = PhotoImage(file=r"Photos\back50.png")
        self.ForwordButtonImg = PhotoImage(file=r"Photos\forward50.png")
        self.PlayButtonImg = PhotoImage(file=r"Photos\play50.png")
        self.PauseButtonImg = PhotoImage(file=r"Photos\pause50.png")
        self.StopButtonImg = PhotoImage(file=r"Photos\stop50.png")

        self.ControlsFrame = Frame(self.root)
        self.ControlsFrame.pack()

        self.BackButton = Button(self.ControlsFrame, image=self.BackButtonImg, borderwidth=0, command=self.PrevSong)
        self.PauseButton = Button(self.ControlsFrame, image=self.PauseButtonImg, borderwidth=0, command=self.pause)
        self.PlayButton = Button(self.ControlsFrame, image=self.PlayButtonImg, borderwidth=0, command=self.play)
        self.StopButton = Button(self.ControlsFrame, image=self.StopButtonImg, borderwidth=0, command=self.stop)
        self.ForwordButton = Button(self.ControlsFrame, image=self.ForwordButtonImg, borderwidth=0, command=self.NextSong)

        self.BackButton.grid(row=0, column=0, padx=10)
        self.PauseButton.grid(row=0, column=1, padx=10)
        self.PlayButton.grid(row=0, column=2, padx=10)
        self.StopButton.grid(row=0, column=3, padx=10)
        self.ForwordButton.grid(row=0, column=4, padx=10)


        self.MyMenu = Menu(self.root)
        self.root.config(menu=self.MyMenu)

        self.AddSongMenu = Menu(self.MyMenu)
        self.MyMenu.add_cascade(label="Options", menu=self.AddSongMenu)
        self.AddSongMenu.add_command(label="Add Songs To The Playlist", command=self.AddManySong)
        self.AddSongMenu.add_command(label="Delete The Selected Song", command=self.DeleteSong)
        self.AddSongMenu.add_command(label="Clear The List", command=self.DeleteAllSongs)

        self.StatusBar = Label(self.root, text="", bd=1, relief=GROOVE, anchor=E)
        self.StatusBar.pack(fill=X, side=BOTTOM, ipady=2)

        self.Slider= ttk.Scale(self.root, orient = "horizontal", from_=0, to = 1 ,command=self.SlideAdjust,value=0,length=360,state="disable")
        self.Slider.pack(pady=20)

        self.root.mainloop()
        self.SendInfo("Session Finished")
        pygame.mixer.music.stop()
        Server.ShutDown()







    def SendInfo(self,State):
        if(State=="Session Finished" or State=="Paused" or State=="UnPaused" or State=="Stopped" or State=="Uploaded"):
            Server.Share(f"{State}")
        elif (State=="Playing"):
            Server.Share(f"{self.songbox.get(ACTIVE)}//{State}")
        elif (State=="Slided"):
            Server.Share(f"{self.songbox.get(ACTIVE)}//{self.Slider.get()}//{State}")






    def SlideAdjust(self,event):
        self.GotSlided=True
        song = self.songbox.get(ACTIVE)
        song=f"Drive//Songs//{song}"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0,start=int(self.Slider.get()))
        self.SendInfo("Slided")






    def play(self):
        self.GotSlided=False
        song = self.songbox.get(ACTIVE)
        song=f"Drive//Songs//{song}"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.GetPosition()


        self.Slider.config(to=int(self.SongLength),state="enable")

        self.SendInfo("Playing")




    def stop(self):
        self.GotSlided=False
        pygame.mixer.music.stop()
        self.songbox.selection_clear(ACTIVE)
        self.StatusBar.config(text="")
        self.SendInfo("Stopped")


    def NextSong(self):
        self.GotSlided=False
        Current = self.songbox.curselection()
        Next = (Current[0] + 1)%self.SizeOfListBox
        song = self.songbox.get(Next)
        song=f"Drive//Songs//{song}"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.songbox.selection_clear(0, END)
        self.songbox.activate(Next)
        self.songbox.select_set(Next, last=None)
        self.SendInfo("Playing")



    def PrevSong(self):
        self.GotSlided=False
        Current = self.songbox.curselection()
        prev = (Current[0] - 1)%self.SizeOfListBox
        song = self.songbox.get(prev)
        song=f"Drive//Songs//{song}"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.songbox.selection_clear(0, END)
        self.songbox.activate(prev)
        self.songbox.select_set(prev, last=None)
        self.SendInfo("Playing")



    def GetPosition(self):
        self.CurrentTime = pygame.mixer.music.get_pos()/1000

        if self.GotSlided and self.IsPaused:
            self.CurrentTime=self.Slider.get()
        elif self.GotSlided:
            self.CurrentTime=self.Slider.get()
            self.CurrentTime+=1


        ConvertedCurrenTime=time.strftime("%M:%S",time.gmtime(self.CurrentTime))


        song=self.songbox.get(ACTIVE)
        song = f"Drive//Songs//{song}"
        SongMut=MP3(song)
        self.SongLength=SongMut.info.length
        ConvertedSongLength = time.strftime("%M:%S", time.gmtime(self.SongLength))

        if int(self.SongLength)==int(self.CurrentTime):
            self.NextSong()



        self.StatusBar.config(text=f"Time Elapsed: {ConvertedCurrenTime} of {ConvertedSongLength}")

        self.Slider.config(value=int(self.CurrentTime),to=int(self.SongLength))



        self.StatusBar.after(1000,self.GetPosition)




    def AddManySong(self):
        songs=filedialog.askopenfilenames(title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
        for song in songs:
            song=song.split("/")[-1]
            DriveAPI.SendToDrive(song)


            self.songbox.insert(END,song)
        self.SizeOfListBox=self.songbox.size()
        self.Uploaded = False
        self.SendInfo("Uploaded")

    def DeleteSong(self):
        self.songbox.delete(ANCHOR)
        self.SizeOfListBox =-1
        pygame.mixer.music.stop()

    def DeleteAllSongs(self):
        self.songbox.delete(0,END)
        self.SizeOfListBox = 0
        pygame.mixer.music.stop()

    def pause(self):
        if (self.IsPaused):
            pygame.mixer.music.unpause()
            self.IsPaused = False
            self.SendInfo("UnPaused")


        else:
            pygame.mixer.music.pause()
            self.IsPaused = True
            self.SendInfo("Paused")


run=Player()

