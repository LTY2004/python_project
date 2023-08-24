from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import random

class Game:
    def __init__(self):
        self.numlist = [0, 0, 0]
        self.player_turn = True

        # Create window
        root = Tk()
        root.title("火柴游戏（人机对战版）")
        root.geometry("515x370")  # (宽度x高度)
        Label(root, text="第 1 堆   第 2 堆   第 3 堆", fg='yellow', bg='dark red', font=("Lucida Grande", 16)).place(x=45,
                                                                                                                y=20)
        Label(root, text="玩家从第    堆取走    根火柴", fg='yellow', bg='dark red', font=("Lucida Grande", 16)).place(x=45,
                                                                                                              y=320)
        root.configure(bg='dark red')

        # Button
        Button(root, command=self.start, text="开始", width=6).place(x=380, y=60)
        Button(root, command=self.intro, text="说明", width=6).place(x=450, y=60)
        Button(root, command=self.lose, text="认输", width=6).place(x=395, y=320)
        Button(root, command=self.submit, text="提交", width=6).place(x=450, y=320)
        self.var = IntVar()
        self.check = Checkbutton(root, text="电脑先手", bg='dark red', variable=self.var, font=("Lucida Grande", 16))
        self.check.place(x=380, y=20)

        # Text box
        self.text_box1 = ScrolledText(root, width=65, height=15, )
        self.text_box1.place(x=10, y=110)
        self.choose1 = Entry(root, width=3)
        self.choose1.place(x=138, y=322)
        self.choose2 = Entry(root, width=3)
        self.choose2.place(x=245, y=322)
        self.sticks1 = StringVar()
        self.s1 = Entry(root, font=20, width=3, textvariable=self.sticks1, state='readonly')
        self.s1.place(x=56, y=60)
        self.sticks2 = StringVar()
        self.s2 = Entry(root, font=20, width=3, textvariable=self.sticks2, state='readonly')
        self.s2.place(x=156, y=60)
        self.sticks3 = StringVar()
        self.s3 = Entry(root, font=20, width=3, textvariable=self.sticks3, state='readonly')
        self.s3.place(x=256, y=60)
        self.slist = [self.sticks1, self.sticks2, self.sticks3]

        root.mainloop()

    def start(self):
        for i in range(3):
            self.numlist[i] = random.randint(10, 99)
            self.slist[i].set(self.numlist[i])
        self.text_box1.insert(CURRENT, "当前状态:" + str(self.numlist[0]) + "," + str(self.numlist[1]) + "," + str(
            self.numlist[2]) + '\n')
        if self.var.get():
            self.computer_turn()

    def intro(self):
        messagebox.showinfo("操作提示", """=======游戏规则=======
1. 玩家和电脑依次从任意一堆火柴中取走1根以上的火柴。
2. 谁拿到最后一根火柴谁就胜利
3. 不得拿走超过当前堆中数量上限的火柴""")

    def lose(self):
        messagebox.showinfo("电脑胜出", "你要加油哦~")
        for i in range(3):
            self.numlist[i] = 0
            self.slist[i].set(self.numlist[i])
            self.text_box1.delete('1.0', END)

    def submit(self):
        try:
            pile = int(self.choose1.get())
            matches = int(self.choose2.get())

            if pile not in [1, 2, 3]:
                raise ValueError("填写的火柴堆只能是1、2、3")

            if self.numlist[pile - 1] == 0:
                raise ValueError("该堆火柴数为0，不能填写该堆")

            if not 1 <= matches <= self.numlist[pile - 1]:
                raise ValueError("取走火柴的数目应是[1,n]上的整数，其中n为所在堆的火柴数")

            self.numlist[pile - 1] -= matches
            self.slist[pile - 1].set(self.numlist[pile - 1])
            self.text_box1.insert(CURRENT, "玩家在第" + str(pile) + "堆中拿走了" + str(matches) + "根火柴\n")
            self.text_box1.insert(CURRENT, "当前状态:" + str(self.numlist[0]) + "," + str(self.numlist[1]) + "," + str(
                self.numlist[2]) + '\n')

            if self.numlist[0] + self.numlist[1] + self.numlist[2] <= 0:
                messagebox.showinfo("游戏结果", "你赢了！恭喜！")
                self.numlist[0] = 0
                self.numlist[1] = 0
                self.numlist[2] = 0
                self.sticks1.set(self.numlist[0])
                self.sticks2.set(self.numlist[1])
                self.sticks3.set(self.numlist[2])
                self.text_box1.delete('1.0', END)
            else:
                self.computer_turn()
        except ValueError as e:
            messagebox.showinfo("错误", str(e))

    def computer_turn(self):
        nsum = self.numlist[0] ^ self.numlist[1] ^ self.numlist[2]

        if nsum != 0:
            for i in range(3):
                if self.numlist[i] ^ nsum < self.numlist[i]:
                    pile = i + 1
                    matches = self.numlist[i] - (self.numlist[i] ^ nsum)
                    break
        else:
            for i in range(3):
                if self.numlist[i] > 0:
                    pile = i + 1
                    matches = random.randint(1, min(3, self.numlist[i]))
                    break

        self.numlist[pile - 1] -= matches
        for i in range(3):
            self.slist[i].set(self.numlist[i])
        self.text_box1.insert(CURRENT, "电脑在第" + str(pile) + "堆中拿走了" + str(matches) + "根火柴\n")
        self.text_box1.insert(CURRENT, "当前状态:" + str(self.numlist[0]) + "," + str(self.numlist[1]) + "," + str(
            self.numlist[2]) + '\n')

        if self.numlist[0] + self.numlist[1] + self.numlist[2] <= 0:
            messagebox.showinfo("游戏结果", "电脑赢了！再接再厉！")
            for i in range(3):
                self.numlist[i] = 0
                self.slist[i].set(self.numlist[i])
                self.text_box1.delete('1.0', END)


game = Game()
