import os
import subprocess
import dataset
from tkinter import Tk, Label, Entry, IntVar, Radiobutton, Checkbutton, Listbox, MULTIPLE, Scrollbar, \
    VERTICAL, HORIZONTAL, Button, END
from tkinter.filedialog import askdirectory
db = dataset.connect('sqlite:///:memory:')
table = db['file_list']


class MainWindow:
    def __init__(self, window):
        self.window = window
        window.title('mkv to mp4')  # title
        Label(window, text='Path to search').grid(row=1, column=1)
        self.path_entry = Entry(window, width=30)  # entry for the path
        self.path_entry.grid(row=1, column=2)  # placing the entry boxes
        Label(window, text='File Type').grid(row=2, column=1)
        self.file_type = IntVar()
        self.delete_option = IntVar()
        Radiobutton(window, text='mkv', variable=self.file_type, value=1).grid(row=1, column=8)
        Radiobutton(window, text='avi', variable=self.file_type, value=2).grid(row=1, column=9)
        Radiobutton(window, text='wmv', variable=self.file_type, value=3).grid(row=1, column=10)
        Radiobutton(window, text='mov', variable=self.file_type, value=4).grid(row=1, column=11)
        Radiobutton(window, text='m4v', variable=self.file_type, value=5).grid(row=1, column=12)
        Radiobutton(window, text='flac', variable=self.file_type, value=6).grid(row=1, column=13)
        Checkbutton(window, text='Delete file when done', variable=self.delete_option)\
            .grid(row=2, column=7, columnspan=4)
        Label(window, text='Choose the files you wish to convert').grid(row=4, column=1, columnspan=5)
        self.select = Listbox(window, selectmode=MULTIPLE, width=60)
        self.select.grid(row=5, column=1, columnspan=5)
        self.yscroll = Scrollbar(command=self.select.yview, orient=VERTICAL)
        self.yscroll.grid(row=5, column=6, sticky='nsw')
        self.select.configure(yscrollcommand=self.yscroll.set)
        self.xscroll = Scrollbar(command=self.select.xview, orient=HORIZONTAL)
        self.xscroll.grid(row=6, column=1, columnspan=5, sticky='ew')
        self.select.configure(xscrollcommand=self.xscroll.set)
        Label(window, text='Done').grid(row=4, column=8, columnspan=5)
        self.done_text = Listbox(window, width=60)
        self.done_text.grid(row=5, column=8, columnspan=5)
        self.yscroll2 = Scrollbar(command=self.done_text.yview, orient=VERTICAL)
        self.yscroll2.grid(row=5, column=13, sticky='nsw')
        self.done_text.configure(yscrollcommand=self.yscroll2.set)
        self.xscroll2 = Scrollbar(command=self.done_text.xview, orient=HORIZONTAL)
        self.xscroll2.grid(row=6, column=8, columnspan=5, sticky='ew')
        self.done_text.configure(xscrollcommand=self.xscroll2.set)
        Button(self.window, text='Browser', command=self.browser).grid(row=1, column=6)
        Button(self.window, text='Search', command=self.search_file_names).grid(row=7, column=1)
        Button(self.window, text='Start', command=self.converting_list).grid(row=7, column=6)
        Button(self.window, text='Done', command=self.window.quit).grid(row=7, column=12, pady=10)

    def browser(self):
        self.path_entry.delete(0, END)
        folder_path = askdirectory()
        self.path_entry.insert(0, folder_path)
        return folder_path

    def type_text(self):
        if self.file_type.get() == 1:
            file_type_text = '.mkv'
        elif self.file_type.get() == 2:
            file_type_text = '.avi'
        elif self.file_type.get() == 3:
            file_type_text = '.wmv'
        elif self.file_type.get() == 4:
            file_type_text = '.mov'
        elif self.file_type.get() == 5:
            file_type_text = '.m4v'
        elif self.file_type.get() == 6:
            file_type_text = '.flac'
        else:
            file_type_text = '.idk'
        return file_type_text

    def delete_file(self):
        if self.delete_option.get() == 1:
            delete_text = 'yes'
        else:
            delete_text = 'no'
        return delete_text

    def search_file_names(self):
        folder = self.path_entry.get()  # gets the path filter
        folder = folder.replace('/', '\\')
        file_types = self.type_text()
        self.select.delete(0, END)
        for dir_path, dir_names, file_names in os.walk(folder):  # things start happening, idk
            for filename in [f for f in file_names if f.endswith(file_types)]:
                file_path = os.path.join(dir_path, filename)  # making the path
                self.select.insert(END, filename)
                table.insert(dict(db_file_name=filename, db_dir_path=dir_path, db_file_path=file_path))

    def converter(self, file_name, dir_path):
        path = os.path.join(dir_path, file_name)
        path_without_type = path.strip(self.type_text())
        if self.type_text() == '.mkv':
            process = 'ffmpeg -hide_banner -i "{0}" -metadata title="" -strict experimental ' \
                    '-c:v copy -c:a aac -b:a 384k "{1}.mp4"'.format(path, path_without_type)
        elif self.type_text() == '.flac':
            new_path = path_without_type.replace('foobar2000', 'mp3')
            new_dir_path = dir_path.replace('foobar2000', 'mp3')
            if not os.path.isdir(new_dir_path):
                os.makedirs(new_dir_path)
            process = 'ffmpeg -hide_banner -i "{0}" -ab 320k -map_metadata 0 -id3v2_version 3 "{1}.mp3"'\
                .format(path, new_path)
        else:
            process = 'ffmpeg -hide_banner -i "{0}" -metadata title=""  -strict experimental ' \
                      '-c:v libx264 -preset ultrafast -c:a aac -b:a 384k "{1}.mp4"'.format(path, path_without_type)
        print(process)
        subprocess.Popen(process, stdout=subprocess.PIPE).stdout.read()

    def converting_list(self):
        file_tuple = self.select.curselection()
        file_list = list(file_tuple)
        list_length = len(file_list)
        for x in range(0, list_length):
            name = self.select.get(file_list[x])
            file_name = table.find_one(db_file_name=name)['db_file_name']
            dir_path = table.find_one(db_file_name=name)['db_dir_path']
            self.converter(file_name, dir_path)
            self.done_text.insert(END, name + ' Is Done')
            self.window.update()
            if self.delete_file() == 'yes':
                path = os.path.join(dir_path, file_name)
                os.remove(path)
        self.done_text.insert(END, 'All Done')


if __name__ == '__main__':
    root = Tk()
    my_gui = MainWindow(root)
    root.mainloop()
