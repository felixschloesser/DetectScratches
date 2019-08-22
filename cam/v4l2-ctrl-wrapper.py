import os
import numpy as np
import ffmpeg
import subprocess

import sys

sys.path.append("/home/tintin/rongheng/cv/")
from lib.image_lib import show_img

import PIL.Image as Image


def list_format():
    output_bin = subprocess.check_output("v4l2-ctl --get-fmt-video -k", shell=True)
    output = output_bin.decode()
    output_list = output.splitlines()
    output_list.pop(0) # throw away first line (Title)
    output_list.pop() # throw away flags

    size_line = output_list.pop(0) # seperate the size line
    size_line = size_line.split() # remove whitespace
    size = size_line[-1].split('/') # sp

    width, height = size

    format = {"width": int(width), "height": int(height)}

    for row in output_list:
        words = row.split() # remove whitespace
        *key, _, value = words
        key = str1 = " ".join(word for word in key)
        try:
            format[key] = int(value)
        except ValueError:
            format[key] = value.strip("'")


    return format


def list_settings(full=False):
    output_bin = subprocess.check_output("v4l2-ctl -l", shell=True)
    output = output_bin.decode()
    output_list = output.splitlines()

    if full:
        settings = []
    else:
     settings = {}


    for row in output_list:
        words = row.split()

        dtype = words[1].strip("()")

        # save the names and the datatype seperatly
        name, dtype, *_ = words

        if full:
            setting = {}

            setting["name"] = name
            setting["dtype"] = dtype.strip("()")

            # Cut off the first bit
            words = words[3:]
            for word in words:
                key, value = word.split("=")
                try:
                    setting[key] = int(value)
                except ValueError:
                    setting[key] = value
            settings.append(setting)

        else:
            words = words[3:]
            for word in words:
                key, value = word.split("=")
                if key == 'value':
                    try:
                        settings[name] = int(value)
                    except ValueError:
                        settings[name] = value


    return settings



my_format = {
    "width": 3264,
    "height": 2448,
    "pixelformat": 'MJPG',
    "field": 'Default',
    "bytesperline": 'Default',
    "colorspace": 'Default',
    "xfer": 'Default',
    "ycbcr": 'Default',
    "quantization": 'Default'
}

my_settings = {
    "brightness": 0,
    "contrast": 64,
    "saturation": 90,
    "hue": 0,
    "white_balance_temperature_auto": 1,
    "gamma": 72,
    "gain": 0,
    "power_line_frequency": 1,
    "white_balance_temperature": 4600,
    "sharpness": 0,
    "backlight_compensation": 1,
    "exposure_auto": 1,
    "exposure_absolute": 800,
    "exposure_auto_priority": 0
}



old_format = list_format()
old_settings = list_settings()


diff_format = {key: my_value for key, my_value in my_format.items()
               if my_value not in old_format.values()}

diff_settings = {key: my_value for key, my_value in my_settings.items()
               if my_value not in old_settings.values()}

for key, value in diff_format.items():
    if key == 'width' or key == 'height':
        os.system("v4l2-ctl --set-fmt-video width=" + str(my_format['width'])
                  + ",height=" + str(my_format['height']))
    if value != "Default":
        os.system("v4l2-ctl --set-fmt-video " + key + "=" + str(value))

for key, value in diff_settings.items():
    os.system("v4l2-ctl --set-ctrl " + key + "=" + str(value))


if diff_format:
    print("FORMAT:")
    print("=======")
    for key, value in diff_format.items():
        print(key + ":", value)

if diff_settings:
    print("")
    print("SETTINGS:")
    print("=========")
    for key, value in diff_settings.items():
        print(key + ":", value)


try:
    out, _ = (
        ffmpeg
        .input('/dev/video0', format='v4l2', pix_fmt="mjpeg", ss=1)
        .output('out8.jpg', vframes=1, format='image2', vcodec='mjpeg')
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )
except ffmpeg.Error as e:
    print("Error:", e.stderr.decode(), file=sys.stderr)
    sys.exit(1)


"""

try:
    out, _ = (
    ffmpeg
    .input('/dev/video0', format='v4l2', pix_fmt="mjpeg", ss=1)
    #.filter('scale', width, -1)
    .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
    .overwrite_output()
    .run(capture_stdout=True, capture_stderr=True)
    )
except ffmpeg.Error as e:
    print(e.stderror.decode(), file=sys.stderr)
    sys.exit(1)



picture = (
    np
    .frombuffer(out, np.uint8)
    .reshape([-1, my_format['height'], my_format['width'], 3])
    )


show_img(img)
"""

"""
os.system("ffmpeg -f v4l2 -input_format mjpeg -ss 1 -i /dev/video0 -video_size 3264x2448 -vframes 1 out.jpg", "y")
"""
