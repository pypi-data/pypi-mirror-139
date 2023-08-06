import sys
from ..video import video2images, images2video


def cli_images2video():
    args = sys.argv
    print(args)
    images2video(*args)


def cli_video2images():
    args = sys.argv
    video2images(*args)
