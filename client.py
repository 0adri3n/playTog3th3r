from tkinter import *
import multiprocessing
from datetime import datetime
from timeit import default_timer
import socket
import pynput.keyboard
import pynput.mouse

class Gui:


    def __init__(self):


        self.all_processes = []  
        self.logsindex = 0 

        
        self.root = Tk()
        self.root.title("playTog3th3r Client")
        self.root.geometry("500x300")
        self.root.minsize(500, 300)
        self.root.maxsize(500, 300)
        self.root.iconbitmap("images/client.ico")

        self.start = None  
        self.job = None 

        self.keysList = []  

        self.client = None 


        self.ïpLabel = Label(self.root, text="IP :", background='#1D1C1C', fg="#999999")
        self.ïpLabel.place(x=20, y=10)

        self.ip = Entry(self.root)
        self.ip.place(width=100, x=20, y=30)

        self.portLabel = Label(self.root, text="Port :", background='#1D1C1C', fg="#999999")
        self.portLabel.place(x=20, y=60)

        self.port = Entry(self.root)
        self.port.place(width=100, x=20, y=80)

        self.passwdLabel = Label(self.root, text="Password :", background='#1D1C1C', fg="#999999")
        self.passwdLabel.place(x=20, y=110)

        self.passwd = Entry(self.root)
        self.passwd.place(width=150, x=20, y=130)

        self.choiceLabel = Label(self.root, text="Sharing type :", background='#1D1C1C', fg="#999999")
        self.choiceLabel.place(x=20, y=160)

        self.choiceList = Listbox(self.root)
        self.choiceList.insert(0, "None")
        self.choiceList.insert(1, "Keys")
        self.choiceList.insert(2, "Click")
        self.choiceList.place(height=50, width=40, x=20, y=185)

        self.keysLabel = Label(self.root, text="Keys(inline, without spaces and accepted by server) :", background='#1D1C1C', fg="#999999")
        self.keysLabel.place(x=18, y=240)

        self.keys = Entry(self.root, background='white', fg="black")
        self.keys.place(width=200, x=20, y=265)


        self.FramePanel = Frame(self.root, borderwidth=0, background="#404040")
        self.FramePanel.pack(side=LEFT)
        self.FramePanel.place(x=300, y=0, width=200, height=300)

        self.statusLabel = Label(self.FramePanel, text="Status :", background='#404040', fg="#999999")
        self.statusLabel.place(x=20, y=10)

        self.status = Label(self.FramePanel, text="Not connected", background='#404040', fg="red")
        self.status.place(x=20, y=30)

        self.uptimeLabel = Label(self.FramePanel, text="Uptime :", background='#404040', fg="#999999")
        self.uptimeLabel.place(x=20, y=60)

        self.uptime = Label(self.FramePanel, text="0:00:00", background='#404040', fg="#999999")
        self.uptime.place(x=20, y=80)

        self.startButton = Button(self.FramePanel, text="Connect", background='#b3b3b3', fg="black", command=self.connect)
        self.startButton.place(x=20, y=110)

        self.stopButton = Button(self.FramePanel, text="Stop connection", background='#b3b3b3', fg="black", command=self.stopconnect)
        self.stopButton.place(x=90, y=110)

        self.logsLabel = Label(self.FramePanel, text="Logs :", background='#404040', fg="#999999")
        self.logsLabel.place(x=20, y=150)

        self.logs = Listbox(self.FramePanel, background='#bfbfbf', fg="black")
        self.logs.place(x=20, y=175, width=160, height=110)

        self.root.config(background='#1D1C1C')
        self.root.mainloop()


    def warningwin(self, alert):

       
        warningwin=Tk()
        warningwin.title("Warning !")
        warningwin.geometry("200x35")
        warningwin.minsize(200, 35)
        warningwin.maxsize(200, 35)
        warningwin.iconbitmap("images/exclamationmark.ico")
        warningwin.config(background='#1D1C1C')

        warninglabel = Label(warningwin, text=alert, background='#1D1C1C', fg="#FBF6F6")
        warninglabel.pack(anchor=CENTER)
        warninglabel.place(width=200, height=35)

        warningwin.mainloop()

    def getClearLog(self, str):

       

        now = datetime.now() 
        current_time = now.strftime("%H:%M:%S")
        newlog = "[" + current_time + "] " + str  
        return newlog

    def updateTime(self):


        now = default_timer() - self.start  
        minutes, seconds = divmod(now, 60) 
        hours, minutes = divmod(minutes, 60)
        str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
        self.uptime.config(text=str_time) 
        self.job = self.root.after(1000, self.updateTime)


    def stopconnect(self):


        if self.job is not None: 
            self.root.after_cancel(self.job)
            self.job = None 
            self.uptime.config(text = "0:00:00") 


        for proc in range(0, len(self.all_processes)): 
            if self.all_processes[proc][1] == "listener":  
                self.all_processes[proc][0].terminate()  
                self.status.config(text="Not connected", fg="red") 
                self.logs.insert(self.logsindex, self.getClearLog("Connection stopped.")) 
                self.logsindex += 1  
                self.all_processes.pop(proc)  


    def connect(self):

        portstr = self.port.get()
        passwdstr = self.passwd.get()
        ipstr = self.ip.get()

        for k in self.keys.get():
            self.keysList.append(k)  

        if self.choiceList.get(ACTIVE) == "Click":  

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.client.connect((ipstr, int(portstr))) 
            message = passwdstr
            self.client.send(message.encode('utf-8'))  

            status = self.client.recv(1024)  

            if status.decode("utf-8") == "Accepted":  

                process = multiprocessing.Process(target=writeClick, args=(self.client,)) 
                process.start() 
                self.all_processes.append([process, "listener"]) 

                self.start = default_timer()  
                self.updateTime()  

                self.status.config(text="Connected", fg="green") 
                self.logs.insert(self.logsindex, self.getClearLog("Connection established."))  
                self.logsindex += 1  

                
                settings = "IP: " + ipstr + " | Port: " + portstr + " | Password: " + passwdstr + " | Type: " + self.choiceList.get(ACTIVE)
                self.logs.insert(self.logsindex, self.getClearLog(settings))
                self.logsindex += 1

            elif status.decode("utf-8") == "Refused": 
                self.status.config(text="Connection refused", fg="orange") 

        elif self.choiceList.get(ACTIVE) == "Keys" and self.keysList != "": 

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.client.connect((ipstr, int(portstr))) 
            data = str(self.keysList) 
            message = passwdstr + ":" + data 
            self.client.send(message.encode('utf-8'))

            status = self.client.recv(1024)  

            if status.decode("utf-8") == "Accepted":  

                process = multiprocessing.Process(target=writeKeys, args=(self.client,))  
                process.start() 
                self.all_processes.append([process, "listener"])  

                self.start = default_timer()
                self.updateTime() 

                self.status.config(text="Connected", fg="green") 
                self.logs.insert(self.logsindex, self.getClearLog("Connection established."))  
                self.logsindex += 1  

                settings = "IP: " + ipstr + " | Port: " + portstr + " | Password: " + passwdstr + " | Type: " + self.choiceList.get(ACTIVE)
                self.logs.insert(self.logsindex, self.getClearLog(settings))
                self.logsindex += 1


            elif status.decode("utf-8") == "Refused": 
                self.status.config(text="Connection refused", fg="orange") 

        elif self.choiceList.get(ACTIVE) == "None": 
            self.warningwin("Please select a sharing type.")

        elif self.choiceList.get(ACTIVE) == "Keys" and self.keysList == "":
            self.warningwin("Please enter keys.")



def on_press(key, client):


    print('{0} pressed'.format(key))
    client.send(str(key).encode("utf-8"))  

def writeKeys(client):


    while True:
       
        with pynput.keyboard.Listener(on_press=lambda event: on_press(event, client=client)) as listener:
            listener.join() 
def on_click(x, y, button, pressed):

    global client0  

    print(button)
    message = str(button) + ":" + str(x) + ":" + str(y)  
    client0.send(message.encode("utf-8"))  

def writeClick(client):

    global client0

    client0 = client 

    while True:
        
        with pynput.mouse.Listener(on_click=on_click) as listener:
            listener.join()


if __name__ == "__main__": 
    mainwin = Gui()