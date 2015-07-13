import subprocess


def converter():
    path = r"insert full path including file name here"
    path_without = path.strip(".mkv")
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
    args = ' -hide_banner -i "' + path + \
        '" -metadata title="" -strict experimental ' \
        '-map 0:0 -c:v copy ' \
        '-map 0:2 -c:a aac -b 192k "' + path_without + '.mp4"'

    process = ffmpeg_path + args
    subprocess.Popen(process, stdout=subprocess.PIPE).stdout.read()

converter()
