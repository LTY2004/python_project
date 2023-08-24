import tkinter as tk
from tkinter import messagebox

# 创建游戏主窗口和棋盘
window = tk.Tk()
window.title("happy五子棋")

# 创建棋盘
board = [[' ' for _ in range(20)] for _ in range(20)]

# 当前玩家，默认为黑棋
current_player = '黑'

# 统计黑棋和白棋的胜利次数
black_wins = 0
white_wins = 0

# 保存每步棋的历史记录
move_history = []

# 处理落子操作
def place_piece(row, col):
    global current_player
    if board[row][col] == ' ':
        board[row][col] = current_player
        move_history.append((row, col))
        draw_piece(row, col, current_player)
        if check_win(row, col):
            messagebox.showinfo("游戏结束", f"{current_player}棋获胜！")
            update_scoreboard(current_player)
            reset_game()
        else:
            current_player = '黑' if current_player == '白' else '白'
            update_current_player_label()
    else:
        messagebox.showinfo("提示", "该位置已经有棋子了，请选择其他位置。")

# 悔棋操作
def undo_move():
    if move_history:
        global current_player
        current_player = '黑' if current_player == '白' else '白'
        last_move = move_history.pop()
        row, col = last_move
        player = board[row][col]
        board[row][col] = ' '
        tag_to_delete = f'{chr(ord("A") + row)}{chr(ord("A") + col)}'
        canvas.delete(tag_to_delete)
        update_current_player_label()


# 绘制棋盘网格
def draw_board():
    for i in range(19):
        canvas.create_line(15 + i * 30, 15, 15 + i * 30, 555)
        canvas.create_line(15, 15 + i * 30, 555, 15 + i * 30)

# 绘制棋子
def draw_piece(row, col, player):
    x = 15 + col * 30
    y = 15 + row * 30
    if player == '黑':
        tag = f'{chr(ord("A") + row)}{chr(ord("A") + col)}'
        canvas.create_oval(x - 13, y - 13, x + 13, y + 13, fill='black', tags=tag)
    else:
        tag = f'{chr(ord("A") + row)}{chr(ord("A") + col)}'
        canvas.create_oval(x - 13, y - 13, x + 13, y + 13, fill='white', tags=tag)


# 更新当前玩家标签
def update_current_player_label():
    current_player_label.config(text=f"当前玩家：{current_player}棋")

# 更新胜利次数显示
def update_scoreboard(player):
    global black_wins, white_wins
    if player == '黑':
        black_wins += 1
        black_score_label.config(text=f"黑棋胜利次数：{black_wins}")
    else:
        white_wins += 1
        white_score_label.config(text=f"白棋胜利次数：{white_wins}")

# 重置游戏
def reset_game():
    canvas.delete("all")
    draw_board()
    for i in range(19):
        for j in range(19):
            board[i][j] = ' '
    global current_player, move_history
    current_player = '黑'
    move_history = []
    update_current_player_label()

# 检查胜利条件
def check_win(row, col):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        # 向上或向左延伸
        i, j = row, col
        while i - dx >= 0 and j - dy >= 0 and board[i - dx][j - dy] == board[row][col]:
            count += 1
            i -= dx
            j -= dy
        # 向下或向右延伸
        i, j = row, col
        while i + dx < 19 and j + dy < 19 and board[i + dx][j + dy] == board[row][col]:
            count += 1
            i += dx
            j += dy
        if count >= 5:
            return True
    return False

# 鼠标点击事件处理函数
def handle_click(event):
    col = (event.x) // 30
    row = (event.y) // 30
    if 0 <= row < 19 and 0 <= col < 19:
        place_piece(row, col)

# 创建棋盘和棋子
canvas0 = tk.Canvas(window, width=600, height=630)
canvas0.config(bg='dark red')
canvas0.pack()
canvas = tk.Canvas(window, width=570, height=570)
canvas.config(bg='gray')
canvas.place(x=15,y=15)
draw_board()



# 绑定鼠标点击事件
canvas.bind("<Button-1>", handle_click)

# 创建底部标签和按钮
current_player_label = tk.Label(window, text=f"当前玩家：{current_player}棋",fg='yellow',bg='dark red')
current_player_label.place(x=50,y=600)

black_score_label = tk.Label(window, text="黑棋胜利次数：0",fg='yellow',bg='dark red')
black_score_label.place(x=350,y=600)

white_score_label = tk.Label(window, text="白棋胜利次数：0",fg='yellow',bg='dark red')
white_score_label.place(x=450,y=600)

undo_button = tk.Button(window, text="悔棋", command=undo_move)
undo_button.place(x=280,y=600)

# 启动主循环
window.mainloop()
