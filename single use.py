import subprocess


def converter():
    path = r"insert full path including file name here"
    path_without = path.strip(".mkv")
    process = 'ffmpeg -hide_banner -i "' + path + \
              '" -metadata title="" -strict experimental ' \
              '-map 0:0 -c:v copy ' \
              '-map 0:2 -c:a aac -b:a 384k "' + path_without + '.mp4"'

    subprocess.Popen(process, stdout=subprocess.PIPE).stdout.read()

converter()
