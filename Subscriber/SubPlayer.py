import pygame

from Drive import DriveAPI

class Sub:
    def __init__(self):
        pygame.mixer.init()

    def ActionToBeTaken(self,Message):
        state=Message.split("//")[-1]
        Song = Message.split("//")[0]

        if (state=="Session Finished"):
            self.Stop()
            print("Thanks for listening\nBye :)")

        elif (state=="Stopped"):
            self.Stop()

        elif ((state=="Playing")):
            self.Play(Song)

        elif (state=="Paused"):
            self.Pause()

        elif (state=="UnPaused"):
            self.UnPause()

        elif(state=="Uploaded"):
            self.GetFromDrive()

        elif (state=="Slided"):
            time=float(Message.split("//")[1])
            self.Play(Song,int(time))




    def Play(self,Song,time=0):
        Song=f"Drive//Songs//{Song}"
        pygame.mixer.music.load(Song)
        pygame.mixer.music.play(loops=0,start=time)


    def Stop(self):
        pygame.mixer.music.stop()

    def Pause(self):
        pygame.mixer.music.pause()

    def UnPause(self):
        pygame.mixer.music.unpause()

    def GetFromDrive(self):
        DriveAPI.Download()








