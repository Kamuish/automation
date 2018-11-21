import tkinter as tk 
from tkinter import filedialog

from functionalitty import import_from_file,create_pairs, import_gifts_from_file

from friend_db import manual_insert_user, insert_gift,get_all_users

def populate_db_users(root):
    users_from_file = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    import_from_file(users_from_file)

    root.event_generate("<<users>>")

def populate_db_gifts():
    gifts_from_file = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    import_gifts_from_file(gifts_from_file)

def send_mails(selection,email,pw):
    user_ids = [i + 1 for i in selection]
    create_pairs(user_ids,2018,email,pw)


def main():
    window = tk.Tk()
    #window.geometry("350x150")
    window.title("Secret_friend")

    but = tk.Button(window,text = 'Import users', command = lambda: populate_db_users(window))
    but1 = tk.Button(window,text = 'Import gifts', command = lambda: populate_db_gifts())

    listbox = tk.Listbox(window,selectmode = 'multiple')

    
    def draw_users():
        users = get_all_users()
        [listbox.insert(tk.END,a.name) for a in users]

    draw_users()

    window.bind("<<users>>", lambda y : draw_users())
    def select_all():
        listbox.select_set(0,tk.END)
    check = tk.Button(window,text = 'Select all', command = lambda: select_all())
    

    email = tk.Entry(window, width=30)
    email_lab = tk.Label(text = 'Email')
    widget = tk.Entry(window,text = 'Password', show="*", width=30)
    widg_lab = tk.Label(text = 'Password')
    year = tk.Entry(window,text = 'Last year', width=30)
    year_lab = tk.Label(text = 'year')

    send = tk.Button(window,text = 'Send', command = lambda: send_mails(listbox.curselection(),email.get(),widget.get()))



    year.grid(row = 1, column = 2)
    year_lab.grid(row = 1, column =1)

    email.grid(row = 2, column = 2)
    email_lab.grid(row = 2, column =1)

    widget.grid(row = 3, column = 2)
    widg_lab.grid(row = 3, column =1)

    but.grid(row = 0, column = 1, columnspan = 1, sticky = 'nsew')
    but1.grid(row = 0, column = 2, columnspan = 1, sticky = 'nsew')


    listbox.grid(row = 0, column = 0, rowspan = 5)

    

    check.grid(row = 5, column = 0, sticky = 'nsew')
    send.grid(row = 5, column = 1,columnspan = 2, sticky = 'nsew')

    window.mainloop()


if __name__ == '__main__':
    main()