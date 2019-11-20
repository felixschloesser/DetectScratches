import os
import subprocess


def list_format(camera):
    """
    Execute the v4l2 get format command, parse its ouput and return it as a dict.

    First execute the command and read its output from stdin. Then format the
    recieved string, remove whitespace and seperate the  width and heigth row.
    create a dict with those two as the first entries.
    Then go through the other rows and save them as keys and values of a dict.
    Return the dict.
    """
    output_bin = subprocess.check_output("v4l2-ctl -d " + str(camera.device_number) +
                                         " --get-fmt-video -k", shell=True)
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
        key = "".join(word for word in key).lower()
        try:
            format[key] = int(value)
        except ValueError:
            format[key] = value.strip("'")


    return format


def list_exposure(camera, full=False):
    """
    Execute the v4l2 list command, parse its ouput and return it as a dict.

    If *full*-output is false (default) First execute the command and read its
    output from stdin. Then format the recieved string, remove whitespace and
    seperate the  width and heigth row.create a dict with those two as the first entries.
    Then go through the other rows and save them as keys and values of a dict.
    Return the dict.

    Else it puts out all key values pairs of the original stdout in a big list of dicts.
    """
    output_bin = subprocess.check_output("v4l2-ctl -d " + str(camera.device_number) +
                                         " -l", shell=True)
    output = output_bin.decode()
    output_list = output.splitlines()

    if full:
        exposures = []
    else:
     exposures = {}


    for row in output_list:
        words = row.split()

        dtype = words[1].strip("()")

        # save the names and the datatype seperatly
        name, dtype, *_ = words

        if full:
            exposure = {}

            exposure["name"] = name
            exposure["dtype"] = dtype.strip("()")

            # Cut off the first bit
            words = words[3:]
            for word in words:
                key, value = word.split("=")
                try:
                    exposure[key] = int(value)
                except ValueError:
                    exposure[key] = value
            exposures.append(exposure)

        else:
            words = words[3:]
            for word in words:
                key, value = word.split("=")
                if key == 'value':
                    try:
                        exposures[name] = int(value)
                    except ValueError:
                        exposures[name] = value


    return exposures
