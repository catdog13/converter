import subprocess
import os
import time


def convert(directory):
    def create_file_list():
        folder = directory
        file_types = ".flac"
        file_list = list()
        for dir_path, dir_names, file_names in os.walk(folder):
            for filename in [f for f in file_names if f.endswith(file_types)]:
                path = os.path.join(dir_path, filename)
                file_list.append(path)
        return file_list

    def converter(path):
        path_without_type = path.strip(".flac")
        new_path = path_without_type.replace("foobar2000", "mp3")
        dir_path = path.rsplit('\\', 1)[0]
        new_dir_path = dir_path.replace("foobar2000", "mp3")
        if not os.path.isdir(new_dir_path):
            os.makedirs(new_dir_path)
        args = ' -hide_banner -i "' + path + '" -ab 192k -map_metadata 0 -id3v2_version 3 "' \
               + new_path + '.mp3"'
        process = 'ffmpeg' + args
        subprocess.Popen(process, stdout=subprocess.PIPE).stdout.read()

    def loop():
        for file_path in create_file_list():
            converter(file_path)
    loop()

if __name__ == '__main__':
    start_time = time.time()
    convert(r'E:\Music\foobar2000')
    print("Done In " + str(round((time.time() - start_time), 2)) + " seconds")
