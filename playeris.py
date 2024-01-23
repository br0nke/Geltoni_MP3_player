from pygame import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import time
from threading import *

playlist = []
wasstarted = False
volume = 0.3
totallength = 0
quitthreading = False
slider_moved = False
playing = False

mixer.init()
player = mixer.music

class Music:
    def __init__(self, file):
        self.file = file
        name = file.split("/")
        self.name = name[-1]


def AddToList(musicobj):
    listsize = music_list.size() + 1
    music_list.insert(listsize, musicobj.name)
    playlist.append(musicobj)


def OpenFile():
    try:
        filename = filedialog.askopenfilenames(initialdir="/",
                                               title="Select a File",
                                               filetypes=(('MP3 Files', '*.mp3'), ('M3U Files', '*.m3u')
                                                          ))
        if (filename == ""):
            return
        for files in filename:
            music = Music(files)
            AddToList(music)
    except:
        print("OpenFile error.")


def Play():
    global wasstarted
    global player
    global playing
    if (wasstarted == False):
        selected_music = music_list.curselection()
        try:
            selected_music = selected_music[0]
        except:
            messagebox.showwarning(
                "Music", "Choose a song from the list!")

        player.load(playlist[selected_music].file)
        player.play()
        player.set_volume(volume)
        UpdateTime()
        pause_button.place(x=200, y=500)
        wasstarted = True
        UpdateTime()
    else:
        playing = True
        player.unpause()
        play_button.place_forget()
        pause_button.place(x=200, y=500)


def Pause():
    global playing
    playing = False
    player.pause()
    pause_button.place_forget()
    play_button.place(x=200, y=500)


def Stop():
    global wasstarted
    global playing
    if wasstarted == True:
        pause_button.place_forget()
        play_button.place(x=200, y=500)
        wasstarted = False
        player.stop()
        playing = False


def Soundd():
    soundpanel = Toplevel()
    soundpanel.geometry("200x50")
    soundpanel.resizable(False, False)
    soundslider = Scale(soundpanel, from_=0, to=100,
                        orient=HORIZONTAL, command=SoundChanger, length=200)
    soundslider.pack()
    soundslider.set(volume * 100)


def SoundChanger(self):
    global volume
    global novolume_button
    global lowvolume_button
    global highvolume_button
    volume = int(self) / 100
    player.set_volume(volume)
    if int(self) == 0:
        novolume_button.place(x=400, y=500)
        lowvolume_button.place_forget()
        highvolume_button.place_forget()
    if int(self) > 0 and int(self) < 60:
        novolume_button.place_forget()
        highvolume_button.place_forget()
        lowvolume_button.place(x=400, y=500)
    if int(self) > 60:
        novolume_button.place_forget()
        highvolume_button.place(x=400, y=500)
        lowvolume_button.place_forget()


def Forward():
    try:
        for i in music_list.curselection():
            nextmusic = i + 1
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()
    except:
        nextmusic = 0
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()


def Back():
    try:
        for i in music_list.curselection():
            nextmusic = i - 1
            if (nextmusic < 0):
                nextmusic = music_list.size() - 1
                music_list.selection_clear(0, END)
                music_list.activate(nextmusic)
                music_list.selection_set(nextmusic)
                player.load(playlist[nextmusic].file)
                player.play()
                UpdateTime()
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()
    except:
        nextmusic = music_list.size() - 1
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()


def PlaySelected(self):
    global wasstarted
    global player
    selected_music = music_list.curselection()
    selected_music = selected_music[0]
    player.load(playlist[selected_music].file)
    player.play()
    player.set_volume(volume)
    pause_button.place(x=200, y=500)
    wasstarted = True

    UpdateTime()


def UpdateTime():
    global player
    global totallength
    global playing
    selected_music = music_list.curselection()
    selected_music = selected_music[0]
    total_length = mixer.Sound.get_length(
        mixer.Sound(playlist[selected_music].file))

    conv_total_length = time.strftime('%M:%S', time.gmtime(total_length))
    end_song_time.config(text=conv_total_length)
    slider.config(to=int(total_length))
    pos.set(0)
    playing = True
    if update.is_alive() == False:
        update.start()


def UpdateSlider():
    global player
    global totallength
    while True:
        if playing == True:
            if slider_moved == True:
                pos.set(slider.get() + 1)
                conv_total_length = time.strftime(
                    '%M:%S', time.gmtime(int(slider.get())))
                current_song_time.config(text=conv_total_length)
            else:
                current_time = player.get_pos() / 1000
                conv_total_length = time.strftime(
                    '%M:%S', time.gmtime(current_time))
                current_song_time.config(text=conv_total_length)
                pos.set(int(current_time))
            slider.config(variable=pos)
            time.sleep(1)
            if quitthreading == True:
                break


def FastForward(self):
    global slider_moved
    pos.set(self)
    player.play(start=int(self))
    slider_moved = True


def CloseWindow():
    global quitthreading
    quitthreading = True
    player.stop()
    master.destroy()


master = Tk()
master.title("Mp3 Player")
master.protocol("WM_DELETE_WINDOW", CloseWindow)
master.geometry("500x600")
master.resizable(False, False)
update = Thread(target=UpdateSlider)
pos = IntVar()

back_img = PhotoImage(file="backpic.PNG")
back_button = Button(master, image=back_img, command=Back)
play_img = PhotoImage(file="playpic.PNG")
play_button = Button(master, image=play_img, command=Play)
pause_img = PhotoImage(file="pausepic.PNG")
pause_button = Button(master, image=pause_img, command=Pause)
stop_img = PhotoImage(file="stoppic.PNG")
stop_button = Button(master, image=stop_img, command=Stop)
forward_img = PhotoImage(file="forwardpic.PNG")
forward_button = Button(master, image=forward_img, command=Forward)
add_img = PhotoImage(file="addmusicpic.PNG")
add_button = Button(master, image=add_img, command=OpenFile)
novolume_img = PhotoImage(file="novolumepic.PNG")
novolume_button = Button(master, image=novolume_img, command=Soundd)
lowvolume_img = PhotoImage(file="lowvolumepic.PNG")
lowvolume_button = Button(master, image=lowvolume_img, command=Soundd)
highvolume_img = PhotoImage(file="highvolumepic.PNG")
highvolume_button = Button(master, image=highvolume_img, command=Soundd)
current_song_time = Label(master, text="00:00")
end_song_time = Label(master, text="00:00")
slider = Scale(master, from_=0, to=100, orient=HORIZONTAL,
               command=FastForward, showvalue=False, length=315, variable=pos)


music_list = Listbox(master, font=("davish"), width=53,
                     height=11, selectmode=SINGLE)

music_list.place(x=10, y=10)
add_button.place(x=10, y=250)
back_button.place(x=100, y=500)
play_button.place(x=200, y=500)
stop_button.place(x=20, y=500)
forward_button.place(x=270, y=500)
lowvolume_button.place(x=400, y=500)
current_song_time.place(x=50, y=400)
end_song_time.place(x=410, y=400)
slider.place(x=85, y=400)

music_list.bind("<<ListboxSelect>>", PlaySelected)
mainloop()