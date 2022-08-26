
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
import threading
import select
import qrcode
from zipfile import ZipFile
import os
import time
t=None
global l
e=""
hh="jjj"
from shutil import make_archive
import multiprocessing
from kivy.clock import Clock
s=None
from kivy.uix.popup import Popup
import socket 
Window.size=(360,690)
l=[]
#Window.clearcolor=(1,1,1,1)

class threadin(threading.Thread):
      
      def __init__(self,interval=1):
            self.interval=interval
            thread=threading.Thread(target=self.run)
            thread.daemon=True
            thread.start()
            '''thread1=threading.Thread(target=self.run1)
            thread1.daemon=True
            thread1.start()'''
      def run(self):
            global conn
            global s
            h=socket.gethostname()
            f=socket.gethostbyname(h)
            print(f)
           #print(f)
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            e=(f,"8080")
            SEP="%%"
            s.bind((f,8080))
            SEPERATOR="<SEPERATOR>"
            s.listen(1)
            print(":hfh")
            global t
            try:
             conn,address=s.accept()
            except:
             pass
            #print(conn)
            if  conn :
                  print(conn)
                  t=conn
                   

          
threadin()


      



class MyWidget(BoxLayout):
    
   

      def __init__(self,**kwargs):
        super(MyWidget,self).__init__(**kwargs)
        superbox=BoxLayout(orientation="horizontal",spacing=5,padding=(12,12))
        mybut=Button(text="send",size_hint=(40,0.5),on_press=self.send1)
        mybut1=Button(text="recive",size_hint=(40,0.5),on_press=self.run)
        #mybut2=Button(text="qr",size_hint=(40,0.5),on_press=self.qr)
        mybut3=Button(text="scan",size_hint=(40,0.5),on_press=self.cam)
        #superbox.add_widget(mybut2)                
        superbox.add_widget(mybut)
        superbox.add_widget(mybut1)
        superbox.add_widget(mybut3)
        MyWidget.add_widget(self,superbox)
        

      def selected(self,file):
      
       global l
       l=l+[file]
 
     
      def conn(self,file):
            h=socket.gethostname()
            f=socket.gethostbyname(h)
            print(f)
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            e=(f,"8080")
            s.bind((f,8080))
            s.listen(1)
            conn,address=s.accept  ()
            if conn:
               layout=GridLayout(cols=1,padding=10)
               close=Button("connection has been established")
               layout.add_widget(close)
               popup=Popup(title="scan",content=layout,size_hint=(None,None),size=(500,500))
               popup.open()
                        
 
     
      def qr(self,obj):
        h=socket.gethostname()
        d=socket.gethostbyname(h)
        qr=qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(d)
        qr.make(fit=True)
        img=qr.make_image(fill="black",back_color="white")
        img.save("#$$#.png")
        layout=GridLayout(cols=1,padding=10)
        popup=Image(source="#$$#.png")
        close=Button(text="close",size_hint=(0.1,0.1))
        layout.add_widget(popup)
        #layout.add_widget(close)
        popup=Popup(title="scan",content=layout,size_hint=(None,None),size=(500,500))
        
        popup.open()
        close.bind(on_press=popup.dismiss)
        os.remove("#$$#.png")
        
           


      def send1(self,obj):
         global hh
         global t
         SEP="%%%"
         SEPERATOR="<SEPERATOR>"
         if t:
            hh="jj"
      
            if l!=[]:
               j=l[len(l)-1]
               print(j)
               
               #e=j[1:]
               #print(e)
               for i in j:
                   print(i)
                   #print(e)
                   a=i
                   if os.path.isdir(a):
                              n=os.path.basename(i)
                              c=os.path.abspath(make_archive(i,"zip",a))
                              SEP="^.$&.^"
                              
                              filesize=os.path.getsize(c)
                              ''' print("a")
                              filepath_lis=[]
                              print(os.walk(n))
                              for root,directories,files in os.walk(n):
                                 
                                 for filename in files:
                                    filepath=os.path.join(root,filename)
                                    filepath_lis.append(filepath)

                              with ZipFile(n+".zip",'w') as zipe:
                                          for file in filepath_lis:
                                                     print(file)
                                                     print("writing into file")
                                                     zipe.write(os.path.basename(file))
                              zipe.close()
                              filesize=str(os.path.getsize(n+".zip"))
                              print(filesize)'''
                   if SEP=="^.$&.^":
                              n=os.path.basename(i)
                              n=n+".zip"
                              g=open(c,"rb")
                              e=f"{n}{SEPERATOR}{SEP}{SEPERATOR}{filesize}"
                              print(e)
                              t.sendall(str(len(e)).encode())
                              t.sendall(e.encode())
                              
                   else:
                     filesize=str(os.path.getsize(a))
                     g=open(a,"rb")
                     n=os.path.basename(a)
                     print(filesize)
                     e=f"{n}{SEPERATOR}{SEP}{SEPERATOR}{filesize}"
                     t.sendall(str(len(e)).encode())
                     t.sendall(e.encode())
                   
                   while True:
                        k=g.read()
                        if not k:
                              break
                        else:
                           t.sendall(k)
                           print("n")
                  
                   
                 
                   g.close()
                   print("succesfully send")
                   if SEP=="^.$&.^":
                         os.remove(c)
                         
                        
            elif l==[]:
                  n="empty"
                  filesize=0
                  t.send(b"{n}{SEPERATOR}{SEP}{SEPERATOR}{filesize}")
                  
          
         else:
           self.qr(obj)
           ''' layout=GridLayout(cols=1,padding=10)
            close=Button(text="close",size_hint=(0.1,0.1))
            pop=Label(text="Connection was not established\n\Scan the qr code and after that select files and click send")
            layout.add_widget(pop)
            layout.add_widget(close)
            popup=Popup(title="scan",content=layout,size_hint=(None,None),size=(500,500))
            popup.open()
            close.bind(on_press=popup.dismiss)'''
        

          

      def cam(self,obj):
             global e
             e="192.168.1.8"
             global s
             s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
             s.connect((e,8080))
             if s:
                return True

      


      def run(self,obj):
            print(s)
            SEPERATOR="<SEPERATOR>"
            s.settimeout(10)
            q=s.recv(2).decode()
            print(q)
            recived=s.recv(int(q)).decode()
            print(recived)
            name,sep,filesize=recived.split(SEPERATOR)
            print(name,filesize,sep)
            try:
              os.mkdir("downloads")#creates a folder dowmloads :
            except:
                pass
            path=r"C:\Users\user\Desktop\VShare\downloads"
            complete=os.path.join(path,name)
            a=open(complete,"wb+")
            c=0
            while c<=int(filesize):
                       read=s.recv(1024)
                       if not read:
                            break
                       else:
                           a.write(read)
                       c+=1024
            a.close()
            if sep=="^.$&.^":
                  print("hceck")
                  
                  with ZipFile(complete,"r") as  z:
                        e=name.rsplit(".",1)
                        f=os.path.join(path,e[0])
                        os.mkdir(e[0])
                        z.extractall(f)
                        print("finished ext")
                  os.remove(complete)
                  
      
           
            print("completed")
                  
      

      def recive(self,obj):
            e=self.cam(obj)
            if e==0:
                  self.kiti(obj)
         





                 
      
                
               
                
    
               

            
      
        
     
    
        

class FileChooserWindow(App):
    def build(self):
        
        return MyWidget()
        
window=FileChooserWindow()
window.run()
