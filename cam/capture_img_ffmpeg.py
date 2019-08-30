#!/home/tintin/rongheng/cv/cam/.env/bin/python
import os
import ffmpeg
import subprocess
import sys
sys.path.append("/home/tintin/rongheng/cv/")
from lib.image_lib import show_img

# Parser

import argparse

parser = argparse.ArgumentParser(
    description='Read individual video frame and save it as jpeg')
parser.add_argument('-o','--out_filename', type=str, help='Output filename')
parser.add_argument('-a','--alternative', help='Alternative Conversion',
                    action="store_true")

args = parser.parse_args()


def list_format():
    """
    Execute the v4l2 get format command, parse its ouput and return it as a dict.

    First execute the command and read its output from stdin. Then format the
    recieved string, remove whitespace and seperate the  width and heigth row.
    create a dict with those two as the first entries.
    Then go through the other rows and save them as keys and values of a dict.
    Return the dict.
    """
    output_bin = subprocess.check_output("v4l2-ctl --get-fmt-video -k",
                                         shell=True)
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
    """
    Execute the v4l2 list command, parse its ouput and return it as a dict.

    If *full*-output is false (default) First execute the command and read its
    output from stdin. Then format the recieved string, remove whitespace and
    seperate the  width and heigth row.create a dict with those two as the first entries.
    Then go through the other rows and save them as keys and values of a dict.
    Return the dict.

    Else it puts out all key values pairs of the original stdout in a big list of dicts.
    """
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


# Setting the format

def set_format(my_format, echo=False):
    """
    Exectues (only) the commands neccesary to set the camera to the format
    specified in my_format, skips defautls
    """
    old_format = list_format()

    diff_format = {key: my_value for key, my_value in my_format.items()
               if my_value not in old_format.values()}

    if print:
        if diff_format:
            print("FORMAT:")
            print("=======")
            for key, value in diff_format.items():
                print(key + ":", value)

    for key, value in diff_format.items():
        if key == 'width' or key == 'height':
            os.system("v4l2-ctl --set-fmt-video \
                    width=" + str(my_format['width'])
                      + ",height=" + str(my_format['height']))
        if value != "Default":
            os.system("v4l2-ctl --set-fmt-video " + key + "=" + str(value))


def set_settings(my_settings, echo=False):
    """
    Exectues (only) the commands neccesary to set the camera to the settings
    specified in my_settings
    """
    old_settings = list_settings()

    diff_settings = {key: my_value for key, my_value in my_settings.items()
                     if my_value not in old_settings.values()}

    if print:
        if diff_settings:
            print("")
            print("SETTINGS:")
            print("=========")
            for key, value in diff_settings.items():
                print(key + ":", value)

    for key, value in diff_settings.items():
        os.system("v4l2-ctl --set-ctrl " + key + "=" + str(value))

# Custom Format

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
    "exposure_absolute": 1300,
    "exposure_auto_priority": 0
}


try:
    ffmpeg.probe('/dev/video0')
except:
    print("Error: Could not find device '/dev/video0'. Please try reconnecting the camera.")
    sys.exit(0)

set_format(my_format, echo=True)
set_settings(my_settings, echo=True)

try:
    """
    ffmpeg -f v4l2 -i=/dev/video0 -pixel_format=mjpeg -ss=1 -vframes=1 out.jpg
    ffmpeg -f v4l2 -i /dev/video0 -ss 1 -input_format mjpeg -pixel_format mjpeg -vframes 1 out3.jpg
    ffmpeg -f v3l2 -ss 1 -i /dev/video0  -input_format mjpeg -vframes 1 c0.1.jpeg
    """

    out = ffmpeg.input('/dev/video0', format='v4l2', ss=1.5)
    if args.out_filename:
        out = out.output(args.out_filename, input_format='mjpeg', vframes=1)
    else:
        out = out.output("out.jpg", vframes=1)

    ffmpeg.overwrite_output(out)
    out.run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

except ffmpeg.Error as e:
    print("Error:", e.stderr.decode(), file=sys.stderr)
    sys.exit(1)

