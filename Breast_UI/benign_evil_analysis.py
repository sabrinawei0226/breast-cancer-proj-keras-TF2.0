import tkinter as tk
from PIL import Image,ImageTk
import time
import subprocess
import tkinter.messagebox 
#------------------------------------------------------------------------------------------------
root=tk.Tk()
root.state('zoomed')
#root.iconbitmap('./images/icon.ico')
root.title('BI-CNN偵測婦女乳房群聚鈣化點及預測鈣化點良惡')
root.configure(background='#000000')
#------------------------------------------------------------------------------------------------
def mark():
    global open_word_2,open_benign_2
    open_word_2=tk.PhotoImage(file='./images/word_2.png')
    left_word_2.config(image=open_word_2,width=250,height=150)
    left_word_2.place(x=40,y=580)
    open_benign_2=tk.PhotoImage(file='./images/benign_2.png')
    label_benign_1.config(image=open_benign_2)
    time.sleep(3)
    tk.messagebox.showinfo(title='information',message='分析完成!')
    download.config(image=download_image_true,state='normal')
    big.config(image=big_image_true,state='normal')
def back_change():
    subprocess.call('python ./cluster_analysis.py',shell=True);
def download():
    time.sleep(2)
    tk.messagebox.showinfo(title='information',message='下載完成!')  
def home_change():
    subprocess.call('python ./breast_login.py',shell=True);
def zoom():
    subprocess.call('python ./bigsmall_2.py',shell=True);
#------------------------------------------------------------------------------------------------
region_1=tk.Label(root,width=1000,height=10,bg='#44546A').place(x=0,y=0)
open_icon=tk.PhotoImage(file='./images/title_icon.png')
title_icon=tk.Label(root,image=open_icon,width=60,height=60,bg='#44546A').place(x=10,y=25)
title=tk.Label(root,text='偵測婦女乳房群聚鈣化點及預測鈣化點良惡',width=40,height=1,bg='#44546A',fg='#FFE699',font=('標楷體',30,'bold'))   #系統名稱
title.place(x=200,y=32)
title_eg=tk.Label(root,text='BI-CNN',width=6,height=1,bg='#44546A',fg='#FFE699',font=('Times New Roman',30,'bold'))
title_eg.place(x=80,y=30)

#群聚分析標題
function_cluster=tk.Label(root,text='群聚分析',width=8,height=1,bg='#44546A',fg='#ffffff',font=('標楷體',25)) 
function_cluster.place(x=850,y=100)
open_label=tk.PhotoImage(file='./images/yellow.png')
#label=tk.Label(root,image=open_label,width=135,height=3,bg='#000000').place(x=851,y=135)

#良惡分析標題
function_benign=tk.Label(root,text='良惡分析',width=8,height=1,bg='#44546A',fg='#ffffff',font=('標楷體',25))  
function_benign.place(x=1030,y=100)
label_2=tk.Label(root,image=open_label,width=135,height=3,bg='#000000')
label_2.place(x=1031,y=135)

#醫師登出
open_doctor_logout=tk.PhotoImage(file='./images/doctor_logout.png')
doctor_logout=tk.Label(root,image=open_doctor_logout,width=400,height=75,bg='#44546A')          
doctor_logout.place(x=1200,y=75)
img_change1=tk.Label(root,image='',width=47,height=28,bg='#000000')
img_change1.place(x=199,y=169)

#回上頁
back_image=tk.PhotoImage(file='./images/back.png')
back=tk.Button(root,image=back_image,width=45,height=40,bg='#44546A',bd=0,activebackground='#44546A',command=back_change).place(x=1255,y=25) 
#放大 
big_image_false=tk.PhotoImage(file='./images/big_disable.png')
big_image_true=tk.PhotoImage(file='./images/big.png')
big=tk.Button(root,image=big_image_false,width=45,height=42,bg='#44546A',bd=0,activebackground='#44546A',state='disabled',command=zoom)
big.place(x=1325,y=25)
#下載圖片 
download_image_false=tk.PhotoImage(file='./images/download_disable.png')
download_image_true=tk.PhotoImage(file='./images/download.png')
download=tk.Button(root,image=download_image_false,width=45,height=45,bg='#44546A',bd=0,activebackground='#44546A',state='disabled',command=download)
download.place(x=1395,y=25)
#回首頁  
home_image=tk.PhotoImage(file='./images/home.png')
home=tk.Button(root,image=home_image,width=48,height=48,bg='#44546A',bd=0,activebackground='#44546A',command=home_change).place(x=1465,y=23)  

benign_1=tk.PhotoImage(file='./images/benign_1.png')
label_benign_1=tk.Label(root,image=benign_1,width=750,height=420,bg='#ffffff')
label_benign_1.place(x=400,y=200)

#良惡分析
evil=tk.PhotoImage(file='./images/evil.png')
evil_analysis=tk.Button(root,image=evil,width=500,height=125,bg='#000000',bd=0,relief='flat',activebackground='#000000',command=mark)  
evil_analysis.place(x=535,y=650)

open_left_word=tk.PhotoImage(file='./images/word_1.png')
left_word=tk.Label(root,image=open_left_word,width=350,height=275,bg='#000000',bd=0,activebackground='#000000')
left_word.place(x=25,y=200)

open_left_word_2=tk.PhotoImage(file='./images/nothing.png')
left_word_2=tk.Label(root,image=open_left_word_2,width=200,height=100,bg='#000000',bd=0,activebackground='#000000')
left_word_2.place(x=50,y=600)

open_patient_information=tk.PhotoImage(file='./images/patient_information.png')
patient_information=tk.Label(root,image=open_patient_information,width=200,height=300,bg='#000000',bd=0,activebackground='#000000')
patient_information.place(x=1240,y=250)

dash_1=tk.Label(root,text='陳小名',font=('標楷體',20,'bold'),width=5,height=1,bg='#000000',fg='#ffffff')
dash_1.place(x=1360,y=350)
dash_2=tk.Label(root,text='TC-05',width=5,height=1,bg='#000000',fg='#ffffff',font=('Times New Roman',20,'bold'))
dash_2.place(x=1365,y=410)
dash_3=tk.Label(root,text='109/02/20',font=('Times New Roman',20,'bold'),width=8,height=1,bg='#000000',fg='#ffffff')
dash_3.place(x=1340,y=470)
root.mainloop()

