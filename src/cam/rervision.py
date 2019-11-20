#!/home/tintin/rongheng/cv/cam/.env/bin/python

import os
import sys
import ffmpeg
import v4l2wrapper



class Camera(object):
    """The camera Object, handles mainly IO."""
    def __init__(self, device_name):
        """Initialize object with the name of the device, ex: /dev/video0."""
        self.device_name = device_name
        self.init_device()
        self.get_format()
        self.get_exposure()

    def __repr__(self):
        return f"Camera {0}".format(self.device_number)


    def init_device(self):
        """Probe device to see if ffmpeg can recognize a camera."""
        try:
            ffmpeg.probe(self.device_name)
        except:
            print("Error: Could not find device", self.device_name,
                "- Please try reconnecting the camera.")
            sys.exit(1)

        self.device_number = [int(s) for s in list(self.device_name) if s.isdigit()].pop()

    def get_format(self):
        self.format = Format(self)


    def get_exposure(self):
        self.exposure = Exposure(self)

    def capture_img(self, filename):
        #ffmpeg -f v3l2 -ss 1 -i /dev/video0  -input_format mjpeg -vframes 1 filename.jpeg
        try:
            out = ffmpeg.input(self.device_name, format='v4l2', ss=1.5)
            if filename:
                out = out.output(filename, input_format='mjpeg', vframes=1)
            else:
                out = out.output("out.jpg", vframes=1)
            ffmpeg.overwrite_output(out)
            out.run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

        except ffmpeg.Error as e:
            print("Error:", e.stderr.decode(), file=sys.stderr)
            sys.exit(1)



class Format(object):
    def __init__(self, camera):
        self.device_name = camera
        self.get()

    def get(self):
        """Parse output of v4l2-ctl, extract dict and set attributes."""
        formats = v4l2wrapper.list_format(self.device_name)
        for key in formats:
            setattr(self, key, formats[key])

    def set(self, **settings):
        aspect_ratio = 4/3

        for key, value in settings.items():
            if key == "width":
                os.system("v4l2-ctl --set-fmt-video width=" + str(value) +
                          ",height=" + str(int(value/aspect_ratio)) )
            elif key == "height":
                os.system("v4l2-ctl --set-fmt-video width=" + str(int(value*aspect_ratio)) +
                          ",height=" + str(value))
            else:
                os.system("v4l2-ctl --set-fmt-video " + key + "=" + str(value))

        self.get()


class Exposure(Camera):
    def __init__(self, camera):
        self.device_name = camera
        self.get()

    def get(self):
        """Parse output of v4l2-ctl, extract dict and set attributes."""
        exposure = v4l2wrapper.list_exposure(self.device_name)
        for key in exposure:
            setattr(self, key, exposure[key])

    def set(self, **settings):
        for key, value in settings.items():
            os.system("v4l2-ctl --set-ctrl " + key + "=" + str(value))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
    description='Read individual video frame and save it as jpeg')
    parser.add_argument('-o','--out_filename', type=str, help='Output filename')
    parser.add_argument('-s','--sharpness', default=0, help='Set sharpness, default 0')
    parser.add_argument('-e','--exposure', default=300, help='Set exposure_absolute, default 400')

    args = parser.parse_args()


    cam = Camera("/dev/video0")

    cam.format.set(width=3264,
                   height=2448,
                   pixelformat='mjpeg'
                   )
    cam.exposure.set(brightness=0,
                     contrast=64,
                     saturation=90,
                     gamma=72,
                     gain=0,
                     sharpness=0,
                     backlight_compensation=1,
                     exposure_auto=1,
                     exposure_absolute=300,
                     exposure_auto_priority=0
                    )

    if args.sharpness:
        cam.exposure.set(sharpness=args.sharpness)

    if args.exposure:
        cam.exposure.set(exposure_absolute=args.exposure)

    if args.out_filename:
        cam.capture_img(args.out_filename)
    else:
        cam.capture_img("out.jpg")
