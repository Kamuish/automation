import tkinter as tk 
from tkinter import filedialog

from functionalitty import import_from_file,create_pairs

from friend_db import manual_insert_user, insert_gift,get_all_users

def populate_db():
    users_from_file = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    import_from_file(users_from_file)


def send_mails(selection,email,pw):
    user_ids = [i + 1 for i in selection]
    create_pairs(user_ids,2018,1,1)


def main():
    window = tk.Tk()
    window.geometry("250x150")
    window.title("Secret_friend")

    but = tk.Button(window,text = 'Import from file', command = lambda: populate_db())

    listbox = tk.Listbox(window,selectmode = 'multiple')

    users = get_all_users()
    [listbox.insert(tk.END,a.name) for a in users]

    check = tk.Checkbutton(window,text = 'Use all')
    

    email = tk.Entry(window, width=15)
    email_lab = tk.Label(text = 'Email')
    widget = tk.Entry(window,text = 'Password', show="*", width=15)
    widg_lab = tk.Label(text = 'Password')
    year = tk.Entry(window,text = 'Last year', width=15)
    year_lab = tk.Label(text = 'year')

    send = tk.Button(window,text = 'Send', command = lambda: send_mails(listbox.curselection(),email.get(),widget.get()))


    year.grid(row = 1, column = 2)
    year_lab.grid(row = 1, column =1)

    email.grid(row = 2, column = 2)
    email_lab.grid(row = 2, column =1)

    widget.grid(row = 3, column = 2)
    widg_lab.grid(row = 3, column =1)

    but.grid(row = 0, column = 1, columnspan = 2)

    listbox.grid(row = 0, column = 0, rowspan = 5)

    

    check.grid(row = 5, column = 0)
    send.grid(row = 4, column = 1,columnspan = 2)

    window.mainloop()


if __name__ == '__main__':
    main()