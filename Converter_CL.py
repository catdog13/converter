import os
import sys
import subprocess


def main_loop(directory, delete_option):
    def get_input(file_name, default="yes"):
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        while True:
            sys.stdout.write('Do you want to convert {} [Y/n]'.format(file_name))
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
        file_type = os.path.splitext(path)[-1]
        path_without_type = os.path.splitext(path)[0]
        if file_type == '.mkv':
            process = 'ffmpeg -hide_banner -i "{}" -metadata title="" -strict experimental ' \
                      '-c:v copy -c:a aac -b:a 384k "{}.mp4"'.format(path, path_without_type)
        else:
            process = 'ffmpeg -hide_banner -i "{}" -metadata title=""  -strict experimental ' \
                      '-c:v libx264 -preset ultrafast -c:a aac -b:a 384k "{}.mp4"'.format(path, path_without_type)
        print('Starting', path)
        subprocess.call(process, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if delete_option:
            os.remove(path)
        print('Finished', path)

    for file_path in create_file_list():
        converter(file_path)


if __name__ == '__main__':
    main_loop(r'D:\TV', True)
    main_loop(r'D:\complete\Movies', True)
    print("All Done")
