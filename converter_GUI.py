import os
import subprocess
import dataset
import tkinter as tk
from tkinter.filedialog import askdirectory
db = dataset.connect('sqlite:///:memory:')
table = db['file_list']


class MainWindow:
    def __init__(self):
        def gui():
            global path_entry, file_type, delete_option, select, done_text
            window.title("mkv to mp4")  # title
            tk.Label(window, text="Path to search").grid(row=1, column=1)
            path_entry = tk.Entry(window, width=30)  # entry for the path
            path_entry.grid(row=1, column=2)  # placing the entry boxes
            tk.Label(window, text="File Type").grid(row=2, column=1)
            file_type = tk.IntVar()
            delete_option = tk.IntVar()
            tk.Radiobutton(window, text="mkv", variable=file_type, value=1).grid(row=1, column=8)
            tk.Radiobutton(window, text="avi", variable=file_type, value=2).grid(row=1, column=9)
            tk.Radiobutton(window, text="wmv", variable=file_type, value=3).grid(row=1, column=10)
            tk.Radiobutton(window, text="mov", variable=file_type, value=4).grid(row=1, column=11)
            tk.Radiobutton(window, text="m4v", variable=file_type, value=5).grid(row=1, column=12)
            tk.Radiobutton(window, text="flac", variable=file_type, value=6).grid(row=1, column=13)
            tk.Checkbutton(window, text="Delete file when done", variable=delete_option)\
                .grid(row=2, column=7, columnspan=4)
            tk.Label(window, text="Choose the files you wish to convert").grid(row=4, column=1, columnspan=5)
            select = tk.Listbox(window, selectmode=tk.MULTIPLE, width=60)
            select.grid(row=5, column=1, columnspan=5)
            yscroll = tk.Scrollbar(command=select.yview, orient=tk.VERTICAL)
            yscroll.grid(row=5, column=6, sticky='nsw')
            select.configure(yscrollcommand=yscroll.set)
            xscroll = tk.Scrollbar(command=select.xview, orient=tk.HORIZONTAL)
            xscroll.grid(row=6, column=1, columnspan=5, sticky='ew')
            select.configure(xscrollcommand=xscroll.set)
            tk.Label(window, text="Done").grid(row=4, column=8, columnspan=5)
            done_text = tk.Listbox(window, width=60)
            done_text.grid(row=5, column=8, columnspan=5)
            yscroll2 = tk.Scrollbar(command=done_text.yview, orient=tk.VERTICAL)
            yscroll2.grid(row=5, column=13, sticky='nsw')
            done_text.configure(yscrollcommand=yscroll2.set)
            xscroll2 = tk.Scrollbar(command=done_text.xview, orient=tk.HORIZONTAL)
            xscroll2.grid(row=6, column=8, columnspan=5, sticky='ew')
            done_text.configure(xscrollcommand=xscroll2.set)

            return path_entry, file_type, delete_option, select, done_text

        def browser():
            global folder_path
            path_entry.delete(0, tk.END)
            folder_path = askdirectory()
            path_entry.insert(0, folder_path)
            return folder_path

        def type_text():
            if file_type.get() == 1:
                file_type_text = ".mkv"
            elif file_type.get() == 2:
                file_type_text = ".avi"
            elif file_type.get() == 3:
                file_type_text = ".wmv"
            elif file_type.get() == 4:
                file_type_text = ".mov"
            elif file_type.get() == 5:
                file_type_text = ".m4v"
            elif file_type.get() == 6:
                file_type_text = ".flac"
            else:
                file_type_text = ".idk"
            return file_type_text

        def delete_file():
            if delete_option.get() == 1:
                delete_text = "yes"
            else:
                delete_text = "no"
            return delete_text

        def search_file_names():
            folder = path_entry.get()  # gets the path filter
            folder = folder.replace('/', '\\')
            file_types = type_text()
            select.delete(0, tk.END)
            for dir_path, dir_names, file_names in os.walk(folder):  # things start happening, idk
                for filename in [f for f in file_names if f.endswith(file_types)]:
                    file_path = os.path.join(dir_path, filename)  # making the path
                    select.insert(tk.END, filename)
                    table.insert(dict(db_file_name=filename, db_dir_path=dir_path, db_file_path=file_path))

        def converter(file_name, dir_path):
            path = os.path.join(dir_path, file_name)
            path_without_type = path.strip(type_text())
            if type_text() == ".mkv":
                process = 'ffmpeg -hide_banner -i "' + path + '" -metadata title="" -strict experimental ' \
                    '-c:v copy -c:a aac -b:a 384k "' + path_without_type + '.mp4"'
            elif type_text() == ".flac":
                new_path = path_without_type.replace("foobar2000", "mp3")
                new_dir_path = dir_path.replace("foobar2000", "mp3")
                if not os.path.isdir(new_dir_path):
                    os.makedirs(new_dir_path)
                process = 'ffmpeg -hide_banner -i "' + path + '" -ab 320k -map_metadata 0 -id3v2_version 3 "' \
                          + new_path + '.mp3"'
            else:
                process = 'ffmpeg -hide_banner -i "' + path + '" -metadata title=""  -strict experimental ' \
                    '-c:v libx264 -preset ultrafast -c:a aac -b:a 384k "' + path_without_type + '.mp4"'
            print(process)
            subprocess.Popen(process, stdout=subprocess.PIPE).stdout.read()

        def converting_list():
            file_tuple = select.curselection()
            file_list = list(file_tuple)
            list_length = len(file_list)
            for x in range(0, list_length):
                name = select.get(file_list[x])
                file_name = table.find_one(db_file_name=name)['db_file_name']
                dir_path = table.find_one(db_file_name=name)['db_dir_path']
                converter(file_name, dir_path)
                done_text.insert(tk.END, name + " Is Done")
                window.update()
                if delete_file() == "yes":
                    path = os.path.join(dir_path, file_name)
                    os.remove(path)
            done_text.insert(tk.END, "All Done")

        gui()
        tk.Button(window, text="Browser", command=browser).grid(row=1, column=6)
        tk.Button(window, text="Search", command=search_file_names).grid(row=7, column=1)
        tk.Button(window, text="Start", command=converting_list).grid(row=7, column=6)
        tk.Button(window, text="Done", command=window.quit).grid(row=7, column=12, pady=10)
window = tk.Tk()
MainWindow()
window.mainloop()
