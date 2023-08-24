from tkinter import Tk,Button,Label,messagebox as msg,PhotoImage
from random import shuffle

def btclick(e):
    global tmr,stop,first
    if sec==0:stop=0;tmr=rt.after(1000,updateSec)#启用计时器
    if first<0:first=e.widget.pos;bt[first]["bg"]="red"#第1个图背景红色
    else:#单击的是第2个图
        bt[first]["bg"]="SystemButtonFace"#恢复第1个图背景
        p1=[first//10,first%10]#第1个单击按钮所在行、列
        p=e.widget.pos;p2=[p//10,p%10]#第2个单击按钮所在行、列
        if (bt[first].gid==bt[p].gid) and (first!=p):#图像相同，按钮不同
            if check(p1,p2):#2个按钮能连接
                bt[first].place_forget();bt[p].place_forget()#2个按钮隐藏
                ishide[first]=1;ishide[p]=1#记录隐藏
            if 0 not in ishide:#全部按钮均隐藏
                rt.after_cancel(tmr)#终止计时器
                msg.showinfo("恭喜恭喜","游戏成功完成！")
        first=-1#标记未单击任何按钮
def check(p1,p2):#检查2个按钮是否能隐藏
    r1=p1[0];c1=p1[1];r2=p2[0];c2=p2[1]#按钮A(r1,c1)、按钮B(r2,c2)
    if c1!=c2:#仅在列不同时需按行搜索转向点C(r,c1)、D(r,c2)
        for r in range(10):
            if r==r1:#A、C重合
                if r==r2:#B、D重合
                    if (r in (0,9)) or canjoin(r,c1,r,c2):return 1#A、B同边界或直连
                elif ishide[r*10+c2]:#B、D不重合；D无图
                    if (r in (0,9)) and canjoin(r,c2,r2,c2):return 1#C、D同边界；B、D直连
                    if canjoin(r,c1,r,c2):#C、D直连
                        if (c2 in (0,9)) or canjoin(r,c2,r2,c2):return 1#B、D同边界或直连
            elif r==r2:#A、C不重合；B、D重合
                if ishide[r*10+c1]:#C无图
                    if canjoin(r,c1,r,c2):#C、D直连
                        if (c1 in (0,9)) or canjoin(r,c1,r1,c1):return 1#A、C同边界或直连
            elif ishide[r*10+c1] and ishide[r*10+c2]:#A、C不重合；B、D不重合；C、D无图
                if canjoin(r1,c1,r,c1) and canjoin(r,c2,r2,c2):#A、C直连；B、D直连
                    if (r in (0,9)) or canjoin(r,c1,r,c2):return 1#C、D同边界或直连
    if r1!=r2:#仅在行不同时需按列搜索
        for c in range(10):
            if c==c1:#A、C重合
                if c==c2:#B、D重合
                    if (c in (0,9)) or canjoin(r1,c,r2,c):return 1#A、B同边界或直连
                elif ishide[r2*10+c]:#B、D不重合；D无图
                    if (c in (0,9)) and canjoin(r2,c,r2,c2):return 1#C、D同边界；B、D直连
                    if canjoin(r1,c,r2,c):#C、D直连
                        if (r2 in (0,9)) or canjoin(r2,c,r2,c2):return 1#B、D同边界或直连
            elif c==c2:#A、C不重合；B、D重合
                if ishide[r1*10+c]:
                    if canjoin(r1,c,r2,c):#C无图
                        if (r1 in (0,9)) or canjoin(r1,c,r1,c1):return 1#A、C同边界或直连
            elif ishide[r1*10+c] and ishide[r2*10+c]:#A、C不重合；B、D不重合；C、D无图
                if canjoin(r1,c1,r1,c) and canjoin(r2,c,r2,c2):#A、C直连；B、D直连
                    if (c in (0,9)) or canjoin(r1,c,r2,c):return 1#C、D同边界或直连
    return 0
def canjoin(r1,c1,r2,c2):
    #(r1,c1)与(r2,c2)能否直连(r1=r2 or c1=c2)
    if r1==r2:r=0;c=1 if c1<c2 else -1#确定连接的中间点对应的r和c增量
    else:c=0;r=1 if r1<r2 else -1
    while 1:
        r1+=r;c1+=c
        if (r1==r2) and (c1==c2):return 1
        if ishide[r1*10+c1]==0:return 0#中间点有图
def start():
    global first,sec,stop
    if sec>0:stop=1
    sec=0;lsec["text"]=0;first=-1
    pos=list(range(100));shuffle(pos)#0-99乱序后作为25个图像的显示位置索引
    for p in range(100):
        bt[p].gid=pos[p]%25
        bt[p]["image"]=img[bt[p].gid];ishide[p]=0
        bt[p].place(x=(p%10)*45,y=(p//10)*45)
def updateSec():#计时器
    global sec,tmr
    if stop:return
    sec+=1
    lsec["text"]=sec;tmr=rt.after(1000,updateSec)
   
first=-1#第1次单击的按钮索引
ishide=[0]*100#100个按钮是否隐藏
bt=[0]*100#100个按钮对象
tmr=0#计时器
sec=0#游戏经历的秒数
stop=0#终止计时

rt=Tk()#创建窗体
rt.title("连连看")#设置窗口标题
rt.geometry("450x480")
rt.resizable(width=0,height=0) #窗口不能改变大小
for k in range(100):
    bt[k]=Button(rt);bt[k].pos=k
    bt[k].bind("<ButtonRelease-1>",btclick)
Button(rt,text="开始",width=6,command=start).place(x=210,y=450)
Label(rt,text="游戏秒数：").place(x=10,y=455)
lsec=Label(rt,text="0");lsec.place(x=73,y=455)
img=[PhotoImage(file=f"png\\t{k}.png") for k in range(1,26)]#25个图像对象
start()
rt.mainloop()
