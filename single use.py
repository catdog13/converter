import subprocess
import os


def converter(path):
    path_without = os.path.splitext(path)[0]
    process = 'ffmpeg -hide_banner -i "{}" -metadata title="" -strict experimental ' \
              '-map 0:0 -c:v copy ' \
              '-map 0:2 -c:a aac -b:a 384k "{}.mp4"'.format(path, path_without)

    subprocess.Popen(process, stdout=subprocess.PIPE).stdout.read()

converter(r'')
