
from tkinter import *
import multiprocessing
from datetime import datetime
from timeit import default_timer


class Gui:

  
    def __init__(self):

        

        self.all_processes = []  
        self.logsindex = 0  


        self.root = Tk()
        self.root.title("playTog3th3r Server")
        self.root.geometry("500x300")
        self.root.minsize(500, 300)
        self.root.maxsize(500, 300)
        self.root.iconbitmap("images/server_icon.ico")

        self.start = None 
        self.job = None 

        self.acceptedList = []  


        self.portLabel = Label(self.root, text="Port :", background='#1D1C1C', fg="#999999")
        self.portLabel.place(x=20, y=10)

        self.port = Entry(self.root)
        self.port.place(width=100, x=20, y=30)

        self.passwdLabel = Label(self.root, text="Password :", background='#1D1C1C', fg="#999999")
        self.passwdLabel.place(x=20, y=60)

        self.passwd = Entry(self.root)
        self.passwd.place(width=150, x=20, y=80)

        self.choiceLabel = Label(self.root, text="Sharing type :", background='#1D1C1C', fg="#999999")
        self.choiceLabel.place(x=20, y=110)

        self.choiceList = Listbox(self.root)
        self.choiceList.insert(0, "None")
        self.choiceList.insert(1, "Keys")
        self.choiceList.insert(2, "Click")
        self.choiceList.place(height=50, width=40, x=20, y=140)

        self.acceptedLabel = Label(self.root, text="Accepted keys (inline, without spaces) :", background='#1D1C1C',
                                   fg="#999999")
        self.acceptedLabel.place(x=20, y=200)

        self.accepted = Entry(self.root, background='white', fg="black")
        self.accepted.place(width=200, x=20, y=225)


        self.FramePanel = Frame(self.root, borderwidth=0, background="#404040")
        self.FramePanel.pack(side=LEFT)
        self.FramePanel.place(x=300, y=0, width=200, height=300)

        self.statusLabel = Label(self.FramePanel, text="Status :", background='#404040', fg="#999999")
        self.statusLabel.place(x=20, y=10)

        self.status = Label(self.FramePanel, text="Off", background='#404040', fg="red")
        self.status.place(x=20, y=30)

        self.uptimeLabel = Label(self.FramePanel, text="Uptime :", background='#404040', fg="#999999")
        self.uptimeLabel.place(x=20, y=60)

        self.uptime = Label(self.FramePanel, text="0:00:00", background='#404040', fg="#999999")
        self.uptime.place(x=20, y=80)

        self.startButton = Button(self.FramePanel, text="Start server", background='#b3b3b3', fg="black",
                                  command=self.startserv)
        self.startButton.place(x=20, y=110)

        self.stopButton = Button(self.FramePanel, text="Stop server", background='#b3b3b3', fg="black",
                                 command=self.stopserv)
        self.stopButton.place(x=110, y=110)

        self.logsLabel = Label(self.FramePanel, text="Logs :", background='#404040', fg="#999999")
        self.logsLabel.place(x=20, y=150)

        self.logs = Listbox(self.FramePanel, background='#bfbfbf', fg="black")
        self.logs.place(x=20, y=175, width=160, height=110)

        self.root.config(background='#1D1C1C')
        self.root.mainloop()


    def warningwin(self, alert):

        warningwin = Tk()
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

    def stopserv(self):
        

        if self.job is not None: 
            self.root.after_cancel(self.job)  
            self.job = None  
            self.uptime.config(text="0:00:00")

        for proc in range(0, len(self.all_processes)):  
            if self.all_processes[proc][1] == "server": 
                self.all_processes[proc][0].terminate() 
                self.status.config(text="Off", fg="red") 
                self.logs.insert(self.logsindex, self.getClearLog("Server stopped.")) 
                self.logsindex += 1 
                self.all_processes.pop(proc) 
                
    def startserv(self):


        portstr = self.port.get()
        passwdstr = self.passwd.get()

        if self.choiceList.get(ACTIVE) == "Click": 

            process = multiprocessing.Process(target=listening_servClick, args=(int(portstr), passwdstr))
            process.start()
            self.all_processes.append([process, "server"])
            self.start = default_timer() 
            self.updateTime() 

            self.status.config(text="On", fg="green")  
            self.logs.insert(self.logsindex, self.getClearLog("Server started."))  
            self.logsindex += 1 

           
            settings = "Port: " + portstr + " | Password: " + passwdstr + " | Type: " + self.choiceList.get(ACTIVE)
            self.logs.insert(self.logsindex, self.getClearLog(settings))
            self.logsindex += 1

        elif self.choiceList.get(ACTIVE) == "Keys" and self.accepted.get() != "": 

            for k in self.accepted.get():
                self.acceptedList.append(k) 

            process = multiprocessing.Process(target=listening_servKeys, args=(int(portstr), passwdstr, self.acceptedList)) 
            process.start() 
            self.all_processes.append([process, "server"])  

            self.start = default_timer() 
            self.updateTime() 

            self.status.config(text="On", fg="green") 
            self.logs.insert(self.logsindex, self.getClearLog("Server started."))  
            self.logsindex += 1  

            
            settings = "Port: " + portstr + " | Password: " + passwdstr + " | Type: " + self.choiceList.get(ACTIVE)
            self.logs.insert(self.logsindex, self.getClearLog(settings))
            self.logsindex += 1

        elif self.choiceList.get(ACTIVE) == "None": 
            self.warningwin("Please select a sharing type.")

        elif self.choiceList.get(ACTIVE) == "Keys" and self.accepted.get() == "": 
            self.warningwin("Please enter accepted keys.")



import socket
from threading import Thread
import pynput.mouse
from string import digits
import pynput.keyboard

keyboard = pynput.keyboard.Controller()


class listening_servKeys(Thread):


    def __init__(self, p, passwd, keylist):


        Thread.__init__(self)
        self.host = '127.0.0.1'
        self.port = p
        self.password = passwd
        self.keyslist = keylist


        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.clients = []
        self.receive()  

    def handle(self, client):


        while True:

            try: 

                message = client.recv(1024)  
                key = message.decode("utf-8") 
                key = key.replace("'", "")  

                print(key)

                if key in self.keyslist: 
                    keyboard.press(key)
                    keyboard.release(key)

            except: 

                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                print("Client closed the connection.")
                break

    def receive(self):

       

        while True:


            client, address = self.server.accept()  

            lstmess = client.recv(1024) 
            passwd = lstmess.decode().split(":")[0]  
            strlstkeys = lstmess.decode().split(":")[1] 

            templist = []

            for ele in strlstkeys:
                if ele in self.keyslist: 
                    templist.append(ele)

            if passwd == self.password and templist == self.keyslist and len(self.clients) < 1:  

                self.clients.append(client) 

                verif = "Accepted"
                client.send(verif.encode("utf-8")) 

                thread = Thread(target=self.handle, args=(client,)) 
                thread.start()  
                print("Connection accepted.")

            else: 
                verif = "Refused"
                client.send(verif.encode("utf-8"))
                print("Connection refused.")


mouse = pynput.mouse.Controller()


class listening_servClick(Thread):
    

    def __init__(self, p, passwd):
        
        Thread.__init__(self)
        self.host = '127.0.0.1'
        self.port = p
        self.password = passwd

        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.clients = []
        self.receive()  
        
    def handle(self, client):


        while True:

            try: 

                message = client.recv(1024) 
                listmessage = message.decode().split(":")  
                mouv = listmessage[0]  
                x = listmessage[1] 
                y = listmessage[2]  
                x = ''.join(c for c in x if c in digits) 
                y = ''.join(c for c in y if c in digits)  

                x = int(float(x))  
                y = int(float(y)) 
                mouse.position = (x, y)  
                if mouv == "Button.left": 
                    mouse.press(pynput.mouse.Button.left)
                    mouse.release(pynput.mouse.Button.left)
                elif mouv == "Button.right": 
                    mouse.press(pynput.mouseButton.right)
                    mouse.release(pynput.mouse.Button.right)
                print(mouv)

            except:  

                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                print("Client closed the connection.")
                break

    def receive(self):

        

        while True:

            client, address = self.server.accept() 

            passwd = client.recv(1024)  

            if passwd.decode("utf-8") == self.password and len(self.clients) < 1:  

                self.clients.append(client) 

                verif = "Accepted"
                client.send(verif.encode("utf-8")) 

                thread = Thread(target=self.handle, args=(client,))  
                thread.start()  
                print("Connection accepted.")

            else: 
                verif = "Refused"
                client.send(verif.encode("utf-8"))
                print("Connection refused.")


if __name__ == "__main__":
    mainwin = Gui()




