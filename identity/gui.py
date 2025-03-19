import tkinter as tk
from tkinter import ttk, messagebox
from main import register_user, login_user, change_password


def create_gui():
    """创建身份认证系统的主界面"""
    global root
    root = tk.Tk()
    root.title('身份认证系统')
    root.geometry('600x450')  # 设置窗口宽高比为 4:3
    root.resizable(False, False)  # 禁止调整窗口大小

    # 设置全局字体样式
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TButton', font=('Arial', 11))
    style.configure('TEntry', font=('Arial', 12))

    # 主框架
    global main_frame
    main_frame = ttk.Frame(root, padding="30")  # 增加主框架的内边距
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # 将主框架居中显示

    # 标题
    global title_label
    title_label = ttk.Label(main_frame, text='欢迎使用身份认证系统', font=('Arial', 16), anchor=tk.CENTER)
    title_label.grid(row=0, column=0, columnspan=2, pady=20)  # 增加标题与其他控件的垂直间距

    # 用户名标签和输入框
    global label_username, entry_username
    label_username = ttk.Label(main_frame, text='用户名:')
    label_username.grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)  # 增加控件之间的间距
    entry_username = ttk.Entry(main_frame, width=30)
    entry_username.grid(row=1, column=1, padx=10, pady=10)

    # 密码标签和输入框
    global label_password, entry_password
    label_password = ttk.Label(main_frame, text='密码:')
    entry_password = ttk.Entry(main_frame, show='*', width=30)

    # 旧密码和新密码标签及输入框（用于修改密码）
    global label_old_password, entry_old_password, label_new_password, entry_new_password
    label_old_password = ttk.Label(main_frame, text='旧密码:')
    entry_old_password = ttk.Entry(main_frame, show='*', width=30)
    label_new_password = ttk.Label(main_frame, text='新密码:')
    entry_new_password = ttk.Entry(main_frame, show='*', width=30)

    # 按钮容器
    global button_frame
    button_frame = ttk.Frame(main_frame, padding="20")  # 增加按钮容器的内边距
    button_frame.grid(row=5, column=0, columnspan=2, pady=20)  # 将按钮框架放在第5行，避免与动态控件冲突

    # 注册、登录、修改密码、清空按钮
    global button_register, button_login, button_change_pw, button_clear
    button_register = ttk.Button(button_frame, text='注册', command=show_register)
    button_register.pack(side=tk.LEFT, padx=15, pady=10)  # 增大按钮之间的水平和垂直间距

    button_login = ttk.Button(button_frame, text='登录', command=show_login)
    button_login.pack(side=tk.LEFT, padx=15, pady=10)

    button_change_pw = ttk.Button(button_frame, text='修改密码', command=show_change_password)
    button_change_pw.pack(side=tk.LEFT, padx=15, pady=10)

    button_clear = ttk.Button(button_frame, text='清空', command=clear_entries)
    button_clear.pack(side=tk.LEFT, padx=15, pady=10)

    # 提交按钮（动态变化）
    global button_submit
    button_submit = ttk.Button(main_frame)

    # 提交修改密码按钮
    global button_submit_change_pw
    button_submit_change_pw = ttk.Button(main_frame, text='提交修改', command=change_password_handler)

    # 退出按钮
    global button_exit
    button_exit = ttk.Button(root, text='退出', command=root.quit)
    button_exit.pack(side=tk.BOTTOM, pady=20)  # 放置在底部，增加与边框的垂直间距

    # 隐藏所有动态控件
    hide_all_fields()
    root.mainloop()


def hide_all_fields():
    """隐藏所有动态字段和按钮"""
    label_password.grid_forget()
    entry_password.grid_forget()
    label_old_password.grid_forget()
    entry_old_password.grid_forget()
    label_new_password.grid_forget()  # 隐藏新密码标签
    entry_new_password.grid_forget()  # 隐藏新密码输入框
    button_submit.grid_forget()
    button_submit_change_pw.grid_forget()


def show_register():
    """显示注册界面"""
    hide_all_fields()
    label_password.grid(row=2, column=0, sticky=tk.E, pady=5)
    entry_password.grid(row=2, column=1, pady=5)
    button_submit.config(text='提交注册', command=register_user_handler)
    button_submit.grid(row=4, column=0, columnspan=2, pady=10)  # 修改提交按钮的位置


def show_login():
    """显示登录界面"""
    hide_all_fields()
    label_password.grid(row=2, column=0, sticky=tk.E, pady=5)
    entry_password.grid(row=2, column=1, pady=5)
    button_submit.config(text='提交登录', command=login_user_handler)
    button_submit.grid(row=4, column=0, columnspan=2, pady=10)  # 修改提交按钮的位置


def show_change_password():
    """显示修改密码界面"""
    hide_all_fields()  # 先隐藏其他控件

    # 显示旧密码控件
    label_old_password.grid(row=2, column=0, sticky=tk.E, pady=5)
    entry_old_password.grid(row=2, column=1, pady=5)

    # 显示新密码控件，调整到不与 button_frame 冲突的行
    label_new_password.grid(row=3, column=0, sticky=tk.E, pady=5)
    entry_new_password.grid(row=3, column=1, pady=5)

    # 显示提交修改按钮，调整到不与 button_frame 冲突的行
    button_submit_change_pw.grid(row=4, column=0, columnspan=2, pady=10)

    # 刷新布局（可选）
    main_frame.update()


def clear_entries():
    """清空所有输入框"""
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_old_password.delete(0, tk.END)
    entry_new_password.delete(0, tk.END)


def register_user_handler():
    """处理用户注册逻辑"""
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showwarning('警告', '用户名和密码不能为空！')
        return

    success, msg = register_user(username, password)
    if success:
        messagebox.showinfo('成功', msg)
        clear_entries()
        hide_all_fields()
    else:
        messagebox.showerror('错误', msg)


def login_user_handler():
    """处理用户登录逻辑"""
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showwarning('警告', '用户名和密码不能为空！')
        return

    success, msg = login_user(username, password)
    if success:
        messagebox.showinfo('成功', msg)
        clear_entries()
        hide_all_fields()
    else:
        messagebox.showerror('错误', msg)


def change_password_handler():
    """处理修改密码的逻辑"""
    username = entry_username.get().strip()
    old_password = entry_old_password.get().strip()
    new_password = entry_new_password.get().strip()

    if not username or not old_password or not new_password:
        messagebox.showwarning('警告', '所有字段不能为空！')
        return

    # 验证旧密码是否正确
    success, msg = login_user(username, old_password)
    if not success:
        messagebox.showerror('错误', '旧密码不正确或用户不存在！')
        return

    # 修改密码
    success, msg = change_password(username, new_password)
    if success:
        messagebox.showinfo('成功', msg)
        clear_entries()
        hide_all_fields()
    else:
        messagebox.showerror('错误', msg)


if __name__ == '__main__':
    create_gui()