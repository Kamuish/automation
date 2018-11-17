import tkinter as tk 
from tkinter import filedialog

from functionalitty import import_from_file

from friend_db import manual_insert_user, insert_gift, has_match

def populate_db():
    users_from_file = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
    import_from_file(users_from_file)
def main():
    window = tk.Tk()
    window.geometry("266x208")
    window.title("Secret_friend")

    but = tk.Button(window,text = 'Import from file', command = lambda: populate_db())
    but.pack()

    listbox = tk.Listbox(window)
    listbox.pack()
    window.mainloop()


if __name__ == '__main__':
    main()