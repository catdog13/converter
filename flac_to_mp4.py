import subprocess
import os
import time
import shutil


def convert(directory):
    def create_file_list():
        folder = directory
        file_list = []
        cover_list = []
        for root, subdir, files in os.walk(folder):
            for songs in files:
                if songs.endswith('.flac'):
                    full_path = os.path.join(root, songs)
                    file_list.append(full_path)
            for covers in files:
                if covers.endswith('.jpg'):
                    cover_path = os.path.join(root, covers)
                    cover_list.append(cover_path)
        return file_list, cover_list

    def converter(path):
        path_without_type = path.strip(".flac")
        new_path = path_without_type.replace("foobar2000", "mp3")
        dir_path = path.rsplit('\\', 1)[0]
        new_dir_path = dir_path.replace("foobar2000", "mp3")
        if not os.path.isdir(new_dir_path):
            os.makedirs(new_dir_path)
        process = 'ffmpeg -hide_banner -i "' + path + '" -ab 192k -map_metadata 0 -id3v2_version 3 "' \
                  + new_path + '.mp3"'
        print('Starting ' + path)
        subprocess.call(process, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('Finished ' + path)

    def mover(path):
        new_path = path.replace("foobar2000", "mp3")
        shutil.copy2(path, new_path)

    def loop():
        for song_path in create_file_list()[0]:
            converter(song_path)
        for cover_path in create_file_list()[1]:
            mover(cover_path)
    loop()

if __name__ == '__main__':
    start_time = time.time()
    convert(r'D:\Music\foobar2000')
    print("Done In " + str(round((time.time() - start_time), 2)) + " seconds")
