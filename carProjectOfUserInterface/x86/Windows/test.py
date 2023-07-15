import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

root = tk.Tk()

# 创建ttkbootstrap样式对象
style = Style(theme='journal')

# 创建ttk.Button对象
button = ttk.Button(root, text='Click me!')

# 设置按键字体大小为20
style.configure('TButton', font=('TkDefaultFont', 20))

button.pack()
root.mainloop()