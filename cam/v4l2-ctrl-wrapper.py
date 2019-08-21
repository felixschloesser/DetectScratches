import os
import ffmpeg
import subprocess

import subprocess

def list_settings():
    output_bin = subprocess.check_output("v4l2-ctl -l", shell=True)
    output = output_bin.decode()
    output_list = output.splitlines()

    settings = []

    for row in output_list:
        words = row.split()

        dtype = words[1].strip("()")
        setting = {}
        # save the names and the datatype seperatly
        name, dtype, *_ = words

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

    return settings


old_settings = list_settings()

for setting in old_settings:
    print(setting["name"]+": \t", setting["value"])


profile_1 = {"brightness": 0,
             "contrast": 32,
             "saturation": 105,
             "hue": 0,
             "white_balance_temperature_auto": 1,
             "gamma": 100,
             "gain": 2,
             "power_line_frequency": 1,
             "white_balance_temperature": 4600,
             "sharpness": 6,
             "backlight_compensation": 1,
             "exposure_auto": 1,
             "exposure_absolute": 400,
             "exposure_auto_priority": 1
           }

for key, value in profile_1.items():
    os.system("v4l2-ctl --set-ctrl "+key+"="+str(value))


print("\n\n############## NEW SETTINGS #################\n")

new_settings = list_settings()

for setting in new_settings:
    print(setting["name"]+": \t", setting["value"])


"""
os.system("ffmpeg -f v4l2 -input_format mjpeg -ss 1 -i /dev/video0 -video_size 3264x2448 -vframes 1 out.jpg", "y")

v4l2-ctl --set-ctrl sharpness=6
v4l2-ctl --set-ctrl sharpness=6

os.system=
"""



"""
ffmpeg -f v4l2 -input_format mjpeg -ss 1 -i /dev/video0 -video_size 3264x2448 -vframes 1 out.jpg
"""
