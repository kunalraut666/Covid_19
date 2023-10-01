import plyer
import requests
import bs4
import tkinter as tk 
import time 
import datetime
import re
import threading
import webbrowser
import geocoder
from geopy.geocoders import Nominatim
from itertools import islice

def getWebData(url):
    data = requests.get(url)
    return data

def getCoronaData():
    url = 'https://www.mohfw.gov.in/'
    htmldata = getWebData(url)
    
    bs = bs4.BeautifulSoup(htmldata.text,'html.parser')
    
    info1 = bs.find('div',class_='col-xs-8 site-stats-count').get_text()
    info2 = bs.find('div',class_='fullbol').get_text()
    
    res1 = re.findall(r'\w+',info1)
    
    r1 = []
    r2 = info2.split()
    
    for i in res1:
        if i not in r1:
            r1.append(i)

    return f'{r1[0]} : {r1[1]}\n{r1[2]} : {r1[3]}\n{r1[4]} : {r1[5]}\n{r2[0]} {r2[1]} : {r2[3]}'

def AllStateData():
    datalst = []
    splitlen = []
    
    for _ in range(36):
        splitlen.append(6)

    data = getWebData('https://prsindia.org/covid-19/cases')
    bs = bs4.BeautifulSoup(data.text,'html.parser')
    
    for info in bs.find('table',class_='table table-striped table-bordered').find_all('td'):
        datalst.append(info.get_text())

    datalst.remove('\xa0')
    del datalst[0:5]

    Inputt = iter(datalst)
    Output = [list(islice(Inputt, elem)) for elem in splitlen]
    
    return Output

def MyStateData():
    g = geocoder.ip('me')
    geolocator = Nominatim(user_agent="geoapiExercises")
    
    location = geolocator.reverse(str(g.latlng[0])+","+str(g.latlng[1]))
    
    address = location.raw['address']
    mystate = address['state']
    
    alldata = AllStateData()
    
    for i in range(36):
        val = alldata[i][1]
        if val == mystate:
            return f'Your State: {alldata[i][1]}\nActive Cases: {alldata[i][3]}\nDischarged: {alldata[i][4]}\nDeath: {alldata[i][5]}'

def notifyMe():
    d = MyStateData()
    while True:
        plyer.notification.notify(title='Corona Updates',message=d,timeout=10,app_icon='covid-19.ico')
        time.sleep(60)

def refreshButton():
    newdata = getCoronaData()
    print('Refreshing.....')
    label['text'] = newdata

def viewSource():
    webbrowser.open('https://www.mohfw.gov.in/')
    webbrowser.open('https://prsindia.org/covid-19/cases')

def perticularState(state):
    alldata = AllStateData()
    for i in range(36):
        val = alldata[i][1]
        if val == state:
            return f'{state}\n\nConfirmed Cases: {alldata[i][2]}\nActive Cases: {alldata[i][3]}\nDischarged: {alldata[i][4]}\nDeath: {alldata[i][5]}'


def searchbyState():
    root = tk.Toplevel()
    root.geometry('500x500')
    root.resizable(False,False)
    stateName = tk.StringVar()
    root.title("Search State Wise")
    root.iconbitmap('searchicon.ico')
    bkimg = tk.PhotoImage(file='logo.png')
    bkimg = bkimg.subsample(2,2)

    def submit():
        s = stateName.get()
        stwin = tk.Toplevel()
        stwin.resizable(False,False)
        stwin.geometry('755x424')
        stwin.title(f'{s} Details for Covid-19')
        
        stwin.iconbitmap('sticon.ico')
        
        stdata = perticularState(s)
        
        docbg = tk.PhotoImage(file='docbg.png')

        stlabel = tk.Label(stwin,fg='white',text=stdata,font=('Times New Roman',40,'bold',"italic"),compound=tk.CENTER,justify=tk.CENTER,image=docbg)
        stlabel.photo = docbg
        stlabel.pack() 

    label_0 = tk.Label(root,image=bkimg)
    label_0.pack(side='top')
    
    label_1 = tk.Label(root,fg='red',text="Get Corona details State Wise",font=('Times New Roman', 20,'bold'))
    label_1.place(x=80,y=83)


    label_2 = tk.Label(root, text="Enter State Name",font=('Times New Roman', 15))
    label_2.place(x=80,y=170)

    
    entry = tk.Entry(root,textvariable=stateName)
    entry.place(x=240,y=173)
    
    
    tk.Button(root, text='Search',width=10,bg='brown',fg='white',command=submit,font=(10),cursor="hand2").place(x=200,y=300)
    root.mainloop() 
    

win = tk.Tk()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
# win.geometry('1920x1080')
win.geometry(f'{screen_width}x{screen_height}')
win.title('Covid-19 News Tracker INDIA')
win.iconbitmap('mask.ico')

f = ('Times New Roman', 40,'bold')
fbn = ('Times New Roman', 15,'bold')
IndFlag = tk.PhotoImage(file='IndianFlag.png')
poster = tk.PhotoImage(file='poster1.png')
refresh = tk.PhotoImage(file='refresh.png')
search = tk.PhotoImage(file='search.png')
source = tk.PhotoImage(file='view.png')
IndFlag = IndFlag.subsample(20,20)
source = source.subsample(20,20)
search = search.subsample(5, 5)

imglabel = tk.Label(win,image=poster)
imglabel.pack()

IND = tk.Label(win,text='INDIA',image=IndFlag,compound=tk.LEFT,font=f)
IND.place(x=640,y=52)

label = tk.Label(win,fg='white',bg='red',text = getCoronaData(),font=f,compound=tk.CENTER,justify=tk.CENTER)
label.place(x=395,y=120)

refreshbtn = tk.Button(win,bd='5',width=100,height=39,image=refresh,command=refreshButton,cursor="hand2")
refreshbtn.place(x=700,y=550)

searchbtn = tk.Button(win,bd='5',width=200,height=50,image=search,text='Search By State',compound=tk.LEFT,font=fbn,fg='white',bg='red',command=searchbyState,cursor="hand2")
searchbtn.place(x=320,y=550)

sourcebtn = tk.Button(win,bd='5',text='View Source Page',image=source,compound=tk.LEFT,font=fbn,fg='white',bg='red',width=200,height=50,command=viewSource,cursor="hand2")
sourcebtn.place(x=1010,y=550)

th = threading.Thread(target=notifyMe)
th.setDaemon(True)
th.start()

win.mainloop()