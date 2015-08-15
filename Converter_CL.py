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
        for root, subdir, files in os.walk(folder):
            for file in files:
                if file.endswith(file_types):
                    full_path = os.path.join(root, file)
                    if get_input(file) is True:
                        file_list.append(full_path)
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
        print('Starting ' + path)
        subprocess.call(process, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if delete_file() is True:
            os.remove(path)
        print('Finished ' + path)

    def loop():
        for file_path in create_file_list():
            converter(file_path)
    loop()

if __name__ == '__main__':
    main_loop(r'D:\TV', True)
    main_loop(r'D:\complete\Movies', True)
    print("All Done")
