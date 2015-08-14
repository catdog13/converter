import os
import sys
import subprocess


def main_loop(directory, delete_option):
    def delete_file():
        if delete_option is True:
            delete_text = True
        else:
            delete_text = False
        return delete_text

    def get_input(file_name, default="yes"):
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        while True:
            sys.stdout.write('Do you want to convert ' + file_name + '[Y/n]')
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")

    def create_file_list():
        folder = directory
        file_types = ('.avi', '.wmv', '.mov', '.m4v', '.mkv')
        file_list = []
        for dir_path, dir_names, file_names in os.walk(folder):
            for filename in [f for f in file_names if f.endswith(file_types)]:
                file_path = os.path.join(dir_path, filename)
                if get_input(filename) is True:
                    file_list.append(file_path)
        return file_list

    def converter(path):
        file_type = path[-4:]
        path_without_type = path[:-4]
        if file_type == '.mkv':
            process = 'ffmpeg -hide_banner -i "' + path + '" -metadata title="" -strict experimental ' \
                      '-c:v copy -c:a aac -b:a 384k "' + path_without_type + '.mp4"'
        else:
            process = 'ffmpeg -hide_banner -i "' + path + '" -metadata title=""  -strict experimental ' \
                      '-c:v libx264 -preset ultrafast -c:a aac -b:a 384k "' + path_without_type + '.mp4"'
        subprocess.Popen(process, stdout=subprocess.PIPE).stdout.read()
        if delete_file() is True:
            os.remove(path)

    def loop():
        for file_path in create_file_list():
            converter(file_path)
    loop()

if __name__ == '__main__':
    main_loop(r'D:\TV', True)
    main_loop(r'D:\complete\Movies', True)
    print("All Done")
