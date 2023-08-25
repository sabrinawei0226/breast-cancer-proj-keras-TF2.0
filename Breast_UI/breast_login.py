import tkinter as tk
from PIL import Image,ImageTk
import subprocess
#------------------------------------------------------------------------------------------------
root=tk.Tk()
root.state('zoomed')
#root.iconbitmap('./images/icon.ico')
root.title('BI-CNN偵測婦女乳房群聚鈣化點及預測鈣化點良惡')
root.configure(background='#000000')
#------------------------------------------------------------------------------------------------
#跳到下一頁
def jump():
    subprocess.call('python ./cluster_analysis.py',shell=True);
#------------------------------------------------------------------------------------------------
region_1=tk.Label(root,width=50,height=1000,bg='#44546A').place(x=0,y=0)
#icon
big_icon=tk.PhotoImage(file='./images/big_icon.png')
icon=tk.Label(root,image=big_icon,width=450,height=450,bg='#000000').place(x=430,y=200)

#title
title_line1=tk.Label(root,text='BI-CNN',width=6,height=1,bg='#000000',fg='#FFE699',font=('Times New Roman',45,'bold')).place(x=980,y=300)
title_line2=tk.Label(root,text='偵測',width=4,height=1,bg='#000000',fg='#FFE699',font=('標楷體',45,'bold')).place(x=1205,y=305)
title_line3=tk.Label(root,text='婦女乳房群聚鈣化點',width=18,height=1,bg='#000000',fg='#FFE699',font=('標楷體',45,'bold')).place(x=880,y=375)
title_line4=tk.Label(root,text='及預測鈣化點良惡',width=18,height=1,bg='#000000',fg='#FFE699',font=('標楷體',45,'bold')).place(x=880,y=445)

information=tk.Label(root,text='本系統利用深度學習演算法自動分析乳房攝影影像，以輔助醫師看診',width=60,height=1,bg='#000000',fg='#ffffff',font=('標楷體',20))
information.place(x=550,y=630)

notice_line1=tk.Label(root,text='※為保障病患隱私權',width=20,height=1,bg='#44546A',fg='#ffffff',font=('標楷體',14,'bold')).place(x=10,y=30)
notice_line2=tk.Label(root,text='此系統僅限醫事相關人員使用',width=26,height=1,bg='#44546A',fg='#ffffff',font=('標楷體',14,'bold')).place(x=40,y=56)
notice_line3=tk.Label(root,text='請輸入帳號密碼以核對身分',width=24,height=1,bg='#44546A',fg='#ffffff',font=('標楷體',14,'bold')).place(x=40,y=82)


enter1=tk.Label(root,text='帳號:',width=5,height=1,bg='#44546A',fg='#ffffff',font=('標楷體',18,'bold')).place(x=40,y=182)
enter2=tk.Label(root,text='密碼:',width=5,height=1,bg='#44546A',fg='#ffffff',font=('標楷體',18,'bold')).place(x=40,y=242)

input_1=tk.Entry(root,show=None,width=15,font=("Times New Roman",18),bg='#ffffff').place(x=125,y=182)
input_2=tk.Entry(root,show='*',width=15,font=("Times New Roman",18),bg='#ffffff').place(x=125,y=242)

#square_image=tk.PhotoImage(file='./images/square.png')
#square=tk.Label(root,image=square_image,width=800,height=350,bg='#000000').place(x=385,y=285)

#登入
login_image=tk.PhotoImage(file='./images/login.png')
login=tk.Button(root,image=login_image,width=85,height=50,bg='#44546A',bd=0,activebackground='#44546A',command=jump)
login.place(x=122,y=300)
#註冊
regist_image=tk.PhotoImage(file='./images/regist.png')
regist=tk.Button(root,image=regist_image,width=85,height=50,bg='#44546A',bd=0,activebackground='#44546A').place(x=227,y=300)  





root.mainloop()
